import uuid
from django.db import models
from apps.contact.models import ContactRequest

class VisitorSession(models.Model):
    CHAT_MODE_CHOICES = (
        ('AI', 'AI'),
        ('Human', 'Human'),
        ('Hybrid', 'Hybrid'),
    )
    CHAT_STATUS_CHOICES = (
        ('No Chat', 'No Chat'),
        ('Active', 'Active'),
        ('Idle', 'Idle'),
        ('Closed', 'Closed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor_id = models.CharField(max_length=255, db_index=True)
    session_id = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    browser = models.CharField(max_length=100, default='Unknown')
    device = models.CharField(max_length=100, default='Desktop')
    os = models.CharField(max_length=100, default='Unknown')
    screen_size = models.CharField(max_length=50, default='Unknown')
    country = models.CharField(max_length=100, default='Unknown')
    city = models.CharField(max_length=100, default='Unknown')
    referrer = models.TextField(null=True, blank=True)
    first_visit = models.BooleanField(default=True)
    is_returning = models.BooleanField(default=False)
    
    current_url = models.TextField(default='')
    current_page_title = models.CharField(max_length=255, default='Home')
    previous_url = models.TextField(null=True, blank=True)
    
    time_on_current_page = models.IntegerField(default=0)  # in seconds
    total_duration = models.IntegerField(default=0)  # in seconds
    scroll_percentage = models.IntegerField(default=0)
    max_scroll = models.IntegerField(default=0)
    
    current_section = models.CharField(max_length=255, default='Hero')
    active_tab = models.CharField(max_length=255, default='Visible')
    is_idle = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    
    lead_score = models.IntegerField(default=0)
    lead = models.ForeignKey(ContactRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='visitor_sessions')
    
    chat_mode = models.CharField(max_length=20, default='AI', choices=CHAT_MODE_CHOICES)
    chat_status = models.CharField(max_length=20, default='No Chat', choices=CHAT_STATUS_CHOICES)
    scored_milestones = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visitor Session"
        verbose_name_plural = "Visitor Sessions"
        ordering = ['-last_activity']

    def __str__(self):
        return f"Session: {self.session_id} ({self.ip_address})"

    @property
    def conversion_probability(self):
        prob = 10
        if self.lead_score > 0:
            prob += min(self.lead_score * 0.7, 60)
        if self.total_duration > 60:
            prob += 10
        if self.max_scroll > 50:
            prob += 10
        if self.referrer and ('google' in self.referrer.lower() or 'linkedin' in self.referrer.lower()):
            prob += 10
        return min(int(prob), 99)

    @property
    def recommended_service(self):
        if self.lead and self.lead.service:
            return self.lead.service
        url = self.current_url.lower()
        if 'chatbot' in url or 'ai' in url:
            return "AI Chatbot & Automation"
        if 'seo' in url or 'performance' in url:
            return "Performance Marketing & SEO"
        if 'cloud' in url or 'engineering' in url:
            return "Cloud Engineering"
        return "Custom Software Development"

    @property
    def estimated_budget(self):
        if self.lead and self.lead.budget:
            return self.lead.budget
        if self.device == 'Desktop' and self.lead_score > 60:
            return "$25K - $50K"
        return "$10K - $25K"

    @property
    def urgency(self):
        score = self.lead_score
        if score >= 80:
            return "Critical"
        elif score >= 50:
            return "High"
        elif score >= 25:
            return "Medium"
        return "Low"

class VisitorTimelineEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='timeline_events')
    event_type = models.CharField(max_length=50)  # PageView, SectionView, ChatOpened, FormSubmitted, ChatMessage, LeadConverted, etc.
    description = models.CharField(max_length=255)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Visitor Timeline Event"
        verbose_name_plural = "Visitor Timeline Events"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.event_type} on {self.session.session_id}: {self.description}"

class SessionReplayFrame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='replay_frames')
    events_data = models.TextField()  # JSON-serialized array of user actions (clicks, moves, scrolls)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Session Replay Frame"
        verbose_name_plural = "Session Replay Frames"
        ordering = ['created_at']

    def __str__(self):
        return f"Replay Frame for {self.session.session_id} at {self.created_at.strftime('%H:%M:%S')}"

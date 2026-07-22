import uuid
from django.db import models
from django.conf import settings
from apps.contact.models import ContactRequest

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.OneToOneField(ContactRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='converted_client')
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name

class Project(models.Model):
    STATUS_CHOICES = (
        ('Planning', 'Planning'),
        ('Development', 'Development'),
        ('Testing', 'Testing'),
        ('Live', 'Live'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Planning')
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.client.company_name})"

class CRMNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.ForeignKey(ContactRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='crm_notes')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='crm_notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "CRM Note"
        verbose_name_plural = "CRM Notes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.author} on {self.created_at.strftime('%Y-%m-%d')}"

class Lead(ContactRequest):
    class Meta:
        proxy = True
        verbose_name = "Lead / Contact Request"
        verbose_name_plural = "Leads / Contact Requests"


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='proposals')
    lead = models.ForeignKey(ContactRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='proposals')
    title = models.CharField(max_length=255)
    services = models.TextField(help_text="List of services or packages included.")
    scope = models.TextField(help_text="Project scope and description.")
    timeline = models.CharField(max_length=255, default="3 Months")
    pricing = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    milestones = models.TextField(help_text="Project milestones and deliverables.")
    terms = models.TextField(blank=True, help_text="Standard terms and conditions.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Valued: ${self.pricing:,.2f})"


class Contract(models.Model):
    CONTRACT_TYPES = (
        ('NDA', 'Non-Disclosure Agreement'),
        ('SOW', 'Statement of Work'),
        ('Development', 'Development Agreement'),
        ('Maintenance', 'Maintenance Agreement'),
        ('Support', 'Support Service Level Agreement'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contracts')
    proposal = models.ForeignKey(Proposal, on_delete=models.SET_NULL, null=True, blank=True, related_name='contracts')
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPES, default='SOW')
    content = models.TextField()
    is_signed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_contract_type_display()} - {self.client.company_name}"


class Invoice(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
        ('Cancelled', 'Cancelled'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    invoice_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00, help_text="GST percentage rate.")
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto calculate tax and totals on save
        self.gst_amount = self.amount * (self.gst_rate / 100)
        self.total_amount = self.amount + self.gst_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} ({self.client.company_name} - ${self.total_amount:,.2f})"


class WorkspaceTask(models.Model):
    STATUS_CHOICES = (
        ('Todo', 'Todo'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Todo')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class CalendarEvent(models.Model):
    EVENT_TYPES = (
        ('Meeting', 'Meeting'),
        ('Deadline', 'Deadline'),
        ('Interview', 'Interview'),
        ('Follow Up', 'Follow Up'),
        ('Content Schedule', 'Content Schedule'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default='Meeting')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.event_type})"


class KnowledgeDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='knowledge_docs/', null=True, blank=True)
    url = models.URLField(blank=True)
    content = models.TextField(help_text="Extracted text content from file or URL.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=KnowledgeDocument)
def process_knowledge_document(sender, instance, created, **kwargs):
    if created or not instance.content:
        if instance.url:
            try:
                res = requests.get(instance.url, timeout=5)
                if res.status_code == 200:
                    # Quick text extractor
                    from django.utils.html import strip_tags
                    clean_text = strip_tags(res.text)
                    clean_text = ' '.join(clean_text.split())
                    KnowledgeDocument.objects.filter(id=instance.id).update(content=clean_text[:10000])
            except Exception as e:
                print(f"Error scraping URL: {e}")
        elif instance.file:
            try:
                if instance.file.name.endswith('.txt') or instance.file.name.endswith('.md'):
                    instance.file.open('r')
                    file_content = instance.file.read()
                    instance.file.close()
                    if isinstance(file_content, bytes):
                        file_content = file_content.decode('utf-8')
                    KnowledgeDocument.objects.filter(id=instance.id).update(content=file_content[:15000])
            except Exception as e:
                print(f"Error reading file: {e}")





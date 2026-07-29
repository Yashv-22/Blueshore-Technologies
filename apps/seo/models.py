import uuid
from django.db import models

class SEOPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page_name = models.CharField(max_length=255, help_text="Internal identifier or name of the page")
    route = models.CharField(max_length=255, unique=True, help_text="Path of the page, e.g., '/' or '/contact.html'")
    seo_title = models.CharField(max_length=255)
    seo_description = models.TextField()
    seo_keywords = models.TextField(blank=True, help_text="Comma-separated keywords")
    canonical_url = models.URLField(max_length=500, blank=True)
    robots = models.CharField(max_length=255, default="index, follow", help_text="Robots meta directives (e.g. 'index, follow')")
    
    # Open Graph
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='seo/og/', blank=True, null=True)
    
    # Twitter Cards
    twitter_title = models.CharField(max_length=255, blank=True)
    twitter_description = models.TextField(blank=True)
    twitter_image = models.ImageField(upload_to='seo/twitter/', blank=True, null=True)
    
    # Custom / Overriding JSON Schema Markup
    schema_markup = models.JSONField(blank=True, null=True, help_text="Custom static JSON-LD schema blocks (optional)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Page"
        verbose_name_plural = "SEO Pages"
        ordering = ['page_name']

    def __str__(self):
        return f"{self.page_name} ({self.route})"


class GEOBlock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.OneToOneField(SEOPage, on_delete=models.CASCADE, related_name='geo_block')
    ai_summary = models.TextField(help_text="Concise summary targeted directly at AI Search Overviews / LLM crawlers")
    featured_answer = models.TextField(help_text="Short answer targeted at Google Featured Snippets")
    what_is_this = models.TextField()
    why_it_matters = models.TextField()
    who_is_it_for = models.TextField()
    key_takeaways = models.TextField(help_text="Key takeaways, enter one per line")
    eeat_proof_points = models.TextField(help_text="E-E-A-T proof points, enter one per line")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "GEO Block"
        verbose_name_plural = "GEO Blocks"

    def __str__(self):
        return f"GEO Block for {self.page.page_name}"

    @property
    def takeaways_list(self):
        if not self.key_takeaways:
            return []
        return [line.strip() for line in self.key_takeaways.split('\n') if line.strip()]

    @property
    def proof_points_list(self):
        if not self.eeat_proof_points:
            return []
        return [line.strip() for line in self.eeat_proof_points.split('\n') if line.strip()]


class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(SEOPage, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.IntegerField(default=0, help_text="Order in which FAQ is displayed")
    is_active = models.BooleanField(default=True, help_text="Toggles visibility in AEO sections")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"FAQ: {self.question[:50]} (Page: {self.page.page_name})"


# Cache Invalidation Signals for dynamic SEO Middleware
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

@receiver([post_save, post_delete], sender=SEOPage)
@receiver([post_save, post_delete], sender=GEOBlock)
@receiver([post_save, post_delete], sender=FAQ)
@receiver([post_save, post_delete], sender='blog.BlogPost')
@receiver([post_save, post_delete], sender='portfolio.PortfolioProject')
def clear_seo_cache(sender, **kwargs):
    cache.clear()


class RobotsRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_agent = models.CharField(max_length=255, default="*", help_text="User-agent, e.g. '*', 'GPTBot', 'PerplexityBot'")
    allow_paths = models.TextField(blank=True, help_text="Allowed paths, one per line (optional)")
    disallow_paths = models.TextField(blank=True, help_text="Disallowed paths, one per line (optional)")
    crawl_delay = models.IntegerField(null=True, blank=True, help_text="Crawl delay in seconds (optional)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Robots.txt Rule"
        verbose_name_plural = "Robots.txt Rules"

    def __str__(self):
        return f"Robots Rule for: {self.user_agent}"


@receiver([post_save, post_delete], sender=RobotsRule)
def clear_robots_cache(sender, **kwargs):
    cache.delete('seo_robots_txt_content')


class ServicePillar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_slug = models.CharField(max_length=255, unique=True, help_text="Unique slug, e.g., 'crm-integrations'")
    name = models.CharField(max_length=255, help_text="Clean service name, e.g. 'CRM Creation & Integrations'")
    title = models.CharField(max_length=255, help_text="SEO Title")
    description = models.TextField(help_text="SEO Meta Description")
    tagline = models.CharField(max_length=255, help_text="Hero section tagline")
    hero_bg_color = models.CharField(max_length=50, default="#3790ff", help_text="Hex code background highlight")
    
    # Body copy - structured Markdown or HTML (3,000–5,000 words)
    body_content = models.TextField(help_text="Primary pillar body copy (HTML/Markdown)")
    
    # JSON-structured fields
    process_json = models.JSONField(blank=True, null=True, help_text="List of process steps: [{'step': 1, 'title': '...', 'desc': '...'}]")
    tech_stack_json = models.JSONField(blank=True, null=True, help_text="List of technologies: [{'name': '...', 'icon': '...'}]")
    faq_json = models.JSONField(blank=True, null=True, help_text="List of FAQs: [{'q': '...', 'a': '...'}]")
    testimonials_json = models.JSONField(blank=True, null=True, help_text="List of client testimonials: [{'client': '...', 'text': '...'}]")
    case_studies_json = models.JSONField(blank=True, null=True, help_text="List of case studies: [{'title': '...', 'metric': '...', 'desc': '...'}]")
    
    cta_text = models.CharField(max_length=255, default="Get Started")
    cta_link = models.CharField(max_length=255, default="/contact.html")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Pillar Page"
        verbose_name_plural = "Service Pillar Pages"
        ordering = ['name']

    def __str__(self):
        return f"Pillar: {self.name} (/services/{self.service_slug}/)"
        
@receiver([post_save, post_delete], sender=ServicePillar)
def clear_pillar_cache(sender, **kwargs):
    cache.clear()


# ==============================================================================
# SEO & GROWTH OPERATING SYSTEM (OS) ENTITY GRAPH & CONTENT HUBS
# ==============================================================================

class SEOEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, help_text="Canonical Entity Name (e.g. 'RAG', 'Docker', 'Django')")
    slug = models.SlugField(max_length=255, unique=True)
    entity_type = models.CharField(max_length=100, choices=[
        ('technology', 'Technology / Framework'),
        ('concept', 'Architectural Concept'),
        ('industry', 'Industry Vertical'),
        ('compliance', 'Compliance / Standard'),
        ('solution', 'Solution Type')
    ], default='technology')
    description = models.TextField(blank=True, help_text="Machine-readable entity definition")
    wikidata_url = models.URLField(blank=True, max_length=500)
    wikipedia_url = models.URLField(blank=True, max_length=500)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Entity"
        verbose_name_plural = "SEO Entities"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()})"


class GlossaryTerm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.CharField(max_length=255, unique=True, help_text="Term name, e.g. 'Retrieval Augmented Generation (RAG)'")
    slug = models.SlugField(max_length=255, unique=True)
    short_definition = models.TextField(help_text="20-40 word direct AEO definition for Google Featured Snippets & AI Overviews")
    detailed_explanation = models.TextField(help_text="Comprehensive technical explanation (Markdown/HTML)")
    code_example = models.TextField(blank=True, help_text="Optional Python/JS/Config snippet")
    architecture_diagram_mermaid = models.TextField(blank=True, help_text="Optional Mermaid JS diagram syntax")
    category = models.CharField(max_length=100, default="AI & Automation")
    
    entities = models.ManyToManyField(SEOEntity, blank=True, related_name='glossary_terms')
    related_services = models.ManyToManyField(ServicePillar, blank=True, related_name='glossary_terms')
    
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Glossary Term"
        verbose_name_plural = "Glossary Terms"
        ordering = ['term']

    def __str__(self):
        return f"Glossary: {self.term} (/glossary/{self.slug}/)"


class ComparisonPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text="Comparison title, e.g. 'FastAPI vs Django: B2B Architecture Comparison'")
    slug = models.SlugField(max_length=255, unique=True)
    entity_a = models.CharField(max_length=100, help_text="First tech/solution name, e.g. 'FastAPI'")
    entity_b = models.CharField(max_length=100, help_text="Second tech/solution name, e.g. 'Django'")
    verdict_summary = models.TextField(help_text="Executive summary and architectural recommendation")
    comparison_matrix_json = models.JSONField(blank=True, null=True, help_text="[{'feature': 'Performance', 'a': '...', 'b': '...'}]")
    detailed_breakdown = models.TextField(help_text="Full comparison body copy (HTML/Markdown)")
    
    related_entities = models.ManyToManyField(SEOEntity, blank=True, related_name='comparisons')
    related_services = models.ManyToManyField(ServicePillar, blank=True, related_name='comparisons')
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comparison Page"
        verbose_name_plural = "Comparison Pages"
        ordering = ['title']

    def __str__(self):
        return f"Compare: {self.title} (/compare/{self.slug}/)"


class B2BResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text="Resource title, e.g. 'Enterprise SOC 2 Compliance & Architecture Guide'")
    slug = models.SlugField(max_length=255, unique=True)
    resource_type = models.CharField(max_length=100, choices=[
        ('guide', 'Architecture Guide'),
        ('checklist', 'Security Checklist'),
        ('whitepaper', 'Technical Whitepaper'),
        ('template', 'Code Template'),
        ('playbook', 'Engineering Playbook')
    ], default='guide')
    summary = models.TextField(help_text="Overview of resource benefits")
    file_url = models.CharField(max_length=500, blank=True, help_text="Path or external link to resource asset")
    reading_time_min = models.IntegerField(default=10)
    
    related_services = models.ManyToManyField(ServicePillar, blank=True, related_name='resources')
    
    is_published = models.BooleanField(default=True)
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "B2B Resource"
        verbose_name_plural = "B2B Resources"
        ordering = ['-created_at']

    def __str__(self):
        return f"Resource: {self.title} (/resources/{self.slug}/)"


class TechnologyHubPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Technology name, e.g. 'Django Enterprise Framework'")
    slug = models.SlugField(max_length=255, unique=True)
    hero_title = models.CharField(max_length=255)
    description = models.TextField(help_text="Meta description and hero snippet")
    architectural_benefits = models.TextField(help_text="Core advantages for B2B applications")
    code_example = models.TextField(blank=True, help_text="Production-grade implementation snippet")
    use_cases_json = models.JSONField(blank=True, null=True, help_text="[{'title': '...', 'desc': '...'}]")
    
    related_services = models.ManyToManyField(ServicePillar, blank=True, related_name='technologies')
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Technology Hub Page"
        verbose_name_plural = "Technology Hub Pages"
        ordering = ['name']

    def __str__(self):
        return f"Tech Hub: {self.name} (/technology/{self.slug}/)"


class IndustryHubPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Industry vertical, e.g. 'Healthcare & Telehealth'")
    slug = models.SlugField(max_length=255, unique=True)
    hero_title = models.CharField(max_length=255)
    description = models.TextField()
    compliance_frameworks = models.CharField(max_length=255, default="HIPAA, SOC 2, ISO 27001", help_text="Comma-separated frameworks")
    key_challenges = models.TextField(help_text="Specific operational bottlenecks in this sector")
    tailored_solutions_json = models.JSONField(blank=True, null=True)
    
    related_services = models.ManyToManyField(ServicePillar, blank=True, related_name='industries')
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Industry Hub Page"
        verbose_name_plural = "Industry Hub Pages"
        ordering = ['name']

    def __str__(self):
        return f"Industry Hub: {self.name} (/industry/{self.slug}/)"


# ==============================================================================
# COMPETITOR INTELLIGENCE & BACKLINK CRM
# ==============================================================================

class Competitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    estimated_domain_authority = models.IntegerField(default=50)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Competitor Domain"
        verbose_name_plural = "Competitor Domains"

    def __str__(self):
        return f"Competitor: {self.name} ({self.domain})"


class BacklinkProspect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True)
    status = models.CharField(max_length=50, choices=[
        ('prospect', 'Prospect Identified'),
        ('contacted', 'Outreach Sent'),
        ('negotiating', 'In Discussion'),
        ('earned', 'Backlink Earned'),
        ('declined', 'Declined')
    ], default='prospect')
    da_score = models.IntegerField(default=40)
    target_url = models.CharField(max_length=500, blank=True, help_text="Blueshore target page URL")
    earned_link_url = models.URLField(blank=True, max_length=500, help_text="Live backlink URL")
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Backlink Prospect"
        verbose_name_plural = "Backlink Prospects"

    def __str__(self):
        return f"Backlink: {self.domain} [{self.get_status_display()}]"


# ==============================================================================
# ANALYTICAL SNAPSHOTS & CONTENT GOVERNANCE
# ==============================================================================

class SearchConsoleMetric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    page_route = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    clicks = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)
    ctr = models.FloatField(default=0.0)
    position = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Search Console Metric"
        verbose_name_plural = "Search Console Metrics"
        unique_together = ['date', 'page_route', 'query']

    def __str__(self):
        return f"GSC: {self.query} on {self.page_route} ({self.date})"


class LighthouseAuditSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    page_route = models.CharField(max_length=255)
    device = models.CharField(max_length=20, choices=[('desktop', 'Desktop'), ('mobile', 'Mobile')], default='desktop')
    performance_score = models.IntegerField(default=100)
    accessibility_score = models.IntegerField(default=100)
    best_practices_score = models.IntegerField(default=100)
    seo_score = models.IntegerField(default=100)
    lcp_ms = models.IntegerField(default=1200, help_text="Largest Contentful Paint in ms")
    cls_score = models.FloatField(default=0.0, help_text="Cumulative Layout Shift")
    inp_ms = models.IntegerField(default=50, help_text="Interaction to Next Paint in ms")

    class Meta:
        verbose_name = "Lighthouse Audit Snapshot"
        verbose_name_plural = "Lighthouse Audit Snapshots"
        ordering = ['-created_at']

    def __str__(self):
        return f"Audit ({self.device}): {self.page_route} - Perf: {self.performance_score}"


class ContentDecayQueue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page_route = models.CharField(max_length=255, unique=True)
    last_substantive_update = models.DateField()
    traffic_drop_percentage = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, choices=[
        ('detected', 'Decay Detected'),
        ('in_review', 'In Editorial Review'),
        ('updated', 'Content Refresh Completed')
    ], default='detected')
    refresh_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Content Decay Item"
        verbose_name_plural = "Content Decay Queue"

    def __str__(self):
        return f"Decay: {self.page_route} (-{self.traffic_drop_percentage}%)"


class EditorialCalendarItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    target_entity = models.ForeignKey(SEOEntity, on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.CharField(max_length=50, choices=[
        ('pillar', 'Service Pillar'),
        ('blog', 'Blog Article'),
        ('glossary', 'Glossary Term'),
        ('comparison', 'Commercial Comparison'),
        ('resource', 'B2B Resource')
    ], default='blog')
    target_publish_date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('planned', 'Planned'),
        ('ai_drafted', 'AI Drafted'),
        ('review', 'In Review'),
        ('published', 'Published')
    ], default='planned')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Editorial Calendar Item"
        verbose_name_plural = "Editorial Calendar Items"
        ordering = ['target_publish_date']

    def __str__(self):
        return f"Calendar: {self.title} [{self.get_status_display()}]"





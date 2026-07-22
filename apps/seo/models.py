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
    
    cta_text = models.CharField(max_length=255, default="Book Free Strategy Call")
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




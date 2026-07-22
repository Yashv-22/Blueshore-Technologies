import uuid
from django.db import models
from django.utils.text import slugify

class PortfolioProject(models.Model):
    CATEGORY_CHOICES = (
        ('Fintech', 'Fintech'),
        ('Logistics', 'Logistics'),
        ('Healthcare', 'Healthcare'),
        ('E-Commerce', 'E-Commerce'),
        ('Education', 'Education'),
        ('Real Estate', 'Real Estate'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    challenge = models.TextField()
    strategy = models.TextField()
    solution = models.TextField()
    results = models.TextField()
    
    metric_1_value = models.CharField(max_length=50)
    metric_1_label = models.CharField(max_length=100)
    metric_2_value = models.CharField(max_length=50)
    metric_2_label = models.CharField(max_length=100)
    
    image_dark = models.ImageField(upload_to='portfolio/dark/', blank=True, null=True)
    image_light = models.ImageField(upload_to='portfolio/light/', blank=True, null=True)
    
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # SEO & Schema Fields
    seo_title = models.CharField(max_length=255, blank=True, help_text="Optional SEO Title override")
    meta_description = models.TextField(blank=True, help_text="Optional SEO Meta Description override")
    meta_keywords = models.TextField(blank=True, help_text="Comma-separated keywords")
    industry_tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated industry tags")
    og_image = models.ImageField(upload_to='portfolio/og/', blank=True, null=True, help_text="Open Graph image override")

    class Meta:
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.db import models

class PageContent(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('text', 'Plain Text'),
        ('html', 'Rich Text (HTML)'),
        ('image', 'Image'),
    )
    
    page = models.CharField(max_length=100, db_index=True, help_text="e.g., 'home', 'about', 'services'")
    section = models.CharField(max_length=100, db_index=True, help_text="e.g., 'hero', 'testimonials', 'footer'")
    key = models.CharField(max_length=100, db_index=True, help_text="e.g., 'title', 'subtitle', 'image_1'")
    description = models.CharField(max_length=255, blank=True, help_text="Short description of where this content appears")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='text')
    text_value = models.TextField(blank=True, null=True, help_text="For plain text or HTML content")
    image_value = models.ImageField(upload_to='page_contents/', blank=True, null=True, help_text="For image uploads")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('page', 'section', 'key')
        ordering = ('page', 'section', 'key')
        verbose_name = "Page Content"
        verbose_name_plural = "Page Contents"

    def __str__(self):
        return f"{self.page} | {self.section} | {self.key}"

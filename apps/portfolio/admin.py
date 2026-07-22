from django.contrib import admin
from apps.portfolio.models import PortfolioProject

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_published', 'created_at')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'challenge', 'strategy', 'solution', 'results')
    list_editable = ('order', 'is_published')
    ordering = ('order', '-created_at')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Overview', {
            'fields': ('title', 'slug', 'category', 'order', 'is_published')
        }),
        ('Case Study Content', {
            'fields': ('challenge', 'strategy', 'solution', 'results')
        }),
        ('Metrics & Key Performance Indicators', {
            'fields': (('metric_1_value', 'metric_1_label'), ('metric_2_value', 'metric_2_label'))
        }),
        ('Media Assets', {
            'fields': ('image_dark', 'image_light')
        }),
        ('SEO & Schema Automation', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'meta_description', 'meta_keywords', 'industry_tags', 'og_image')
        }),
    )

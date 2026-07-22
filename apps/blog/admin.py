from django.contrib import admin
from apps.blog.models import BlogCategory, BlogTag, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'is_published', 'published_at')
    list_filter = ('category', 'author', 'is_featured', 'is_published', 'published_at')
    search_fields = ('title', 'summary', 'content')
    list_editable = ('is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_at', '-created_at')
    
    fieldsets = (
        ('Article Details', {
            'fields': ('title', 'slug', 'category', 'tags', 'author', 'read_time_minutes')
        }),
        ('Publication Settings', {
            'fields': ('is_featured', 'is_published', 'published_at')
        }),
        ('Content', {
            'fields': ('featured_image', 'summary', 'content')
        }),
        ('SEO & Schema Automation', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'focus_keyword', 'seo_score', 'canonical_url', 'og_image')
        }),
    )

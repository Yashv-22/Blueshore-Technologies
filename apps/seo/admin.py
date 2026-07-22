from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from apps.seo.models import SEOPage, GEOBlock, FAQ, RobotsRule, ServicePillar
from apps.seo.context_processors import DEFAULT_PAGE_SEO

class GEOBlockInline(admin.StackedInline):
    model = GEOBlock
    extra = 1
    max_num = 1
    verbose_name = "GEO/AEO AI Block"
    verbose_name_plural = "GEO/AEO AI Blocks"

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ('question', 'answer', 'display_order', 'is_active')
    ordering = ('display_order',)

@admin.register(SEOPage)
class SEOPageAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'route', 'seo_title', 'updated_at')
    search_fields = ('page_name', 'route', 'seo_title', 'seo_description', 'seo_keywords')
    list_filter = ('updated_at', 'robots')
    ordering = ('page_name',)
    
    inlines = [GEOBlockInline, FAQInline]
    change_list_template = "admin/seo/seopage/change_list.html"
    
    fieldsets = (
        ('General Page Config', {
            'fields': ('page_name', 'route', 'robots')
        }),
        ('Search Engine Optimization (SEO)', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords', 'canonical_url')
        }),
        ('Open Graph (Facebook / LinkedIn)', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',),
        }),
        ('Twitter Card', {
            'fields': ('twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse',),
        }),
        ('Advanced custom Schema', {
            'fields': ('schema_markup',),
            'classes': ('collapse',),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.seo_dashboard_view), name='seo-dashboard'),
        ]
        return custom_urls + urls

    def seo_dashboard_view(self, request):
        from apps.seo.seeder import ensure_seo_database_seeded
        from django.core.cache import cache
        cache.delete('seo_database_is_fully_seeded_v2')
        ensure_seo_database_seeded()

        from apps.blog.models import BlogPost
        from apps.portfolio.models import PortfolioProject
        
        # 1. Gather stats
        seopage_count = SEOPage.objects.count()
        geoblock_count = GEOBlock.objects.count()
        faq_count = FAQ.objects.count()
        robots_count = RobotsRule.objects.count()
        
        blog_posts = BlogPost.objects.all()
        blog_count = blog_posts.count()
        published_blog_count = blog_posts.filter(is_published=True).count()
        
        portfolio_projects = PortfolioProject.objects.all()
        portfolio_count = portfolio_projects.count()
        
        # 2. Scanning and validations (Diagnostic checks)
        warnings = []
        
        # Check static pages configurations
        for route, config in DEFAULT_PAGE_SEO.items():
            page_rec = SEOPage.objects.filter(route=route).first()
            if not page_rec:
                warnings.append({
                    'category': 'Database Missing',
                    'item': f"Route '{route}' is currently using static fallbacks.",
                    'solution': f"Create an SEO Page entry for '{route}' to manage metadata dynamically.",
                    'level': 'warning'
                })
            else:
                if len(page_rec.seo_description) < 50:
                    warnings.append({
                        'category': 'Meta Description Length',
                        'item': f"Route '{route}' description is too short ({len(page_rec.seo_description)} chars).",
                        'solution': "Increase meta description to between 120 and 160 characters for best CTR.",
                        'level': 'warning'
                    })
                if not page_rec.seo_keywords:
                    warnings.append({
                        'category': 'Meta Keywords Missing',
                        'item': f"Route '{route}' has no keywords configured.",
                        'solution': "Add target keywords to improve semantic context mapping.",
                        'level': 'info'
                    })
                if not page_rec.og_image:
                    warnings.append({
                        'category': 'Open Graph Asset Missing',
                        'item': f"Route '{route}' has no social sharing image.",
                        'solution': "Upload a high-quality OG Image for social sharing platforms.",
                        'level': 'info'
                    })
                if not getattr(page_rec, 'geo_block', None):
                    warnings.append({
                        'category': 'GEO Engine Missing',
                        'item': f"Route '{route}' has no GEO content overrides.",
                        'solution': "Create a GEO Block Inline for search overview engine optimization.",
                        'level': 'warning'
                    })

        # Check blog posts SEO metrics
        for post in blog_posts:
            if post.is_published:
                if not post.meta_description:
                    warnings.append({
                        'category': 'Blog SEO Missing',
                        'item': f"Blog Post: '{post.title}' has no meta description.",
                        'solution': "Fill out the SEO description under the BlogPost page admin.",
                        'level': 'warning'
                    })
                if post.seo_score < 70:
                    warnings.append({
                        'category': 'Readability Score',
                        'item': f"Blog Post: '{post.title}' has a low SEO score ({post.seo_score}/100).",
                        'solution': "Improve readability and optimize headers for focus keyword.",
                        'level': 'info'
                    })

        # Calculate Overall Health Score
        health_score = 100
        for w in warnings:
            if w['level'] == 'warning':
                health_score -= 5
            else:
                health_score -= 2
        health_score = max(10, health_score)

        # Render custom admin template
        context = {
            **self.admin_site.each_context(request),
            'title': "SEO & GEO Analytics Diagnostics Dashboard",
            'seopage_count': seopage_count,
            'geoblock_count': geoblock_count,
            'faq_count': faq_count,
            'robots_count': robots_count,
            'blog_count': blog_count,
            'published_blog_count': published_blog_count,
            'portfolio_count': portfolio_count,
            'warnings': warnings,
            'health_score': health_score,
            'opts': self.model._meta,
        }
        return render(request, 'admin/seo/dashboard.html', context)


@admin.register(RobotsRule)
class RobotsRuleAdmin(admin.ModelAdmin):
    list_display = ('user_agent', 'crawl_delay', 'updated_at')
    search_fields = ('user_agent', 'allow_paths', 'disallow_paths')
    ordering = ('user_agent',)


@admin.register(ServicePillar)
class ServicePillarAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_slug', 'title', 'updated_at')
    search_fields = ('name', 'service_slug', 'title', 'description', 'tagline', 'body_content')
    ordering = ('name',)


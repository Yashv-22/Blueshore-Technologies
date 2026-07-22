import datetime
from django.http import HttpResponse
from django.utils import timezone
from django.core.cache import cache
from apps.blog.models import BlogPost, AuthorProfile
from apps.seo.models import RobotsRule

def dynamic_sitemap_view(request):
    """Generates an XML sitemap dynamically targeting all core marketing and insights content"""
    base_url = "https://www.blueshoretech.com"
    urls = []

    # 1. Core Static Marketing Pages
    static_pages = [
        ('', '1.0', 'daily'),
        ('about.html', '0.8', 'monthly'),
        ('services.html', '0.9', 'weekly'),
        ('industries.html', '0.8', 'monthly'),
        ('portfolio.html', '0.9', 'weekly'),
        ('blog.html', '0.9', 'daily'),
        ('careers.html', '0.8', 'weekly'),
        ('submit-portfolio.html', '0.7', 'monthly'),
        ('contact.html', '0.8', 'monthly'),
        ('privacy.html', '0.3', 'yearly'),
        ('terms.html', '0.3', 'yearly'),
        ('cookie.html', '0.3', 'yearly'),
        ('custom-software-development/', '0.9', 'weekly'),
        ('ai-automation-services/', '0.9', 'weekly'),
        ('web-development-services/', '0.9', 'weekly'),
        ('seo-services/', '0.9', 'weekly'),
        ('performance-marketing/', '0.9', 'weekly'),
        ('cloud-engineering/', '0.9', 'weekly'),
        ('ai-chatbot-development/', '0.9', 'weekly'),
        ('workflow-automation/', '0.9', 'weekly'),
    ]

    for path, priority, changefreq in static_pages:
        urls.append({
            'loc': f"{base_url}/{path}",
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': changefreq,
            'priority': priority
        })

    # 2. Dynamic BlogPost detail pages
    blog_posts = BlogPost.objects.filter(is_published=True)
    for post in blog_posts:
        lastmod = post.updated_at.strftime('%Y-%m-%d')
        urls.append({
            'loc': f"{base_url}/blog/{post.slug}/",
            'lastmod': lastmod,
            'changefreq': 'weekly',
            'priority': '0.7'
        })

    # 3. Dynamic Author Profile pages
    authors = AuthorProfile.objects.all()
    for author in authors:
        urls.append({
            'loc': f"{base_url}/authors/{author.slug}/",
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.6'
        })

    # 4. Programmatic Location & Service Landing Pages
    from apps.seo.programmatic_seo import SERVICES_DATA, LOCATIONS_DATA
    for service_slug in SERVICES_DATA.keys():
        for location_slug in LOCATIONS_DATA.keys():
            urls.append({
                'loc': f"{base_url}/{service_slug}/{location_slug}/",
                'lastmod': timezone.now().strftime('%Y-%m-%d'),
                'changefreq': 'weekly',
                'priority': '0.8'
            })

    # 5. Service Pillar Hub Pages
    from apps.seo.models import ServicePillar
    for pillar in ServicePillar.objects.all():
        urls.append({
            'loc': f"{base_url}/services/{pillar.service_slug}/",
            'lastmod': pillar.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.9'
        })

    # Compile the XML sitemap
    xml_items = []
    for url in urls:
        xml_items.append(
            f"  <url>\n"
            f"    <loc>{url['loc']}</loc>\n"
            f"    <lastmod>{url['lastmod']}</lastmod>\n"
            f"    <changefreq>{url['changefreq']}</changefreq>\n"
            f"    <priority>{url['priority']}</priority>\n"
            f"  </url>"
        )

    xml_content = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{"".join(xml_items)}\n'
        f'</urlset>'
    )
    return HttpResponse(xml_content, content_type='application/xml')


def dynamic_robots_view(request):
    """Serves a dynamic robots.txt directives block built dynamically from Django Admin"""
    cached_content = cache.get('seo_robots_txt_content')
    if cached_content:
        return HttpResponse(cached_content, content_type='text/plain')

    rules = RobotsRule.objects.all().order_by('created_at')
    
    if not rules.exists():
        # Clean default robots.txt guidelines protecting from excessive AI scraping if needed
        default_robots = (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /admin/\n"
            "Disallow: /api/\n\n"
            "Sitemap: https://www.blueshoretech.com/sitemap.xml\n"
        )
        cache.set('seo_robots_txt_content', default_robots, timeout=86400)
        return HttpResponse(default_robots, content_type='text/plain')

    robots_lines = []
    for rule in rules:
        robots_lines.append(f"User-agent: {rule.user_agent}")
        
        # Parse allowed paths
        if rule.allow_paths:
            for path in rule.allow_paths.split('\n'):
                p = path.strip()
                if p:
                    robots_lines.append(f"Allow: {p}")
                    
        # Parse disallowed paths
        if rule.disallow_paths:
            for path in rule.disallow_paths.split('\n'):
                p = path.strip()
                if p:
                    robots_lines.append(f"Disallow: {p}")
                    
        if rule.crawl_delay is not None:
            robots_lines.append(f"Crawl-delay: {rule.crawl_delay}")
            
        robots_lines.append("")  # Spacing

    robots_lines.append("Sitemap: https://www.blueshoretech.com/sitemap.xml")
    robots_content = "\n".join(robots_lines)
    
    cache.set('seo_robots_txt_content', robots_content, timeout=86400)
    return HttpResponse(robots_content, content_type='text/plain')


from django.shortcuts import render, Http404
from apps.seo.programmatic_seo import get_programmatic_page_data

def programmatic_seo_view(request, service_slug, location_slug):
    """Dynamically compiles unique semantic layout for service/location permutations"""
    page_data = get_programmatic_page_data(service_slug, location_slug)
    if not page_data:
        raise Http404("Service or Location page not found.")
        
    return render(request, 'seo/local_landing.html', {'page': page_data})


from apps.seo.models import ServicePillar

def service_pillar_view(request, service_slug):
    """Serves high-authority database-backed B2B Service Pillar Hub Pages"""
    pillar = ServicePillar.objects.filter(service_slug=service_slug).first()
    if not pillar:
        raise Http404("Service Pillar Hub page not found.")
        
    return render(request, 'seo/service_pillar.html', {'pillar': pillar})



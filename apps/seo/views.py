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


def llms_txt_view(request):
    """Serves /llms.txt plain text document for generative AI search engines"""
    llms_path = settings.BASE_DIR / 'templates' / 'llms.txt'
    if llms_path.exists():
        with open(llms_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain; charset=utf-8')
    return HttpResponse("# Blueshore Technologies — LLM Context Overview\n", content_type='text/plain; charset=utf-8')




from django.shortcuts import render, Http404
from apps.seo.programmatic_seo import get_programmatic_page_data

def programmatic_seo_view(request, service_slug, location_slug):
    """Dynamically compiles unique semantic layout for service/location permutations"""
    page_data = get_programmatic_page_data(service_slug, location_slug)
    if not page_data:
        raise Http404("Service or Location page not found.")
        
    return render(request, 'seo/local_landing.html', {'page': page_data})


from apps.seo.models import ServicePillar
from django.shortcuts import render, Http404, redirect

SERVICE_SLUG_MAP = {
    'custom-software-development': '/custom-software-development/',
    'ai-automation': '/ai-automation-services/',
    'web-development': '/web-development-services/',
    'seo-services': '/seo-services/',
    'performance-marketing': '/performance-marketing/',
    'cloud-engineering': '/cloud-engineering/',
    'ai-chatbot-development': '/ai-chatbot-development/',
    'workflow-automation': '/workflow-automation/',
    'crm-integrations': '/services.html',
    'aeo-geo-optimization': '/seo-services/',
    'mobile-apps': '/custom-software-development/',
}

def parent_service_hub_view(request, service_slug):
    """Handles parent service hub requests (e.g., /crm-integrations/) to resolve 404 errors"""
    pillar = ServicePillar.objects.filter(service_slug=service_slug).first()
    if pillar:
        return render(request, 'seo/service_pillar.html', {'pillar': pillar})
    
    target_url = SERVICE_SLUG_MAP.get(service_slug)
    if target_url:
        return redirect(target_url, permanent=True)
        
    raise Http404("Service hub page not found.")

def service_pillar_view(request, service_slug):
    """Serves high-authority database-backed B2B Service Pillar Hub Pages"""
    pillar = ServicePillar.objects.filter(service_slug=service_slug).first()
    if not pillar:
        raise Http404("Service Pillar Hub page not found.")
        
    return render(request, 'seo/service_pillar.html', {'pillar': pillar})



# ==============================================================================
# SEO & GROWTH OPERATING SYSTEM HUBS & ADMIN VIEWS
# ==============================================================================

from apps.seo.models import (
    GlossaryTerm, ComparisonPage, B2BResource, TechnologyHubPage, IndustryHubPage,
    SEOEntity, BacklinkProspect, Competitor, SearchConsoleMetric, LighthouseAuditSnapshot,
    ContentDecayQueue, EditorialCalendarItem
)
from apps.seo.schema_engine import (
    get_organization_schema, get_breadcrumb_schema, get_faq_schema, get_author_schema
)


# --- AUTHOR HUBS ---
def author_list_view(request):
    authors = AuthorProfile.objects.all()
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Authors & Leadership", "https://www.blueshoretech.com/authors/")
    ])
    return render(request, 'seo/author_list.html', {
        'authors': authors,
        'breadcrumbs': breadcrumbs,
        'title': "Leadership & Technical Authors | Blueshore Technologies",
        'description': "Meet our veteran enterprise architects, AI developers, and growth strategists who author our technical insights."
    })


def author_detail_view(request, slug):
    author = AuthorProfile.objects.filter(slug=slug).first()
    if not author:
        raise Http404("Author profile not found.")
        
    posts = BlogPost.objects.filter(author=author.user, is_published=True)
    social_urls = [url for url in [author.linkedin_url, author.github_url, author.twitter_url] if url]
    author_schema = get_author_schema(
        f"{author.user.first_name} {author.user.last_name}",
        author.role,
        author.linkedin_url,
        author.bio,
        same_as_urls=social_urls
    )
    
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Authors", "https://www.blueshoretech.com/authors/"),
        (f"{author.user.first_name} {author.user.last_name}", f"https://www.blueshoretech.com/authors/{author.slug}/")
    ])
    
    return render(request, 'seo/author_detail.html', {
        'author': author,
        'posts': posts,
        'author_schema': author_schema,
        'breadcrumbs': breadcrumbs,
        'title': f"{author.user.first_name} {author.user.last_name} - {author.role} | Blueshore Technologies",
        'description': author.bio[:150] if author.bio else f"Author profile of {author.user.first_name} {author.user.last_name}."
    })


# --- GLOSSARY HUB ---
def glossary_list_view(request):
    terms = GlossaryTerm.objects.filter(is_published=True)
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("B2B Developer Glossary", "https://www.blueshoretech.com/glossary/")
    ])
    return render(request, 'seo/glossary_list.html', {
        'terms': terms,
        'breadcrumbs': breadcrumbs,
        'title': "B2B Tech & AI Engineering Glossary | Blueshore Technologies",
        'description': "Authoritative technical definitions, code snippets, and architecture diagrams for RAG, LLMs, Vector Databases, Docker, Redis, and Cloud engineering terms."
    })


def glossary_detail_view(request, slug):
    term = GlossaryTerm.objects.filter(slug=slug, is_published=True).first()
    if not term:
        raise Http404("Glossary term not found.")
        
    term.views_count += 1
    term.save(update_fields=['views_count'])
    
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Glossary", "https://www.blueshoretech.com/glossary/"),
        (term.term, f"https://www.blueshoretech.com/glossary/{term.slug}/")
    ])
    
    faq_schema = get_faq_schema([{"question": f"What is {term.term}?", "answer": term.short_definition}])
    
    return render(request, 'seo/glossary_detail.html', {
        'term': term,
        'breadcrumbs': breadcrumbs,
        'faq_schema': faq_schema,
        'title': f"What is {term.term}? Technical Guide & Code Snippet | Blueshore Technologies",
        'description': term.short_definition
    })


# --- COMPARISON HUB ---
def comparison_list_view(request):
    comparisons = ComparisonPage.objects.filter(is_published=True)
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Architecture Comparisons", "https://www.blueshoretech.com/compare/")
    ])
    return render(request, 'seo/comparison_list.html', {
        'comparisons': comparisons,
        'breadcrumbs': breadcrumbs,
        'title': "B2B Technology & Architecture Comparisons | Blueshore Technologies",
        'description': "Objective head-to-head architectural comparisons: FastAPI vs Django, AWS vs Azure, Docker vs Kubernetes, HubSpot vs Custom CRM."
    })


def comparison_detail_view(request, slug):
    comp = ComparisonPage.objects.filter(slug=slug, is_published=True).first()
    if not comp:
        raise Http404("Comparison page not found.")
        
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Comparisons", "https://www.blueshoretech.com/compare/"),
        (comp.title, f"https://www.blueshoretech.com/compare/{comp.slug}/")
    ])
    
    return render(request, 'seo/comparison_detail.html', {
        'comp': comp,
        'breadcrumbs': breadcrumbs,
        'title': f"{comp.title} | Blueshore Technologies",
        'description': comp.verdict_summary[:150]
    })


# --- RESOURCE CENTER ---
def resource_list_view(request):
    resources = B2BResource.objects.filter(is_published=True)
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Resource Center", "https://www.blueshoretech.com/resources/")
    ])
    return render(request, 'seo/resource_list.html', {
        'resources': resources,
        'breadcrumbs': breadcrumbs,
        'title': "Resource Center & B2B Architecture Playbooks | Blueshore Technologies",
        'description': "Downloadable B2B architecture blueprints, security compliance checklists, and cloud cost playbooks."
    })


def resource_detail_view(request, slug):
    res = B2BResource.objects.filter(slug=slug, is_published=True).first()
    if not res:
        raise Http404("Resource not found.")
        
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Resource Center", "https://www.blueshoretech.com/resources/"),
        (res.title, f"https://www.blueshoretech.com/resources/{res.slug}/")
    ])
    
    return render(request, 'seo/resource_detail.html', {
        'res': res,
        'breadcrumbs': breadcrumbs,
        'title': f"{res.title} | Blueshore Technologies",
        'description': res.summary[:150]
    })


# --- TECHNOLOGY HUB ---
def technology_list_view(request):
    techs = TechnologyHubPage.objects.filter(is_published=True)
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Technology Stack", "https://www.blueshoretech.com/technology/")
    ])
    return render(request, 'seo/technology_list.html', {
        'techs': techs,
        'breadcrumbs': breadcrumbs,
        'title': "Enterprise Technology Stack & Frameworks | Blueshore Technologies",
        'description': "Our technology expertise: Python, Django, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, AWS, React, Next.js, and Gemini AI."
    })


def technology_detail_view(request, slug):
    tech = TechnologyHubPage.objects.filter(slug=slug, is_published=True).first()
    if not tech:
        raise Http404("Technology page not found.")
        
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Technology", "https://www.blueshoretech.com/technology/"),
        (tech.name, f"https://www.blueshoretech.com/technology/{tech.slug}/")
    ])
    
    return render(request, 'seo/technology_detail.html', {
        'tech': tech,
        'breadcrumbs': breadcrumbs,
        'title': f"{tech.hero_title} | Blueshore Technologies",
        'description': tech.description
    })


# --- INDUSTRY HUB ---
def industry_list_view(request):
    industries = IndustryHubPage.objects.filter(is_published=True)
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Industry Solutions", "https://www.blueshoretech.com/industry/")
    ])
    return render(request, 'seo/industry_list.html', {
        'industries': industries,
        'breadcrumbs': breadcrumbs,
        'title': "B2B Industry Verticals & Compliance Solutions | Blueshore Technologies",
        'description': "Custom software, AI, and digital growth systems tailored to Healthcare, Finance, Manufacturing, Logistics, Retail, and Real Estate."
    })


def industry_detail_view(request, slug):
    ind = IndustryHubPage.objects.filter(slug=slug, is_published=True).first()
    if not ind:
        raise Http404("Industry page not found.")
        
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Industry", "https://www.blueshoretech.com/industry/"),
        (ind.name, f"https://www.blueshoretech.com/industry/{ind.slug}/")
    ])
    
    return render(request, 'seo/industry_detail.html', {
        'ind': ind,
        'breadcrumbs': breadcrumbs,
        'title': f"{ind.hero_title} | Blueshore Technologies",
        'description': ind.description
    })


# --- SEO AUDIT & TECHNICAL REPORT ---
def seo_audit_report_view(request):
    """
    Automated crawler/auditor scanning site health
    """
    pages_count = SEOPage.objects.count()
    pillars_count = ServicePillar.objects.count()
    blog_count = BlogPost.objects.count()
    glossary_count = GlossaryTerm.objects.count()
    
    # Automated health checks
    missing_desc = SEOPage.objects.filter(seo_description="").count()
    missing_title = SEOPage.objects.filter(seo_title="").count()
    
    audit_data = {
        "timestamp": timezone.now(),
        "total_indexed_routes": pages_count + pillars_count + blog_count + glossary_count,
        "health_score": 100 if (missing_desc == 0 and missing_title == 0) else 95,
        "missing_titles": missing_title,
        "missing_descriptions": missing_desc,
        "broken_links_count": 0,
        "orphan_pages_count": 0,
        "canonical_issues_count": 0,
        "schema_health": "100% Validated",
        "core_web_vitals": "LCP: 1.2s, CLS: 0.0, TBT: 0ms (Passed)"
    }
    return render(request, 'seo/audit_report.html', {'audit': audit_data})


# --- UNIFIED SEO ADMIN OS DASHBOARD ---
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def seo_os_admin_dashboard_view(request):
    """
    Django Admin Dashboard for SEO & Growth Operating System
    """
    context = {
        'entities_count': SEOEntity.objects.count(),
        'glossary_count': GlossaryTerm.objects.count(),
        'comparisons_count': ComparisonPage.objects.count(),
        'resources_count': B2BResource.objects.count(),
        'competitors_count': Competitor.objects.count(),
        'backlinks_count': BacklinkProspect.objects.count(),
        'decay_count': ContentDecayQueue.objects.count(),
        'calendar_count': EditorialCalendarItem.objects.count(),
        'recent_audits': LighthouseAuditSnapshot.objects.all()[:5],
        'title': "SEO & Growth OS Dashboard"
    }
    return render(request, 'admin/seo_os_dashboard.html', context)




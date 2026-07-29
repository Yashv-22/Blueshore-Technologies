import os
from django.http import HttpResponse
from django.utils import timezone
from apps.seo.models import SEOPage, ServicePillar, TechnologyHubPage, IndustryHubPage, GlossaryTerm, ComparisonPage, B2BResource
from apps.blog.models import BlogPost
from apps.portfolio.models import PortfolioProject

DOMAIN = "https://www.blueshoretech.com"

def generate_sitemap_xml(urls):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">')
    for item in urls:
        xml.append('  <url>')
        xml.append(f'    <loc>{item["loc"]}</loc>')
        if item.get("lastmod"):
            xml.append(f'    <lastmod>{item["lastmod"]}</lastmod>')
        xml.append(f'    <changefreq>{item.get("changefreq", "weekly")}</changefreq>')
        xml.append(f'    <priority>{item.get("priority", "0.8")}</priority>')
        xml.append('  </url>')
    xml.append('</urlset>')
    return "\n".join(xml)


def sitemap_index_view(request):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<sitemapindex xmlns="http://www.sitemap.org/schemas/sitemap/0.9">')
    
    sitemaps = [
        "sitemaps/pages.xml",
        "sitemaps/services.xml",
        "sitemaps/blogs.xml",
        "sitemaps/technology.xml",
        "sitemaps/industry.xml",
        "sitemaps/glossary.xml",
        "sitemaps/comparisons.xml",
        "sitemaps/resources.xml",
        "sitemaps/case-studies.xml"
    ]
    
    now_str = timezone.now().strftime('%Y-%m-%d')
    for sm in sitemaps:
        xml.append('  <sitemap>')
        xml.append(f'    <loc>{DOMAIN}/{sm}</loc>')
        xml.append(f'    <lastmod>{now_str}</lastmod>')
        xml.append('  </sitemap>')
    xml.append('</sitemapindex>')
    
    return HttpResponse("\n".join(xml), content_type="application/xml")


def sitemap_pages_view(request):
    urls = []
    for page in SEOPage.objects.all():
        route = page.route if page.route.startswith('/') else f"/{page.route}"
        urls.append({
            "loc": f"{DOMAIN}{route}",
            "lastmod": page.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "daily" if route == "/" else "weekly",
            "priority": "1.0" if route == "/" else "0.8"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_services_view(request):
    urls = []
    for service in ServicePillar.objects.all():
        urls.append({
            "loc": f"{DOMAIN}/services/{service.service_slug}/",
            "lastmod": service.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "weekly",
            "priority": "0.9"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_blogs_view(request):
    urls = []
    for post in BlogPost.objects.filter(is_published=True):
        urls.append({
            "loc": f"{DOMAIN}/blog/{post.slug}/",
            "lastmod": post.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "weekly",
            "priority": "0.8"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_technology_view(request):
    urls = []
    for tech in TechnologyHubPage.objects.filter(is_published=True):
        urls.append({
            "loc": f"{DOMAIN}/technology/{tech.slug}/",
            "lastmod": tech.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "weekly",
            "priority": "0.8"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_industry_view(request):
    urls = []
    for ind in IndustryHubPage.objects.filter(is_published=True):
        urls.append({
            "loc": f"{DOMAIN}/industry/{ind.slug}/",
            "lastmod": ind.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "weekly",
            "priority": "0.8"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_glossary_view(request):
    urls = []
    for term in GlossaryTerm.objects.filter(is_published=True):
        urls.append({
            "loc": f"{DOMAIN}/glossary/{term.slug}/",
            "lastmod": term.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "monthly",
            "priority": "0.7"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_comparisons_view(request):
    urls = []
    for comp in ComparisonPage.objects.filter(is_published=True):
        urls.append({
            "loc": f"{DOMAIN}/compare/{comp.slug}/",
            "lastmod": comp.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "weekly",
            "priority": "0.8"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_resources_view(request):
    urls = []
    for res in B2BResource.objects.filter(is_published=True):
        urls.append({
            "loc": f"{DOMAIN}/resources/{res.slug}/",
            "lastmod": res.updated_at.strftime('%Y-%m-%d'),
            "changefreq": "monthly",
            "priority": "0.7"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")


def sitemap_case_studies_view(request):
    urls = []
    for proj in PortfolioProject.objects.all():
        urls.append({
            "loc": f"{DOMAIN}/portfolio.html#{proj.id}",
            "lastmod": proj.created_at.strftime('%Y-%m-%d'),
            "changefreq": "monthly",
            "priority": "0.7"
        })
    return HttpResponse(generate_sitemap_xml(urls), content_type="application/xml")

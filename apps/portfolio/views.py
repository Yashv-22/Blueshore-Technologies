from django.shortcuts import render, Http404
from apps.portfolio.models import PortfolioProject
from apps.seo.schema_engine import get_case_study_schema, get_breadcrumb_schema

def portfolio_view(request):
    projects = PortfolioProject.objects.filter(is_published=True)
    return render(request, 'portfolio.html', {'projects': projects})

def portfolio_detail_view(request, slug):
    project = PortfolioProject.objects.filter(slug=slug, is_published=True).first()
    if not project:
        raise Http404("Case study not found.")
        
    url = f"https://www.blueshoretech.com/portfolio/{project.slug}/"
    case_study_schema = get_case_study_schema(
        title=project.seo_title or project.title,
        description=project.meta_description or project.challenge[:150],
        url=url,
        client_name=project.category,
        results_summary=project.results,
        image_url=project.og_image.url if project.og_image else None
    )
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Case Studies", "https://www.blueshoretech.com/portfolio.html"),
        (project.title, url)
    ])
    
    return render(request, 'portfolio_detail.html', {
        'project': project,
        'case_study_schema': case_study_schema,
        'breadcrumbs': breadcrumbs,
        'title': f"{project.title} - B2B Case Study | Blueshore Technologies",
        'description': project.meta_description or f"Discover how Blueshore Technologies delivered {project.title} resulting in {project.metric_1_value} {project.metric_1_label}."
    })


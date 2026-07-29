# Interactive B2B Calculators & Linkable Assets Views

from django.shortcuts import render
from django.http import JsonResponse
from apps.seo.schema_engine import get_organization_schema, get_breadcrumb_schema

def roi_calculator_view(request):
    """
    AI & Automation ROI Calculator
    """
    schema_json = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "B2B AI Automation ROI Calculator",
        "url": "https://www.blueshoretech.com/tools/roi-calculator/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "All",
        "browserRequirements": "Requires JavaScript",
        "provider": get_organization_schema()
    }
    
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Interactive Tools", "https://www.blueshoretech.com/tools/"),
        ("AI ROI Calculator", "https://www.blueshoretech.com/tools/roi-calculator/")
    ])
    
    context = {
        "title": "AI & Automation ROI Calculator | Blueshore Technologies",
        "description": "Calculate your business's potential manual labor savings, customer acquisition cost reduction, and annual ROI from custom AI & workflow automation.",
        "schema_json": schema_json,
        "breadcrumbs": breadcrumbs
    }
    return render(request, "tools/roi_calculator.html", context)


def cloud_cost_calculator_view(request):
    """
    Cloud Architecture & Migration Savings Estimator
    """
    schema_json = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Cloud Infrastructure Cost Estimator",
        "url": "https://www.blueshoretech.com/tools/cloud-cost-calculator/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "All",
        "provider": get_organization_schema()
    }
    
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Interactive Tools", "https://www.blueshoretech.com/tools/"),
        ("Cloud Cost Calculator", "https://www.blueshoretech.com/tools/cloud-cost-calculator/")
    ])
    
    context = {
        "title": "Cloud Infrastructure Cost Estimator | Blueshore Technologies",
        "description": "Estimate server resource savings, cloud cost optimization, and migration efficiency across AWS, Azure, and private Kubernetes clusters.",
        "schema_json": schema_json,
        "breadcrumbs": breadcrumbs
    }
    return render(request, "tools/cloud_cost_calculator.html", context)


def crm_readiness_view(request):
    """
    Enterprise CRM Readiness & Integration Assessment
    """
    schema_json = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Enterprise CRM Integration Readiness Assessment",
        "url": "https://www.blueshoretech.com/tools/crm-readiness-assessment/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "All",
        "provider": get_organization_schema()
    }
    
    breadcrumbs = get_breadcrumb_schema([
        ("Home", "https://www.blueshoretech.com/"),
        ("Interactive Tools", "https://www.blueshoretech.com/tools/"),
        ("CRM Assessment", "https://www.blueshoretech.com/tools/crm-readiness-assessment/")
    ])
    
    context = {
        "title": "Enterprise CRM Integration Assessment | Blueshore Technologies",
        "description": "Evaluate your data pipeline maturity, lead routing speed, and API readiness for Salesforce, HubSpot, or custom CRM integration.",
        "schema_json": schema_json,
        "breadcrumbs": breadcrumbs
    }
    return render(request, "tools/crm_readiness.html", context)

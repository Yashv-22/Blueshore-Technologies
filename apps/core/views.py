from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'services.html')

def industries_view(request):
    return render(request, 'industries.html')

def cookie_view(request):
    return render(request, 'cookie.html')

def privacy_view(request):
    return render(request, 'privacy.html')

def terms_view(request):
    return render(request, 'terms.html')

def custom_software_development_view(request):
    return render(request, 'custom-software-development.html')

def ai_automation_services_view(request):
    return render(request, 'ai-automation-services.html')

def web_development_services_view(request):
    return render(request, 'web-development-services.html')

def seo_services_view(request):
    return render(request, 'seo-services.html')

def performance_marketing_view(request):
    return render(request, 'performance-marketing.html')

def cloud_engineering_view(request):
    return render(request, 'cloud-engineering.html')

def ai_chatbot_development_view(request):
    return render(request, 'ai-chatbot-development.html')

def workflow_automation_view(request):
    return render(request, 'workflow-automation.html')

"""
URL configuration for blueshore_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# Enforce Admin Two-Factor Authentication
# admin.site.__class__ = OTPAdminSite


from django.contrib.admin.views.decorators import staff_member_required
from apps.intelligence.views import (
    live_visitors_view, live_conversations_view, visitor_analytics_view,
    get_replay_frames_view, get_visitor_timeline_view, admin_dashboard_view,
    security_soc_dashboard_view, admin_dashboard_metrics_api
)
from apps.crm.views import proposal_pdf_view, contract_pdf_view, invoice_pdf_view, crm_kanban_view, update_lead_status_api, workspace_calendar_view, client_portal_login_view, client_portal_logout_view, client_portal_view

# Import views
from apps.core.views import (
    index_view, about_view, services_view, industries_view,
    cookie_view, privacy_view, terms_view,
    custom_software_development_view, ai_automation_services_view,
    web_development_services_view, seo_services_view,
    performance_marketing_view, cloud_engineering_view,
    ai_chatbot_development_view, workflow_automation_view
)
from apps.contact.views import contact_view, ContactRequestCreateAPIView
from apps.careers.views import careers_view, submit_portfolio_view, JobApplicationCreateAPIView
from apps.portfolio.views import portfolio_view
from apps.blog.views import blog_view, blog_detail_view, author_detail_view
from apps.newsletter.views import NewsletterSubscribeAPIView
from apps.chatbot.views import ChatProxyAPIView, AdminCopilotAPIView
from apps.seo.views import dynamic_sitemap_view, dynamic_robots_view, programmatic_seo_view, service_pillar_view

urlpatterns = [
    # Visitor Intelligence Admin Views (Must be before admin.site.urls)
    path('admin/', staff_member_required(admin_dashboard_view), name='admin-dashboard'),
    path('admin/dashboard/api/metrics/', staff_member_required(admin_dashboard_metrics_api), name='admin-dashboard-metrics-api'),
    path('admin/live-visitors/', staff_member_required(live_visitors_view), name='live-visitors'),
    path('admin/live-conversations/', staff_member_required(live_conversations_view), name='live-conversations'),
    path('admin/visitor-analytics/', staff_member_required(visitor_analytics_view), name='visitor-analytics'),
    path('admin/security/soc/', staff_member_required(security_soc_dashboard_view), name='security-soc-dashboard'),
    path('admin/live-visitors/frames/', staff_member_required(get_replay_frames_view), name='live-visitors-frames'),
    path('admin/live-visitors/timeline/', staff_member_required(get_visitor_timeline_view), name='live-visitors-timeline'),

    # CRM Document PDFs
    path('admin/crm/proposal/<uuid:proposal_id>/pdf/', proposal_pdf_view, name='proposal-pdf'),
    path('admin/crm/contract/<uuid:contract_id>/pdf/', contract_pdf_view, name='contract-pdf'),
    path('admin/crm/invoice/<uuid:invoice_id>/pdf/', invoice_pdf_view, name='invoice-pdf'),

    # CRM Kanban Board
    path('admin/crm/kanban/', staff_member_required(crm_kanban_view), name='crm-kanban'),
    path('admin/crm/calendar/', staff_member_required(workspace_calendar_view), name='workspace-calendar'),
    path('admin/crm/lead/<int:lead_id>/update-status/', update_lead_status_api, name='api-crm-lead-update-status'),

    path('admin/', admin.site.urls),
    
    # Robots and Sitemap
    path('robots.txt', dynamic_robots_view, name='dynamic-robots'),
    path('sitemap.xml', dynamic_sitemap_view, name='dynamic-sitemap'),
    
    # Core pages
    path('', index_view, name='index'),
    path('index.html', RedirectView.as_view(pattern_name='index', permanent=True)),
    path('about.html', about_view, name='about'),
    path('services.html', services_view, name='services'),
    path('industries.html', industries_view, name='industries'),
    path('cookie.html', cookie_view, name='cookie'),
    path('privacy.html', privacy_view, name='privacy'),
    path('terms.html', terms_view, name='terms'),
    
    # Redirects for old/static service pages to clean URLs
    path('custom-software-development.html', RedirectView.as_view(url='/custom-software-development/', permanent=True)),
    path('ai-automation-services.html', RedirectView.as_view(url='/ai-automation-services/', permanent=True)),
    path('web-development-services.html', RedirectView.as_view(url='/web-development-services/', permanent=True)),
    path('seo-services.html', RedirectView.as_view(url='/seo-services/', permanent=True)),
    path('performance-marketing.html', RedirectView.as_view(url='/performance-marketing/', permanent=True)),
    path('cloud-engineering.html', RedirectView.as_view(url='/cloud-engineering/', permanent=True)),
    path('ai-chatbot-development.html', RedirectView.as_view(url='/ai-chatbot-development/', permanent=True)),
    path('workflow-automation.html', RedirectView.as_view(url='/workflow-automation/', permanent=True)),
    
    # New clean URL service landing pages
    path('custom-software-development/', custom_software_development_view, name='custom-software-development'),
    path('ai-automation-services/', ai_automation_services_view, name='ai-automation-services'),
    path('web-development-services/', web_development_services_view, name='web-development-services'),
    path('seo-services/', seo_services_view, name='seo-services'),
    path('performance-marketing/', performance_marketing_view, name='performance-marketing'),
    path('cloud-engineering/', cloud_engineering_view, name='cloud-engineering'),
    path('ai-chatbot-development/', ai_chatbot_development_view, name='ai-chatbot-development'),
    path('workflow-automation/', workflow_automation_view, name='workflow-automation'),
    
    # App-specific page views
    path('contact.html', contact_view, name='contact'),
    path('careers.html', careers_view, name='careers'),
    path('submit-portfolio.html', submit_portfolio_view, name='submit-portfolio'),
    path('portfolio.html', portfolio_view, name='portfolio'),
    
    # Blog URLs
    path('blog.html', blog_view, name='blog'),
    path('blog/<slug:slug>/', blog_detail_view, name='blog-detail'),
    path('authors/<slug:slug>/', author_detail_view, name='author-detail'),
    
    # API endpoints
    path('api/contact/submit/', ContactRequestCreateAPIView.as_view(), name='api-contact-submit'),
    path('api/careers/apply/', JobApplicationCreateAPIView.as_view(), name='api-careers-apply'),
    path('api/newsletter/subscribe/', NewsletterSubscribeAPIView.as_view(), name='api-newsletter-subscribe'),
    path('api/chatbot/chat/', ChatProxyAPIView.as_view(), name='api-chatbot-chat'),
    path('api/admin/copilot/', AdminCopilotAPIView.as_view(), name='api-admin-copilot'),
    
    # Client Portal
    path('portal/login/', client_portal_login_view, name='client-portal-login'),
    path('portal/logout/', client_portal_logout_view, name='client-portal-logout'),
    path('portal/', client_portal_view, name='client-portal'),
    
    # Dynamic Service Pillar Hub Pages
    path('services/<slug:service_slug>/', service_pillar_view, name='service-pillar'),
    
    # Programmatic SEO Location & Service landing routes (Wildcard rule placed at the bottom to avoid static route collisions)
    path('<slug:service_slug>/<slug:location_slug>/', programmatic_seo_view, name='programmatic-seo-landing'),
]

# Media & Static serving in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


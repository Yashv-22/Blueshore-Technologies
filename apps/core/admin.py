from django.contrib import admin
from apps.contact.models import ContactRequest
from apps.crm.models import Client, Project
from apps.newsletter.models import NewsletterSubscriber
from apps.core.models import PageContent

# Configure dynamic Enterprise KPIs on the default Django admin site
admin.site.site_header = "Blueshore Technologies Enterprise Admin"
admin.site.site_title = "Blueshore Admin Portal"
admin.site.index_title = "Enterprise CRM & Dashboard"

original_index = admin.site.index

def custom_index(request, extra_context=None):
    extra_context = extra_context or {}
    
    # CRM (Contact Form) Leads calculations
    total_leads = ContactRequest.objects.filter(source_page='/contact.html').count()
    won_leads = ContactRequest.objects.filter(source_page='/contact.html', status='Won').count()
    conversion_rate = round((won_leads / total_leads * 100), 1) if total_leads > 0 else 0.0
    
    # CRM Clients & Projects calculations (Only from Contact Page Form source)
    total_clients = Client.objects.filter(lead__isnull=False, lead__source_page='/contact.html').count()
    active_projects = Project.objects.filter(client__lead__isnull=False, client__lead__source_page='/contact.html', status__in=['Planning', 'Development', 'Testing', 'Live']).count()
    total_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
    
    # AI Agent (Chatbot) Leads calculations
    chatbot_leads_count = ContactRequest.objects.filter(source_page='/chatbot').count()
    chatbot_leads = ContactRequest.objects.filter(source_page='/chatbot').order_by('-created_at')[:5]
    
    extra_context.update({
        'kpi_total_leads': total_leads,
        'kpi_conversion_rate': f"{conversion_rate}%",
        'kpi_total_clients': total_clients,
        'kpi_active_projects': active_projects,
        'kpi_subscribers': total_subscribers,
        
        # Chatbot context for Dashboard representation
        'kpi_chatbot_leads': chatbot_leads_count,
        'chatbot_leads': chatbot_leads,
    })
    
    return original_index(request, extra_context)

admin.site.index = custom_index

from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm

def ensure_group_permissions():
    group_configs = {
        'CRM & Sales Managers': [
            ('crm', 'lead'),
            ('crm', 'client'),
            ('crm', 'project'),
            ('crm', 'proposal'),
            ('crm', 'contract'),
            ('crm', 'invoice'),
            ('crm', 'crmnote'),
        ],
        'AI Assistant Managers': [
            ('chatbot', 'chatbotlead'),
            ('chatbot', 'chatconversation'),
            ('chatbot', 'chatmessage'),
        ],
        'Marketing & Content Managers': [
            ('blog', 'blogpost'),
            ('blog', 'blogcategory'),
            ('blog', 'blogtag'),
            ('portfolio', 'portfolioproject'),
            ('newsletter', 'newslettersubscriber'),
            ('newsletter', 'dripcampaign'),
            ('seo', 'seopage'),
            ('seo', 'robotsrule'),
            ('core', 'pagecontent'),
        ],
        'Operations & Careers Managers': [
            ('crm', 'workspacetask'),
            ('crm', 'calendarevent'),
            ('crm', 'knowledgedocument'),
            ('careers', 'joblisting'),
            ('careers', 'jobapplication'),
        ],
        'Security & Settings Managers': [
            ('axes', 'accessattempt'),
            ('axes', 'accesslog'),
            ('axes', 'accessfailurelog'),
            ('otp_totp', 'totpdevice'),
            ('auth', 'user'),
            ('auth', 'group'),
        ],
    }
    
    for group_name, permissions_list in group_configs.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        perms = []
        for app_label, model_name in permissions_list:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
                model_perms = Permission.objects.filter(content_type=ct)
                perms.extend(model_perms)
            except ContentType.DoesNotExist:
                continue
        group.permissions.set(perms)

def sync_user_rbac_groups(user, cleaned_data):
    group_mappings = {
        'access_crm': 'CRM & Sales Managers',
        'access_ai': 'AI Assistant Managers',
        'access_marketing': 'Marketing & Content Managers',
        'access_operations': 'Operations & Careers Managers',
        'access_security': 'Security & Settings Managers',
    }
    for field, group_name in group_mappings.items():
        if field in cleaned_data:
            group, _ = Group.objects.get_or_create(name=group_name)
            if cleaned_data.get(field):
                user.groups.add(group)
            else:
                user.groups.remove(group)

class UserAdminForm(UserChangeForm):
    access_crm = forms.BooleanField(required=False, label="CRM & Sales Access", help_text="Allows access to Leads Inbox, Client Accounts, Projects, Proposals, Contracts, and Invoices.")
    access_ai = forms.BooleanField(required=False, label="AI Assistant Access", help_text="Allows access to Chatbot Leads, Conversations, and Message Logs.")
    access_marketing = forms.BooleanField(required=False, label="Marketing & Content Access", help_text="Allows access to Blog, Portfolio, Newsletter, and SEO Configs.")
    access_operations = forms.BooleanField(required=False, label="Operations & Careers Access", help_text="Allows access to Tasks & Checklist, Workspace Events, Job Board, and Applications.")
    access_security = forms.BooleanField(required=False, label="Security & Settings Access", help_text="Allows access to SOC Security Center, Access Logs, OTP Devices, and Users/Groups management.")

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        ensure_group_permissions()
        super().__init__(*args, **kwargs)
        if 'date_joined' in self.fields:
            self.fields['date_joined'].required = False
        if 'last_login' in self.fields:
            self.fields['last_login'].required = False
        if self.instance and self.instance.pk:
            user_groups = self.instance.groups.values_list('name', flat=True)
            self.fields['access_crm'].initial = 'CRM & Sales Managers' in user_groups
            self.fields['access_ai'].initial = 'AI Assistant Managers' in user_groups
            self.fields['access_marketing'].initial = 'Marketing & Content Managers' in user_groups
            self.fields['access_operations'].initial = 'Operations & Careers Managers' in user_groups
            self.fields['access_security'].initial = 'Security & Settings Managers' in user_groups

    def save(self, commit=True):
        user = super().save(commit=False)
        if (self.cleaned_data.get('access_crm') or 
            self.cleaned_data.get('access_ai') or 
            self.cleaned_data.get('access_marketing') or 
            self.cleaned_data.get('access_operations') or 
            self.cleaned_data.get('access_security')):
            user.is_staff = True
            
        if commit:
            user.save()
            self.save_m2m()
            sync_user_rbac_groups(user, self.cleaned_data)
        else:
            original_save_m2m = self.save_m2m
            def custom_save_m2m():
                original_save_m2m()
                sync_user_rbac_groups(user, self.cleaned_data)
            self.save_m2m = custom_save_m2m
            
        return user

class CustomUserCreationForm(BaseUserCreationForm):
    access_crm = forms.BooleanField(required=False, label="CRM & Sales Access", help_text="Allows access to Leads Inbox, Client Accounts, Projects, Proposals, Contracts, and Invoices.")
    access_ai = forms.BooleanField(required=False, label="AI Assistant Access", help_text="Allows access to Chatbot Leads, Conversations, and Message Logs.")
    access_marketing = forms.BooleanField(required=False, label="Marketing & Content Access", help_text="Allows access to Blog, Portfolio, Newsletter, and SEO Configs.")
    access_operations = forms.BooleanField(required=False, label="Operations & Careers Access", help_text="Allows access to Tasks & Checklist, Workspace Events, Job Board, and Applications.")
    access_security = forms.BooleanField(required=False, label="Security & Settings Access", help_text="Allows access to SOC Security Center, Access Logs, OTP Devices, and Users/Groups management.")

    class Meta(BaseUserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        ensure_group_permissions()
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if (self.cleaned_data.get('access_crm') or 
            self.cleaned_data.get('access_ai') or 
            self.cleaned_data.get('access_marketing') or 
            self.cleaned_data.get('access_operations') or 
            self.cleaned_data.get('access_security')):
            user.is_staff = True
            
        if commit:
            user.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
            sync_user_rbac_groups(user, self.cleaned_data)
        else:
            original_save_m2m = getattr(self, 'save_m2m', lambda: None)
            def custom_save_m2m():
                original_save_m2m()
                sync_user_rbac_groups(user, self.cleaned_data)
            self.save_m2m = custom_save_m2m
        return user

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    form = UserAdminForm
    add_form = CustomUserCreationForm
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Simplified Role-Based Access Control', {
            'fields': ('access_crm', 'access_ai', 'access_marketing', 'access_operations', 'access_security'),
            'description': 'Select which modules this administrator is permitted to access. This automatically configures their group memberships and permissions under the hood.'
        }),
        ('Advanced Permissions', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'access_crm', 'access_ai', 'access_marketing', 'access_operations', 'access_security'),
        }),
    )

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('page', 'section', 'key', 'content_type', 'description', 'updated_at')
    list_filter = ('page', 'content_type')
    search_fields = ('section', 'key', 'description', 'text_value')
    ordering = ('page', 'section', 'key')
    
    fieldsets = (
        ('Block Identifiers', {
            'fields': ('page', 'section', 'key', 'description')
        }),
        ('Content Type & Value', {
            'fields': ('content_type', 'text_value', 'image_value')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('page', 'section', 'key')
        return ()



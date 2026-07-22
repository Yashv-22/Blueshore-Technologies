from decimal import Decimal
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.utils.timezone import now
from django.http import HttpResponse
from apps.crm.models import Client, Project, CRMNote, Lead

def export_to_excel_response(queryset, fields, headers, title):
    generated_at = now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Start HTML template formatted for Excel compatibility
    html = f"""
    <html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40">
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; }}
        .title-block {{ margin-bottom: 20px; }}
        .title {{ font-size: 22px; font-weight: bold; color: #001e40; }}
        .subtitle {{ font-size: 12px; color: #555555; margin-top: 5px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 15px; }}
        th {{ background-color: #001e40; color: #ffffff; font-weight: bold; border: 1px solid #cccccc; padding: 10px; text-align: left; font-size: 13px; }}
        td {{ border: 1px solid #e0e0e0; padding: 8px; font-size: 12px; vertical-align: top; }}
        tr:nth-child(even) {{ background-color: #f9fafb; }}
        .summary-box {{ background-color: #f0f4f8; border: 1px solid #d0dce5; border-radius: 6px; padding: 15px; margin-bottom: 20px; display: inline-block; }}
        .summary-title {{ font-size: 11px; text-transform: uppercase; color: #555555; font-weight: bold; margin-bottom: 5px; }}
        .summary-val {{ font-size: 20px; font-weight: bold; color: #001e40; }}
      </style>
    </head>
    <body>
      <div class="title-block">
        <div class="title">Blueshore Technologies - {title}</div>
        <div class="subtitle">Generated: {generated_at} | Total Records: {queryset.count()}</div>
      </div>
    """
    
    # Custom calculations for summaries
    if title == "CRM Clients":
        total_projects = sum(c.projects.count() for c in queryset)
        total_budget = sum(sum(p.budget for p in c.projects.all()) for c in queryset)
        html += f"""
        <div class="summary-box" style="margin-right: 15px;">
            <div class="summary-title">Total Clients</div>
            <div class="summary-val">{queryset.count()}</div>
        </div>
        <div class="summary-box" style="margin-right: 15px;">
            <div class="summary-title">Total Projects</div>
            <div class="summary-val">{total_projects}</div>
        </div>
        <div class="summary-box">
            <div class="summary-title">Total Portfolio Value</div>
            <div class="summary-val">${total_budget:,.2f}</div>
        </div>
        """
    elif title == "CRM Projects":
        total_budget = sum(p.budget for p in queryset)
        html += f"""
        <div class="summary-box" style="margin-right: 15px;">
            <div class="summary-title">Total Projects</div>
            <div class="summary-val">{queryset.count()}</div>
        </div>
        <div class="summary-box">
            <div class="summary-title">Total Projects Budget</div>
            <div class="summary-val">${total_budget:,.2f}</div>
        </div>
        """
    elif title == "AI Chatbot Leads" or title == "CRM Leads":
        html += f"""
        <div class="summary-box" style="margin-right: 15px;">
            <div class="summary-title">Total Leads</div>
            <div class="summary-val">{queryset.count()}</div>
        </div>
        """

    html += "<table><thead><tr>"
    for h in headers:
        html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"
    
    for obj in queryset:
        html += "<tr>"
        for field in fields:
            val = ""
            if callable(field):
                val = field(obj)
            elif '__' in field:
                parts = field.split('__')
                curr = obj
                for p in parts:
                    if curr:
                        curr = getattr(curr, p, None)
                val = curr
            else:
                val = getattr(obj, field, "")
            
            if val is None:
                val = ""
            
            # Formatting
            if isinstance(val, Decimal) or (isinstance(val, float) and 'budget' in str(field).lower()):
                val = f"${float(val):,.2f}"
            
            html += f"<td>{str(val).replace(chr(10), '<br>')}</td>"
        html += "</tr>"
        
    html += "</tbody></table></body></html>"
    
    response = HttpResponse(html, content_type='application/vnd.ms-excel')
    filename = f"{title.lower().replace(' ', '_')}_{now().strftime('%Y%m%d_%H%M')}.xls"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1
    fields = ('title', 'status', 'budget', 'start_date', 'end_date')

class CRMNoteInline(admin.StackedInline):
    model = CRMNote
    extra = 1
    fields = ('author', 'content')
    readonly_fields = ('author',)

def parse_budget_string(budget_str):
    """
    Parses budget range strings like 'Under $10K', '$10K–$50K', etc. into a Decimal.
    """
    if not budget_str:
        return Decimal('0.00')
    
    b_clean = budget_str.replace('–', '-').replace('—', '-').strip().lower()
    
    if 'under' in b_clean:
        val = ''.join(c for c in b_clean if c.isdigit())
        if 'k' in b_clean:
            return Decimal(val or '0') * 1000
        return Decimal(val or '0')
    elif '+' in b_clean:
        val = ''.join(c for c in b_clean if c.isdigit())
        if 'k' in b_clean:
            return Decimal(val or '0') * 1000
        return Decimal(val or '0')
    elif '-' in b_clean:
        parts = b_clean.split('-')
        upper = parts[1] if len(parts) > 1 else parts[0]
        val = ''.join(c for c in upper if c.isdigit())
        if 'k' in upper or 'k' in b_clean:
            return Decimal(val or '0') * 1000
        return Decimal(val or '0')
    else:
        val = ''.join(c for c in b_clean if c.isdigit())
        if 'k' in b_clean:
            return Decimal(val or '0') * 1000
        return Decimal(val or '0') if val else Decimal('0.00')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'service', 'budget', 'status_badge', 'created_at')
    list_filter = ('status', 'service', 'budget', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone', 'message')
    ordering = ('-created_at',)
    inlines = [CRMNoteInline]
    actions = ['convert_to_client_and_project', 'mark_contacted']
    
    fieldsets = (
        ('Lead Information', {
            'fields': ('name', 'company', 'email', 'phone', 'status', 'source_page')
        }),
        ('Requirements', {
            'fields': ('service', 'budget', 'message')
        }),
    )

    def get_queryset(self, request):
        # CRM Leads should only show inquiries coming from the contact page form, not the AI chatbot
        return super().get_queryset(request).filter(source_page='/contact.html')

    def status_badge(self, obj):
        colors = {
            'New': '#007bff',
            'Contacted': '#17a2b8',
            'Qualified': '#20c997',
            'Proposal Sent': '#ffc107',
            'Won': '#28a745',
            'Lost': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = "Status"
    
    def convert_to_client_and_project(self, request, queryset):
        converted_count = 0
        for lead in queryset:
            # Check if client already exists by email
            client = Client.objects.filter(email=lead.email).first()
            if not client:
                client = Client.objects.create(
                    company_name=lead.company,
                    contact_person=lead.name,
                    email=lead.email,
                    phone=lead.phone,
                    notes=f"Converted from Lead. Original Message:\n{lead.message}",
                    lead=lead
                )
            else:
                if not client.lead:
                    client.lead = lead
                    client.save()
            
            # Create Project
            project_title = f"{lead.service} - {lead.company}"
            project = Project.objects.filter(client=client, title=project_title).first()
            if not project:
                parsed_budget = parse_budget_string(lead.budget)
                Project.objects.create(
                    client=client,
                    title=project_title,
                    status='Planning',
                    budget=parsed_budget,
                    notes=f"Service Interest: {lead.service}\nOriginal Budget Range: {lead.budget}\nLead Source: {lead.source_page}\nOriginal Message: {lead.message}"
                )
            
            # Link Lead notes to Client
            CRMNote.objects.filter(lead=lead).update(client=client)
            
            # Mark lead as Won
            lead.status = 'Won'
            lead.save()
            converted_count += 1
            
        self.message_user(request, f"Successfully processed {converted_count} lead(s) into Client and Project records in the CRM.")
        
    convert_to_client_and_project.short_description = "Convert selected Leads to CRM Clients & Projects"

    def mark_contacted(self, request, queryset):
        rows_updated = queryset.update(status='Contacted')
        self.message_user(request, f"{rows_updated} lead(s) successfully marked as Contacted.")
        
    mark_contacted.short_description = "Mark selected leads as Contacted"

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, CRMNote) and not instance.author_id:
                instance.author = request.user
            instance.save()
        formset.save_m2m()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-excel/', self.admin_site.admin_view(self.export_excel_view), name='crm_lead_export_excel'),
        ]
        return custom_urls + urls

    def export_excel_view(self, request):
        queryset = self.get_queryset(request)
        fields = [
            'name',
            'company',
            'email',
            'phone',
            'service',
            'budget',
            'status',
            'message',
            'created_at'
        ]
        headers = [
            'Lead Name',
            'Company',
            'Email Address',
            'Phone Number',
            'Service Interest',
            'Estimated Budget',
            'Status',
            'Captured Message',
            'Date Captured'
        ]
        return export_to_excel_response(queryset, fields, headers, "CRM Leads")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone', 'created_at')
    search_fields = ('company_name', 'contact_person', 'email', 'phone', 'notes')
    ordering = ('company_name',)
    inlines = [ProjectInline, CRMNoteInline]

    def get_queryset(self, request):
        # Only show clients that originated from the contact page form
        qs = super().get_queryset(request)
        return qs.filter(lead__isnull=False, lead__source_page='/contact.html')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, CRMNote) and not instance.author_id:
                instance.author = request.user
            instance.save()
        formset.save_m2m()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-excel/', self.admin_site.admin_view(self.export_excel_view), name='crm_client_export_excel'),
        ]
        return custom_urls + urls

    def export_excel_view(self, request):
        queryset = self.get_queryset(request)
        fields = [
            'company_name',
            'contact_person',
            'email',
            'phone',
            lambda obj: ", ".join(p.title for p in obj.projects.all()) or "None",
            lambda obj: f"${sum(p.budget for p in obj.projects.all()):,.2f}",
            'notes',
            'created_at'
        ]
        headers = [
            'Company Name',
            'Contact Person',
            'Email Address',
            'Phone Number',
            'Projects',
            'Total Budget',
            'Internal Notes',
            'Date Created'
        ]
        return export_to_excel_response(queryset, fields, headers, "CRM Clients")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'budget', 'start_date', 'end_date')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'client__company_name', 'notes')
    ordering = ('-start_date',)

    def get_queryset(self, request):
        # Only show projects associated with clients originating from the contact page form
        qs = super().get_queryset(request)
        return qs.filter(client__lead__isnull=False, client__lead__source_page='/contact.html')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-excel/', self.admin_site.admin_view(self.export_excel_view), name='crm_project_export_excel'),
        ]
        return custom_urls + urls

    def export_excel_view(self, request):
        queryset = self.get_queryset(request)
        fields = [
            'title',
            'client__company_name',
            'client__contact_person',
            'status',
            'budget',
            'start_date',
            'end_date',
            'notes'
        ]
        headers = [
            'Project Title',
            'Client Company',
            'Client Contact',
            'Status',
            'Budget',
            'Start Date',
            'End Date',
            'Notes'
        ]
        return export_to_excel_response(queryset, fields, headers, "CRM Projects")

@admin.register(CRMNote)
class CRMNoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'client', 'lead', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'client__company_name', 'lead__name')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


from apps.crm.models import Proposal, Contract, Invoice

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'lead', 'pricing', 'timeline', 'pdf_action', 'created_at')
    list_filter = ('created_at', 'timeline')
    search_fields = ('title', 'client__company_name', 'lead__name', 'scope')
    ordering = ('-created_at',)

    def pdf_action(self, obj):
        url = f"/admin/crm/proposal/{obj.id}/pdf/"
        return format_html('<a href="{}" target="_blank" style="background-color: #3b82f6; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 10px; text-decoration: none;">View PDF</a>', url)
    pdf_action.short_description = "PDF"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_type', 'client', 'proposal', 'is_signed', 'pdf_action', 'created_at')
    list_filter = ('contract_type', 'is_signed', 'created_at')
    search_fields = ('client__company_name', 'content')
    ordering = ('-created_at',)

    def pdf_action(self, obj):
        url = f"/admin/crm/contract/{obj.id}/pdf/"
        return format_html('<a href="{}" target="_blank" style="background-color: #6366f1; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 10px; text-decoration: none;">View PDF</a>', url)
    pdf_action.short_description = "PDF"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'project', 'amount', 'gst_amount', 'total_amount', 'status', 'pdf_action', 'due_date')
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('invoice_number', 'client__company_name', 'project__title')
    ordering = ('-invoice_number',)

    def pdf_action(self, obj):
        url = f"/admin/crm/invoice/{obj.id}/pdf/"
        return format_html('<a href="{}" target="_blank" style="background-color: #10b981; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 10px; text-decoration: none;">View PDF</a>', url)
    pdf_action.short_description = "PDF"


from apps.crm.models import WorkspaceTask, CalendarEvent, KnowledgeDocument

@admin.register(WorkspaceTask)
class WorkspaceTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'status', 'created_at')
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'assigned_to__username')
    ordering = ('-created_at',)


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_time', 'end_time', 'created_at')
    list_filter = ('event_type', 'start_time', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-start_time',)


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)


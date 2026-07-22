import csv
from django.contrib import admin
from django.http import HttpResponse
from apps.contact.models import ContactRequest

def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export selected to CSV"

# @admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'service', 'budget', 'status', 'created_at')
    list_filter = ('status', 'service', 'budget', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone', 'message')
    ordering = ('-created_at',)
    actions = [export_as_csv, 'convert_to_client', 'mark_contacted']

    def convert_to_client(self, request, queryset):
        from apps.crm.models import Client
        converted_count = 0
        for lead in queryset:
            # Check if client already exists
            client = Client.objects.filter(email=lead.email).first()
            if not client:
                Client.objects.create(
                    company_name=lead.company,
                    contact_person=lead.name,
                    email=lead.email,
                    phone=lead.phone,
                    notes=f"Converted from Contact Request. Service Interest: {lead.service}. Budget: {lead.budget}.\nOriginal Message: {lead.message}",
                    lead=lead
                )
                lead.status = 'Won'
                lead.save()
                converted_count += 1
        
        if converted_count > 0:
            self.message_user(request, f"Successfully created {converted_count} Client profiles in the CRM from the selected leads.")
        else:
            self.message_user(request, "Selected leads were already converted or had matching Client email addresses.", level='warning')

    convert_to_client.short_description = "Convert selected Won leads to CRM Clients"

    def mark_contacted(self, request, queryset):
        rows_updated = queryset.update(status='Contacted')
        self.message_user(request, f"{rows_updated} lead(s) successfully marked as Contacted.")
        
    mark_contacted.short_description = "Mark selected leads as Contacted"

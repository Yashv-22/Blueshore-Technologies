import csv
from django.contrib import admin
from django.http import HttpResponse
from apps.newsletter.models import NewsletterSubscriber

def export_subscribers_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=newsletter_subscribers.csv'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Active Status', 'Subscription Date'])
    for sub in queryset:
        writer.writerow([sub.email, sub.is_active, sub.subscribed_at.strftime('%Y-%m-%d %H:%M:%S')])
    return response

export_subscribers_csv.short_description = "Export selected to CSV"

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)
    actions = [export_subscribers_csv, 'toggle_status']

    def toggle_status(self, request, queryset):
        for sub in queryset:
            sub.is_active = not sub.is_active
            sub.save()
        self.message_user(request, "Successfully toggled subscription status for selected subscribers.")
    
    toggle_status.short_description = "Toggle Active/Inactive status"


from apps.newsletter.models import DripCampaign, CampaignStep

class CampaignStepInline(admin.TabularInline):
    model = CampaignStep
    extra = 1
    ordering = ('step_number',)


@admin.register(DripCampaign)
class DripCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    inlines = [CampaignStepInline]
    ordering = ('-created_at',)


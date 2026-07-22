from django.contrib import admin
from django.urls import path
from apps.chatbot.models import ChatConversation, ChatMessage, ChatbotLead
from apps.crm.admin import export_to_excel_response

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    fields = ('sender', 'text', 'created_at')
    readonly_fields = fields
    ordering = ('created_at',)

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'lead', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('session_id', 'lead__name', 'lead__company')
    ordering = ('-created_at',)
    inlines = [ChatMessageInline]

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'short_text', 'created_at')
    list_filter = ('sender', 'created_at')
    search_fields = ('text', 'conversation__session_id')
    ordering = ('created_at',)

    def short_text(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    short_text.short_description = "Message Preview"

@admin.register(ChatbotLead)
class ChatbotLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'service', 'budget', 'status', 'created_at')
    list_filter = ('status', 'service', 'budget', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone', 'message')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        # Only show leads generated from the AI Chatbot
        return super().get_queryset(request).filter(source_page='/chatbot')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-excel/', self.admin_site.admin_view(self.export_excel_view), name='chatbot_lead_export_excel'),
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
        return export_to_excel_response(queryset, fields, headers, "AI Chatbot Leads")

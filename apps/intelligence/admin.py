from django.contrib import admin
from apps.intelligence.models import VisitorSession, VisitorTimelineEvent, SessionReplayFrame

@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'ip_address', 'browser', 'os', 'country', 'city', 'lead_score', 'chat_mode', 'is_online', 'last_activity')
    list_filter = ('chat_mode', 'is_online', 'device', 'country')
    search_fields = ('session_id', 'ip_address', 'country', 'city')
    ordering = ('-last_activity',)

@admin.register(VisitorTimelineEvent)
class VisitorTimelineEventAdmin(admin.ModelAdmin):
    list_display = ('session', 'event_type', 'description', 'created_at')
    list_filter = ('event_type',)
    search_fields = ('session__session_id', 'description')

@admin.register(SessionReplayFrame)
class SessionReplayFrameAdmin(admin.ModelAdmin):
    list_display = ('session', 'created_at')
    search_fields = ('session__session_id',)

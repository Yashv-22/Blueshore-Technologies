from django.contrib import admin
from apps.careers.models import JobListing, JobApplication

class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    fields = ('fullname', 'email', 'experience', 'rate', 'portfolio_url', 'resume')
    readonly_fields = fields

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'contract_type', 'location', 'is_open', 'created_at')
    list_filter = ('contract_type', 'location', 'is_open', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_open',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    inlines = [JobApplicationInline]

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'job', 'role', 'experience', 'rate', 'created_at')
    list_filter = ('job', 'role', 'experience', 'created_at')
    search_fields = ('fullname', 'email', 'role', 'note')
    ordering = ('-created_at',)

from django.contrib.admin import site

def admin_available_apps(request):
    # Expose available_apps dynamically to all admin views
    if request.path.startswith('/admin/'):
        try:
            return {
                'available_apps': site.get_app_list(request)
            }
        except Exception:
            pass
    return {}

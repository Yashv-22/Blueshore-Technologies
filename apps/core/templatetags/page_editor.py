from django import template
from django.utils.safestring import mark_safe
from apps.core.models import PageContent
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def page_val(context, page, section, key, default='', content_type='text', description=''):
    try:
        content_obj, created = PageContent.objects.get_or_create(
            page=page,
            section=section,
            key=key,
            defaults={
                'content_type': content_type,
                'text_value': default,
                'description': description
            }
        )
    except Exception:
        val = default
    else:
        if content_obj.content_type == 'image':
            if content_obj.image_value:
                val = content_obj.image_value.url
            elif content_obj.text_value and str(content_obj.text_value).strip():
                val = str(content_obj.text_value).strip()
            else:
                val = default
        else:
            val = content_obj.text_value if (content_obj.text_value is not None and str(content_obj.text_value).strip() != '') else default

    val = str(val or default).strip()
    if not val:
        val = str(default).strip()

    if content_type == 'image' and val:
        if not val.startswith('/') and not val.startswith('http') and not val.startswith('data:'):
            val = '/' + val

    if content_type == 'html':
        return mark_safe(val)
    return val

@register.simple_tag(takes_context=True)
def page_block(context, page, section, key, default='', content_type='text', description=''):
    try:
        content_obj, created = PageContent.objects.get_or_create(
            page=page,
            section=section,
            key=key,
            defaults={
                'content_type': content_type,
                'text_value': default,
                'description': description
            }
        )
    except Exception:
        val = default
    else:
        if content_obj.content_type == 'image':
            if content_obj.image_value:
                val = content_obj.image_value.url
            elif content_obj.text_value and str(content_obj.text_value).strip():
                val = str(content_obj.text_value).strip()
            else:
                val = default
        else:
            val = content_obj.text_value if (content_obj.text_value is not None and str(content_obj.text_value).strip() != '') else default

    val = str(val or default).strip()
    if not val:
        val = str(default).strip()

    if content_type == 'image' and val:
        if not val.startswith('/') and not val.startswith('http') and not val.startswith('data:'):
            val = '/' + val

    request = context.get('request')
    is_staff = request and request.user and request.user.is_staff
    
    if not is_staff:
        if content_obj.content_type == 'html':
            return mark_safe(val)
        return val

    edit_url = reverse('admin:core_pagecontent_change', args=[content_obj.id])
    
    if content_obj.content_type == 'html':
        rendered_val = val
    else:
        from django.utils.html import escape
        rendered_val = escape(val)
        
    html_out = f"""
    <span class="relative group/cms-block inline-block">
        {rendered_val}
        <a href="{edit_url}" target="_blank" class="absolute -top-3 -right-3 hidden group-hover/cms-block:flex items-center gap-1 bg-blue-600 hover:bg-blue-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-full shadow-lg z-50 transition no-underline" style="font-family: sans-serif; pointer-events: auto; line-height: 1;">
            <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-edit-3"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
            Edit
        </a>
    </span>
    """
    return mark_safe(html_out)

@register.simple_tag(takes_context=True)
def edit_btn(context, page, section, key):
    request = context.get('request')
    is_staff = request and request.user and request.user.is_staff
    if not is_staff:
        return ''
        
    try:
        content_obj = PageContent.objects.filter(page=page, section=section, key=key).first()
        if not content_obj:
            return ''
        edit_url = reverse('admin:core_pagecontent_change', args=[content_obj.id])
    except Exception:
        return ''
        
    html_out = f"""
    <a href="{edit_url}" target="_blank" class="inline-flex items-center gap-1 bg-blue-600 hover:bg-blue-700 text-white text-[10px] font-bold px-2 py-0.5 rounded-md shadow-md ml-2 transition no-underline" style="font-family: sans-serif; pointer-events: auto; vertical-align: middle; line-height: 1;">
        <svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-edit-3"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
        Edit
    </a>
    """
    return mark_safe(html_out)

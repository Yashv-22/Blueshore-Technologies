import os
import re
import markdown as md
from PIL import Image
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

def get_svg_dimensions(svg_path):
    try:
        with open(svg_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        svg_tag = re.search(r'<svg\s+([^>]+)>', content, re.IGNORECASE)
        if svg_tag:
            attrs = dict(re.findall(r'([\w\-:]+)\s*=\s*["\']([^"\']*)["\']', svg_tag.group(1)))
            width_str = attrs.get('width')
            height_str = attrs.get('height')
            
            width, height = None, None
            if width_str and height_str:
                width_str = width_str.replace('px', '').strip()
                height_str = height_str.replace('px', '').strip()
                if '%' not in width_str and '%' not in height_str:
                    try:
                        width = int(float(width_str))
                        height = int(float(height_str))
                    except ValueError:
                        pass
                        
            if width and height:
                return width, height
                
            viewbox = attrs.get('viewBox')
            if viewbox:
                parts = viewbox.split()
                if len(parts) == 4:
                    try:
                        return int(float(parts[2])), int(float(parts[3]))
                    except ValueError:
                        pass
    except Exception:
        pass
    return None

def inject_image_dimensions(html_content):
    img_tag_pattern = re.compile(r'<img\s+([^>]+)>', re.IGNORECASE)
    
    def replace_img(match):
        attrs_str = match.group(1)
        attrs = dict(re.findall(r'([\w\-]+)\s*=\s*["\']([^"\']*)["\']', attrs_str))
        
        src = attrs.get('src')
        if src and not ('width' in attrs and 'height' in attrs):
            img_path = None
            if src.startswith('/assets/'):
                img_path = os.path.join(settings.BASE_DIR, 'assets', src[len('/assets/'):])
            elif src.startswith('/media/'):
                img_path = os.path.join(settings.BASE_DIR, 'media', src[len('/media/'):])
            elif not src.startswith('http') and not src.startswith('//'):
                img_path = os.path.join(settings.BASE_DIR, src.lstrip('/'))
                
            if img_path and os.path.exists(img_path) and os.path.isfile(img_path):
                width, height = None, None
                if img_path.lower().endswith('.svg'):
                    dims = get_svg_dimensions(img_path)
                    if dims:
                        width, height = dims
                else:
                    try:
                        with Image.open(img_path) as img:
                            width, height = img.size
                    except Exception:
                        pass
                
                if width and height:
                    new_attrs = []
                    if 'width' not in attrs:
                        new_attrs.append(f'width="{width}"')
                    if 'height' not in attrs:
                        new_attrs.append(f'height="{height}"')
                    if new_attrs:
                        return f'<img {attrs_str} {" ".join(new_attrs)}>'
        return match.group(0)

    return img_tag_pattern.sub(replace_img, html_content)

@register.filter(name='markdown')
def markdown_filter(value):
    if not value:
        return ""
    rendered_html = md.markdown(value, extensions=['extra', 'codehilite', 'toc'])
    processed_html = inject_image_dimensions(rendered_html)
    return mark_safe(processed_html)

def get_image_dimensions_helper(image_input):
    if not image_input:
        return None
        
    # If it is an ImageFieldFile
    if hasattr(image_input, 'name') and hasattr(image_input, 'url'):
        if image_input.name.lower().endswith('.svg'):
            try:
                if hasattr(image_input, 'path') and os.path.exists(image_input.path):
                    return get_svg_dimensions(image_input.path)
            except Exception:
                pass
        else:
            try:
                if hasattr(image_input, 'width') and hasattr(image_input, 'height') and image_input.width and image_input.height:
                    return image_input.width, image_input.height
            except Exception:
                pass
            try:
                if hasattr(image_input, 'path') and os.path.exists(image_input.path):
                    with Image.open(image_input.path) as img:
                        return img.size
            except Exception:
                pass

    # If it is a string URL or path
    src = str(image_input)
    img_path = None
    if src.startswith('/assets/'):
        img_path = os.path.join(settings.BASE_DIR, 'assets', src[len('/assets/'):])
    elif src.startswith('/media/'):
        img_path = os.path.join(settings.BASE_DIR, 'media', src[len('/media/'):])
    elif not src.startswith('http') and not src.startswith('//'):
        img_path = os.path.join(settings.BASE_DIR, src.lstrip('/'))
        
    if img_path and os.path.exists(img_path) and os.path.isfile(img_path):
        if img_path.lower().endswith('.svg'):
            return get_svg_dimensions(img_path)
        else:
            try:
                with Image.open(img_path) as img:
                    return img.size
            except Exception:
                pass
                
    return None

@register.filter(name='img_width')
def img_width(image_input):
    dims = get_image_dimensions_helper(image_input)
    return dims[0] if dims else ""

@register.filter(name='img_height')
def img_height(image_input):
    dims = get_image_dimensions_helper(image_input)
    return dims[1] if dims else ""

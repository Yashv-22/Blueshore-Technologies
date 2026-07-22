import os
import shutil
from django.conf import settings
from django.core.cache import cache
from apps.seo.models import SEOPage, GEOBlock, FAQ, RobotsRule
from apps.seo.context_processors import DEFAULT_PAGE_SEO
from apps.blog.models import BlogPost
from apps.seo.faq_data import get_page_seo_data

def ensure_seo_database_seeded():
    # Cache key to prevent redundant seeding on every request
    if cache.get('seo_database_is_fully_seeded_v3'):
        return

    # 1. Setup media paths for default OG image
    og_image_relative = 'seo/og/og-image.png'
    og_image_media_path = os.path.join(settings.MEDIA_ROOT, 'seo', 'og', 'og-image.png')
    twitter_image_relative = 'seo/twitter/og-image.png'
    twitter_image_media_path = os.path.join(settings.MEDIA_ROOT, 'seo', 'twitter', 'og-image.png')
    
    source_og = os.path.join(settings.BASE_DIR, 'assets', 'og-image.png')
    if os.path.exists(source_og):
        if not os.path.exists(og_image_media_path):
            os.makedirs(os.path.dirname(og_image_media_path), exist_ok=True)
            try:
                shutil.copy(source_og, og_image_media_path)
            except Exception:
                pass
        if not os.path.exists(twitter_image_media_path):
            os.makedirs(os.path.dirname(twitter_image_media_path), exist_ok=True)
            try:
                shutil.copy(source_og, twitter_image_media_path)
            except Exception:
                pass

    # 2. Seed default, core, and service pages dynamically
    for route in DEFAULT_PAGE_SEO.keys():
        page_name = route.replace('.html', '').replace('/', '').replace('-', ' ').title() or "Home"
        if page_name == "Home" or page_name == "":
            page_name = "Home"

        page_seo_data = get_page_seo_data(route)
        if not page_seo_data:
            continue

        # Create or update SEOPage metadata
        seo, created = SEOPage.objects.get_or_create(
            route=route,
            defaults={
                'page_name': f"{page_name} Page",
                'seo_title': page_seo_data['title'],
                'seo_description': page_seo_data['description'],
                'seo_keywords': page_seo_data['keywords'],
                'canonical_url': page_seo_data['canonical'],
                'robots': page_seo_data['robots'],
                'og_title': page_seo_data['title'],
                'og_description': page_seo_data['description'],
                'twitter_title': page_seo_data['title'],
                'twitter_description': page_seo_data['description']
            }
        )
        
        # Ensure values are strictly up-to-date with latest configurations
        if not created:
            seo.seo_title = page_seo_data['title']
            seo.seo_description = page_seo_data['description']
            seo.seo_keywords = page_seo_data['keywords']
            seo.canonical_url = page_seo_data['canonical']
            seo.robots = page_seo_data['robots']
            seo.save()

        # Populate OG images
        if os.path.exists(og_image_media_path) and not seo.og_image:
            seo.og_image = og_image_relative
            seo.twitter_image = twitter_image_relative
            seo.save()

        # Create or update GEO Block
        geo_block = getattr(seo, 'geo_block', None)
        c_geo = page_seo_data["geo"]
        if geo_block:
            geo_block.featured_answer = c_geo["featured_answer"]
            geo_block.ai_summary = c_geo["featured_answer"]
            geo_block.what_is_this = c_geo["what_is_this"]
            geo_block.who_is_it_for = c_geo["who_is_it_for"]
            geo_block.why_it_matters = c_geo["why_it_matters"]
            geo_block.key_takeaways = "\n".join(c_geo["takeaways"])
            geo_block.eeat_proof_points = c_geo["proof_points"]
            geo_block.save()
        else:
            GEOBlock.objects.create(
                page=seo,
                ai_summary=c_geo["featured_answer"],
                featured_answer=c_geo["featured_answer"],
                what_is_this=c_geo["what_is_this"],
                who_is_it_for=c_geo["who_is_it_for"],
                why_it_matters=c_geo["why_it_matters"],
                key_takeaways="\n".join(c_geo["takeaways"]),
                eeat_proof_points=c_geo["proof_points"]
            )

        # Clear and recreate FAQs for absolute consistency
        seo.faqs.all().delete()
        for idx, faq_info in enumerate(page_seo_data["faqs"]):
            FAQ.objects.create(
                page=seo,
                question=faq_info["q"],
                answer=f"{faq_info['a']}\n{faq_info['details']}",
                display_order=idx,
                is_active=True
            )

    # 3. Seed RobotsRule if none exists
    if RobotsRule.objects.count() == 0:
        RobotsRule.objects.create(
            user_agent="*",
            allow_paths="/",
            disallow_paths="/admin/\n/api/",
        )

    # 4. Heal existing BlogPosts
    for post in BlogPost.objects.all():
        if not post.meta_description or post.seo_score < 70:
            post.save()

    # Cache this check so we do not query the DB on subsequent requests
    cache.set('seo_database_is_fully_seeded_v3', True, timeout=None)

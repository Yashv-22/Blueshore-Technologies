import re
import json
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from apps.seo.models import SEOPage, GEOBlock, FAQ
from apps.seo.context_processors import normalize_route, DEFAULT_PAGE_SEO
from apps.seo.schema_engine import generate_page_schemas
from apps.blog.models import BlogPost

DEFAULT_GEO_BLOCKS = {
    "featured_answer": (
        "Blueshore Technologies helps enterprise partners build custom software, AI/automation systems, "
        "zero-trust cloud architectures, and digital transformation solutions to scale operations globally."
    ),
    "what_is_this": (
        "Blueshore Technologies is a premier B2B software engineering and digital growth agency in Delhi NCR "
        "engineering scalable web applications, custom software, and intelligent AI automation systems."
    ),
    "who_is_it_for": (
        "Global mid-market and enterprise businesses seeking high-performance digital systems, custom web apps, "
        "and robust AI automation solutions."
    ),
    "why_it_matters": (
        "In a hyper-connected economy, technology without strategy is just an expense. We design resilient, "
        "SEO-optimized digital ecosystems that scale conversions and streamline business operations."
    ),
    "key_takeaways": [
        "50+ custom digital platforms successfully delivered globally.",
        "Specialized expertise in AI automation, conversion-focused design, and performance marketing.",
        "Guaranteed 2-hour response SLA with dedicated 24/7 technical support."
    ],
    "eeat_proof_points": (
        "Verified B2B systems engineering by Blueshore Technologies. 50+ products delivered, ISO 27001 readiness, "
        "zero-trust cloud standards, and Clutch Leader honors."
    )
}

DEFAULT_FAQS = [
    {
        "q": "What core services does Blueshore Technologies provide?",
        "a": "Blueshore Technologies specializes in custom website development, SEO & organic growth, performance marketing, AI automation, and branding/creative systems.",
        "details": "We combine advanced Artificial Intelligence (AI), custom engineering, branding, workflow automation, SEO, and performance marketing into one unified growth system designed for real business growth."
    },
    {
        "q": "How does AI automation help businesses scale?",
        "a": "Our custom AI solutions streamline operations, automate customer support, qualify leads, and optimize workflows.",
        "details": "This reduces manual work, increases productivity, and cuts customer acquisition costs."
    },
    {
        "q": "What makes Blueshore Technologies different from other agencies?",
        "a": "We do not build basic websites. We build revenue-generating digital ecosystems combining strategy, tech, and marketing.",
        "details": "Our focus is directly on measurable business outcomes, faster scaling, and reducing client acquisition costs."
    }
]


def generate_geo_aeo_html(seo_page, path):
    parts = [p for p in path.split('/') if p]
    is_programmatic = len(parts) == 2 and not parts[0].endswith('.html') and not parts[1].endswith('.html') and parts[0] not in ['blog', 'authors', 'portal', 'api', 'admin']
    
    geo = None
    page_data = None
    if is_programmatic:
        from apps.seo.programmatic_seo import get_programmatic_page_data
        page_data = get_programmatic_page_data(parts[0], parts[1])
        if page_data:
            geo = page_data["geo_block"]
            
    if not geo and seo_page and seo_page.pk:
        geo = getattr(seo_page, 'geo_block', None)
        
    if geo:
        if is_programmatic:
            featured_answer = geo["featured_answer"]
            what_is_this = geo["what_is_this"]
            who_is_it_for = geo["who_is_it_for"]
            why_it_matters = geo["why_it_matters"]
            takeaways = geo["takeaways_list"]
            proof_points = geo["proof_points_list"]
        else:
            featured_answer = geo.featured_answer
            what_is_this = geo.what_is_this
            who_is_it_for = geo.who_is_it_for
            why_it_matters = geo.why_it_matters
            takeaways = geo.takeaways_list
            proof_points = geo.proof_points_list
    else:
        # Fallback to default GEO block content
        featured_answer = DEFAULT_GEO_BLOCKS["featured_answer"]
        what_is_this = DEFAULT_GEO_BLOCKS["what_is_this"]
        who_is_it_for = DEFAULT_GEO_BLOCKS["who_is_it_for"]
        why_it_matters = DEFAULT_GEO_BLOCKS["why_it_matters"]
        takeaways = DEFAULT_GEO_BLOCKS["key_takeaways"]
        proof_points = [DEFAULT_GEO_BLOCKS["eeat_proof_points"]]

    # Build takeaways HTML
    key_takeaways_html = ""
    for t in takeaways:
        if t.strip():
            key_takeaways_html += f"<li>{t.strip()}</li>\n"
            
    # Build EEAT proof points HTML
    eeat_proof_points_html = " ".join([p.strip() for p in proof_points if p.strip()])
    
    # Try to get active FAQs
    faqs = []
    if is_programmatic and page_data:
        faqs = page_data["faqs"]
    elif seo_page and seo_page.pk:
        faqs = list(seo_page.faqs.filter(is_active=True))
        
    if not faqs:
        faqs = DEFAULT_FAQS

        
    # Build FAQs HTML
    faqs_html = ""
    for faq in faqs:
        q = faq.question if hasattr(faq, 'question') else faq.get('q')
        a = faq.answer if hasattr(faq, 'answer') else faq.get('a')
        
        paragraphs = [p.strip() for p in a.split('\n') if p.strip()]
        if not paragraphs:
            continue
        lead = paragraphs[0]
        body_paragraphs = paragraphs[1:]
        
        if not hasattr(faq, 'answer') and faq.get('details'):
            body_paragraphs.append(faq.get('details'))
            
        answer_html = f'<p class="text-white font-medium pl-3 border-l-2 border-[#3790ff]">{lead}</p>'
        for bp in body_paragraphs:
            answer_html += f'<p>{bp}</p>'
            
        faqs_html += f"""
                    <div
                        class="bg-[#0B1221] border border-white/[0.06] rounded-xl overflow-hidden transition-all duration-300 hover:border-[#3790ff]/30">
                        <button type="button"
                            class="w-full px-6 py-4 flex items-center justify-between text-left text-white font-semibold hover:text-[#3790ff] transition-colors"
                            onclick="toggleFaq(this)" aria-expanded="false">
                            <span>{q}</span>
                            <span
                                class="material-symbols-outlined transition-transform duration-300 pointer-events-none">expand_more</span>
                        </button>
                        <div class="faq-content max-h-0 overflow-hidden transition-all duration-300 ease-in-out">
                            <div
                                class="px-6 pb-6 text-sm text-slate-400 font-light leading-relaxed border-t border-white/[0.03] pt-4 space-y-3">
                                {answer_html}
                            </div>
                        </div>
                    </div>
        """
        
    # Compile the final GEO & AEO block matching layout and classes
    return f"""<!-- GEO & AEO Content Block -->
    <section
        class="py-16 bg-[#030816] text-[#e2e8f0] border-t border-white/[0.06] font-['Inter'] relative overflow-hidden"
        aria-label="Factual Summary and Frequently Asked Questions">
        <div class="absolute inset-0 opacity-[0.02] pointer-events-none"
            style="background-image: radial-gradient(circle, #3790ff 1px, transparent 1px); background-size: 30px 30px;">
        </div>
        <div class="max-w-[1280px] mx-auto px-8 relative z-10">

            <blockquote
                class="answer-summary featured-answer text-lg text-white font-medium pl-4 border-l-4 border-[#3790ff] leading-relaxed mb-16 md:mb-20 max-w-4xl mx-auto italic text-center md:text-left">
                "{featured_answer}"
            </blockquote>

            <!-- GEO Block Header -->
            <div class="grid lg:grid-cols-3 gap-10 md:gap-12 pb-14 border-b border-white/[0.06] text-left">
                <!-- Column 1: What is this & Who is it for -->
                <div class="space-y-8">
                    <div>
                        <h3 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-2">What Is This?</h3>
                        <p class="text-sm text-slate-400 leading-relaxed font-light">
                            {what_is_this}
                        </p>
                    </div>
                    <div class="pt-6 border-t border-white/[0.06]">
                        <h4 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-2">Who Is It For?</h4>
                        <p class="text-xs text-slate-400 leading-relaxed font-light">
                            {who_is_it_for}
                        </p>
                    </div>
                </div>

                <!-- Column 2: Why it matters & Key Takeaways -->
                <div class="space-y-8">
                    <div>
                        <h3 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-2">Why It Matters</h3>
                        <p class="text-sm text-slate-300 leading-relaxed font-light">
                            {why_it_matters}
                        </p>
                    </div>
                    <div class="pt-6 border-t border-white/[0.06]">
                        <h4 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-2">Key Takeaways</h4>
                        <ul class="list-disc pl-4 text-xs text-slate-400 space-y-1.5 font-light">
                            {key_takeaways_html}
                        </ul>
                    </div>
                </div>

                <!-- Column 3: Core Benefits -->
                <div class="space-y-8">
                    <div>
                        <h3 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-2">Core Benefits</h3>
                        <ul class="text-xs text-slate-400 space-y-2.5 font-light">
                            <li><strong class="text-white">Conversion Optimization:</strong> Fast, mobile-first websites designed to turn visitors into leads.</li>
                            <li><strong class="text-white">AI Automation:</strong> Custom CRM, chatbots, and workflow automation reducing manual work.</li>
                            <li><strong class="text-white">Performance Marketing:</strong> Data-driven ad campaigns maximizing ROI and growth.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- AEO FAQ Accordion Block -->
            <div class="pt-14 max-w-4xl mx-auto">
                <h3 class="text-2xl font-bold text-center text-white mb-10 tracking-tight">Common Questions (AEO & FAQ)</h3>
                <div class="space-y-4" id="aeo-faq-accordion">
                    {faqs_html}
                </div>
            </div>

        </div>
    </section>

    <script>
        function toggleFaq(button) {{
            const parent = button.parentElement;
            const content = parent.querySelector('.faq-content');
            const icon = button.querySelector('.material-symbols-outlined');
            const isExpanded = button.getAttribute('aria-expanded') === 'true';

            // Close other FAQ items
            const allItems = parent.parentElement.querySelectorAll('.faq-content');
            const allButtons = parent.parentElement.querySelectorAll('button');
            const allIcons = parent.parentElement.querySelectorAll('.material-symbols-outlined');

            allItems.forEach((el, index) => {{
                el.style.maxHeight = null;
                allButtons[index].setAttribute('aria-expanded', 'false');
                allIcons[index].style.transform = 'rotate(0deg)';
            }});

            if (!isExpanded) {{
                content.style.maxHeight = content.scrollHeight + "px";
                button.setAttribute('aria-expanded', 'true');
                icon.style.transform = 'rotate(180deg)';
            }} else {{
                content.style.maxHeight = null;
                button.setAttribute('aria-expanded', 'false');
                icon.style.transform = 'rotate(0deg)';
            }}
        }}
    </script>
    <!-- End GEO & AEO Content Block -->"""


class SEOMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Only process successful HTML responses
        if response.status_code != 200 or 'text/html' not in response.get('Content-Type', ''):
            return response

        from apps.seo.seeder import ensure_seo_database_seeded
        ensure_seo_database_seeded()

        path = request.path
        
        # Check cache if not authenticated
        is_cacheable = not (hasattr(request, 'user') and request.user.is_authenticated)
        cache_key = f"seo_processed_content:{path}"
        if is_cacheable:
            cached_html = cache.get(cache_key)
            if cached_html:
                response.content = cached_html.encode('utf-8')
                response['Content-Length'] = str(len(response.content))
                return response

        route = normalize_route(path)
        seo = None
        fallback = None

        # Resolve dynamic overrides for blog detail and author pages
        if path.startswith('/blog/') and not path.endswith('blog.html'):
            slug = path.strip('/').split('/')[-1]
            post = BlogPost.objects.filter(slug=slug, is_published=True).first()
            if post:
                seo = SEOPage(
                    page_name=f"Blog: {post.title}",
                    route=path,
                    seo_title=post.meta_title or post.title,
                    seo_description=post.meta_description or post.summary,
                    seo_keywords=post.meta_keywords,
                    canonical_url=post.canonical_url or f"https://www.blueshoretech.com{path}",
                    robots="index, follow"
                )
                if post.og_image:
                    seo.og_image = post.og_image
                    seo.twitter_image = post.og_image
        elif path.startswith('/authors/'):
            slug = path.strip('/').split('/')[-1]
            username_map = {
                'abhishek-kashyap': 'abhishek',
                'ashish-kushwaha': 'ashish',
            }
            username = username_map.get(slug.lower())
            if not username:
                username = slug.split('-')[0].lower()
            from apps.blog.models import AuthorProfile
            profile = AuthorProfile.objects.filter(user__username=username).first()
            if profile:
                full_name = profile.user.get_full_name() or profile.user.username
                seo = SEOPage(
                    page_name=f"Author: {full_name}",
                    route=path,
                    seo_title=f"Meet {full_name} | {profile.role} - Blueshore Technologies",
                    seo_description=f"Read expert insights and articles by {full_name}, {profile.role} at Blueshore Technologies, specializing in {profile.expertise}.",
                    seo_keywords=f"blueshore technologies, {full_name}, {profile.role}, {profile.expertise}",
                    canonical_url=f"https://www.blueshoretech.com{path}",
                    robots="index, follow"
                )
                if profile.avatar:
                    seo.og_image = profile.avatar
                    seo.twitter_image = profile.avatar
        else:
            parts = [p for p in path.split('/') if p]
            is_programmatic = len(parts) == 2 and not parts[0].endswith('.html') and not parts[1].endswith('.html') and parts[0] not in ['blog', 'authors', 'portal', 'api', 'admin']
            
            if is_programmatic:
                from apps.seo.programmatic_seo import get_programmatic_page_data
                page_data = get_programmatic_page_data(parts[0], parts[1])
                if page_data:
                    seo = SEOPage(
                        page_name=f"Programmatic: {parts[0]}/{parts[1]}",
                        route=path,
                        seo_title=page_data['seo_title'],
                        seo_description=page_data['seo_description'],
                        seo_keywords=page_data['seo_keywords'],
                        canonical_url=page_data['canonical_url'],
                        robots="index, follow"
                    )
            
            if not seo:
                # Lookup database-backed page configuration
                seo = SEOPage.objects.filter(route=route).first()
                if not seo and path == '/':
                    seo = SEOPage.objects.filter(route='/index.html').first()


        # If not found in database, build virtual SEOPage from default configurations
        if not seo:
            fallback = DEFAULT_PAGE_SEO.get(route)
            if not fallback and route == '/index.html':
                fallback = DEFAULT_PAGE_SEO.get('/')
            
            if fallback:
                seo = SEOPage(
                    page_name=f"Fallback: {route}",
                    route=route,
                    seo_title=fallback['title'],
                    seo_description=fallback['description'],
                    seo_keywords=fallback['keywords'],
                    canonical_url=fallback['canonical'],
                    robots=fallback['robots']
                )

        if not seo:
            return response

        content = response.content.decode('utf-8', errors='ignore')

        # Strip all existing hardcoded JSON-LD schema blocks to prevent duplicates
        content = re.sub(r'<script\s+type=[\'"]application/ld\+json[\'"]>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

        # Replace Title
        if seo.seo_title:
            content = re.sub(r'<title>.*?</title>', lambda m: f'<title>{seo.seo_title}</title>', content, flags=re.IGNORECASE)

        # Replace/Inject Meta Description
        if seo.seo_description:
            desc_tag = f'<meta name="description" content="{seo.seo_description}">'
            if re.search(r'<meta\s+name="description"\s+content=".*?"\s*/?>', content, flags=re.IGNORECASE):
                content = re.sub(r'<meta\s+name="description"\s+content=".*?"\s*/?>', lambda m: desc_tag, content, flags=re.IGNORECASE)
            elif re.search(r'<meta\s+content=".*?"\s+name="description"\s*/?>', content, flags=re.IGNORECASE):
                content = re.sub(r'<meta\s+content=".*?"\s+name="description"\s*/?>', lambda m: desc_tag, content, flags=re.IGNORECASE)
            else:
                content = re.sub(r'</head>', lambda m: f'{desc_tag}\n</head>', content, flags=re.IGNORECASE)

        # Replace/Inject Meta Keywords
        if seo.seo_keywords:
            keywords_tag = f'<meta name="keywords" content="{seo.seo_keywords}">'
            if re.search(r'<meta\s+name="keywords"\s+content=".*?"\s*/?>', content, flags=re.IGNORECASE):
                content = re.sub(r'<meta\s+name="keywords"\s+content=".*?"\s*/?>', lambda m: keywords_tag, content, flags=re.IGNORECASE)
            else:
                content = re.sub(r'</head>', lambda m: f'{keywords_tag}\n</head>', content, flags=re.IGNORECASE)

        # Replace/Inject Robots tag
        if seo.robots:
            robots_tag = f'<meta name="robots" content="{seo.robots}">'
            if re.search(r'<meta\s+name="robots"\s+content=".*?"\s*/?>', content, flags=re.IGNORECASE):
                content = re.sub(r'<meta\s+name="robots"\s+content=".*?"\s*/?>', lambda m: robots_tag, content, flags=re.IGNORECASE)
            else:
                content = re.sub(r'</head>', lambda m: f'{robots_tag}\n</head>', content, flags=re.IGNORECASE)

        # Replace/Inject Canonical URL
        if seo.canonical_url or (fallback and fallback.get('canonical')):
            canonical_val = seo.canonical_url or fallback.get('canonical')
            canonical_tag = f'<link rel="canonical" href="{canonical_val}">'
            if re.search(r'<link\s+rel="canonical"\s+href=".*?"\s*/?>', content, flags=re.IGNORECASE):
                content = re.sub(r'<link\s+rel="canonical"\s+href=".*?"\s*/?>', lambda m: canonical_tag, content, flags=re.IGNORECASE)
            else:
                content = re.sub(r'</head>', lambda m: f'{canonical_tag}\n</head>', content, flags=re.IGNORECASE)

        # Open Graph & Twitter Card Overrides
        og_t = seo.og_title or seo.seo_title
        og_d = seo.og_description or seo.seo_description
        
        try:
            og_img_url = seo.og_image.url if (seo.og_image and hasattr(seo.og_image, 'url') and seo.og_image.name) else "https://www.blueshoretech.com/assets/og-image.png"
        except ValueError:
            og_img_url = "https://www.blueshoretech.com/assets/og-image.png"
        
        twitter_t = seo.twitter_title or og_t
        twitter_d = seo.twitter_description or og_d
        
        try:
            twitter_img_url = seo.twitter_image.url if (seo.twitter_image and hasattr(seo.twitter_image, 'url') and seo.twitter_image.name) else og_img_url
        except ValueError:
            twitter_img_url = og_img_url

        # Helper replacements
        def replace_og_twitter_tags(html):
            # og:title
            if re.search(r'<meta\s+property="og:title"\s+content=".*?"\s*/?>', html, flags=re.IGNORECASE):
                html = re.sub(r'<meta\s+property="og:title"\s+content=".*?"\s*/?>', lambda m: f'<meta property="og:title" content="{og_t}">', html, flags=re.IGNORECASE)
            else:
                html = re.sub(r'</head>', lambda m: f'<meta property="og:title" content="{og_t}">\n</head>', html, flags=re.IGNORECASE)
            
            # og:description
            if re.search(r'<meta\s+property="og:description"\s+content=".*?"\s*/?>', html, flags=re.IGNORECASE):
                html = re.sub(r'<meta\s+property="og:description"\s+content=".*?"\s*/?>', lambda m: f'<meta property="og:description" content="{og_d}">', html, flags=re.IGNORECASE)
            else:
                html = re.sub(r'</head>', lambda m: f'<meta property="og:description" content="{og_d}">\n</head>', html, flags=re.IGNORECASE)

            # og:image
            if re.search(r'<meta\s+property="og:image"\s+content=".*?"\s*/?>', html, flags=re.IGNORECASE):
                html = re.sub(r'<meta\s+property="og:image"\s+content=".*?"\s*/?>', lambda m: f'<meta property="og:image" content="{og_img_url}">', html, flags=re.IGNORECASE)
            else:
                html = re.sub(r'</head>', lambda m: f'<meta property="og:image" content="{og_img_url}">\n</head>', html, flags=re.IGNORECASE)

            # twitter:title
            if re.search(r'<meta\s+name="twitter:title"\s+content=".*?"\s*/?>', html, flags=re.IGNORECASE):
                html = re.sub(r'<meta\s+name="twitter:title"\s+content=".*?"\s*/?>', lambda m: f'<meta name="twitter:title" content="{twitter_t}">', html, flags=re.IGNORECASE)
            else:
                html = re.sub(r'</head>', lambda m: f'<meta name="twitter:title" content="{twitter_t}">\n</head>', html, flags=re.IGNORECASE)

            # twitter:description
            if re.search(r'<meta\s+name="twitter:description"\s+content=".*?"\s*/?>', html, flags=re.IGNORECASE):
                html = re.sub(r'<meta\s+name="twitter:description"\s+content=".*?"\s*/?>', lambda m: f'<meta name="twitter:description" content="{twitter_d}">', html, flags=re.IGNORECASE)
            else:
                html = re.sub(r'</head>', lambda m: f'<meta name="twitter:description" content="{twitter_d}">\n</head>', html, flags=re.IGNORECASE)

            # twitter:image
            if re.search(r'<meta\s+name="twitter:image"\s+content=".*?"\s*/?>', html, flags=re.IGNORECASE):
                html = re.sub(r'<meta\s+name="twitter:image"\s+content=".*?"\s*/?>', lambda m: f'<meta name="twitter:image" content="{twitter_img_url}">', html, flags=re.IGNORECASE)
            else:
                html = re.sub(r'</head>', lambda m: f'<meta name="twitter:image" content="{twitter_img_url}">\n</head>', html, flags=re.IGNORECASE)

            return html

        content = replace_og_twitter_tags(content)

        # Inject dynamic Breadcrumbs and Structured Schema markup inside <head>
        fallback_config = fallback if fallback else DEFAULT_PAGE_SEO.get(route, {})
        if not fallback_config and route == '/index.html':
            fallback_config = DEFAULT_PAGE_SEO.get('/')
            
        schema_html = generate_page_schemas(request, seo_page=seo, fallback_config=fallback_config)
        content = re.sub(r'</head>', lambda m: f'{schema_html}</head>', content, flags=re.IGNORECASE)

        # Replace GEO & AEO Content Block (Exclude from legal pages)
        is_legal_page = any(p in route for p in ['privacy.html', 'terms.html', 'cookie.html'])
        if is_legal_page:
            geo_block_html = ""
        else:
            geo_block_html = generate_geo_aeo_html(seo, path)

        content = re.sub(
            r'<!--\s*GEO\s*&\s*AEO\s*Content\s*Block\s*-->.*?<!--\s*End\s*GEO\s*&\s*AEO\s*Content\s*Block\s*-->',
            lambda m: geo_block_html,
            content,
            flags=re.DOTALL | re.IGNORECASE
        )

        response.content = content.encode('utf-8')
        response['Content-Length'] = str(len(response.content))

        # Cache the processed output
        if is_cacheable:
            cache.set(cache_key, content, timeout=300)

        return response

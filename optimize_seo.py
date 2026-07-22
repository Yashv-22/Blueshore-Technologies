import os
import sys
import re
import glob
import django

# Initialize Django to access context processors and models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blueshore_server.settings')
django.setup()

from apps.seo.faq_data import get_page_seo_data

# Map basenames to their clean URL routes in the seeder/context processor
FILE_ROUTE_MAPPING = {
    "index.html": "/",
    "about.html": "/about.html",
    "services.html": "/services.html",
    "industries.html": "/industries.html",
    "portfolio.html": "/portfolio.html",
    "blog.html": "/blog.html",
    "careers.html": "/careers.html",
    "submit-portfolio.html": "/submit-portfolio.html",
    "contact.html": "/contact.html",
    "privacy.html": "/privacy.html",
    "terms.html": "/terms.html",
    "cookie.html": "/cookie.html",
    "custom-software-development.html": "/custom-software-development/",
    "ai-automation-services.html": "/ai-automation-services/",
    "web-development-services.html": "/web-development-services/",
    "seo-services.html": "/seo-services/",
    "performance-marketing.html": "/performance-marketing/",
    "cloud-engineering.html": "/cloud-engineering/",
    "ai-chatbot-development.html": "/ai-chatbot-development/",
    "workflow-automation.html": "/workflow-automation/"
}

def get_benefits_for_route(route):
    # Dynamic benefit lists matching target search intent
    if "/custom-software-development/" in route:
        return [
            "<li><strong>Bespoke Engineering:</strong> 100% custom-built codebases aligned with your B2B strategy.</li>",
            "<li><strong>Zero Vendor Lock-In:</strong> Absolute intellectual property and source code ownership transfer.</li>",
            "<li><strong>Million-Load Resiliency:</strong> High-throughput backends designed to scale with your volume.</li>"
        ]
    elif "/ai-automation-services/" in route:
        return [
            "<li><strong>10x Work Leverage:</strong> Automate manual data entry and let your staff focus on growth.</li>",
            "<li><strong>Enterprise Security:</strong> Sandboxed training data hosted securely on private cloud nodes.</li>",
            "<li><strong>Continuous Monitoring:</strong> Real-time logging and human-in-the-loop error validation.</li>"
        ]
    elif "/web-development-services/" in route:
        return [
            "<li><strong>Sub-Second Loading:</strong> Optimized image pipelines and pre-compiled CSS for speed.</li>",
            "<li><strong>SEO-First Architecture:</strong> Built-in structured schemas, clean grids, and indexable code.</li>",
            "<li><strong>Conversion Focused:</strong> Tactile interfaces engineered to turn traffic into qualified leads.</li>"
        ]
    elif "/seo-services/" in route:
        return [
            "<li><strong>Technical Remediations:</strong> Resolve crawl budget blocks, indexing errors, and redirects.</li>",
            "<li><strong>Generative Citations:</strong> AEO structures designed to earn citations in AI search engines.</li>",
            "<li><strong>Topical Domain Authority:</strong> High-buyer-intent content clusters that dominate search rankings.</li>"
        ]
    elif "/performance-marketing/" in route:
        return [
            "<li><strong>CAC Reduction:</strong> Slashing acquisition costs by 30% via negative keyword routing.</li>",
            "<li><strong>ABM Optimization:</strong> Secure high-ticket corporate contracts with targeted LinkedIn campaigns.</li>",
            "<li><strong>Real-Time Analytics:</strong> Comprehensive, audited dashboards tracking actual marketing ROI.</li>"
        ]
    elif "/cloud-engineering/" in route:
        return [
            "<li><strong>99.99% Uptime SLA:</strong> Multi-region replication, auto-scaling, and active server monitoring.</li>",
            "<li><strong>Zero-Trust DevOps:</strong> Infrastructure-as-code and IAM credentials aligned with SOC 2.</li>",
            "<li><strong>CI/CD Pipelines:</strong> Automated testing and security scanning on every codebase compile.</li>"
        ]
    elif "/ai-chatbot-development/" in route:
        return [
            "<li><strong>Zero Hallucination:</strong> RAG architectures forcing AI to answer from private documents.</li>",
            "<li><strong>24/7 Support Self-Service:</strong> Automate customer ticketing and transaction routines securely.</li>",
            "<li><strong>Warm Human Handoff:</strong> Automatic routing to human agents with full chat transcripts.</li>"
        ]
    elif "/workflow-automation/" in route:
        return [
            "<li><strong>API Integration:</strong> Sync data across CRMs, billing, and legacy databases instantly.</li>",
            "<li><strong>Agentic Pipelines:</strong> Autonomous multi-agent coordination executing multi-step processes.</li>",
            "<li><strong>Zero Data Silos:</strong> Clean, synchronized datasets establishing a single operational truth.</li>"
        ]
    else:
        return [
            "<li><strong>Conversion Optimization:</strong> Fast, mobile-first websites designed to turn visitors into leads.</li>",
            "<li><strong>AI Automation:</strong> Custom CRM, chatbots, and workflow automation reducing manual work.</li>",
            "<li><strong>Performance Marketing:</strong> Data-driven ad campaigns maximizing ROI and growth.</li>"
        ]

# Dynamically construct PAGE_CONFIGS by pulling from faq_data.py
PAGE_CONFIGS = {}
for filename, route in FILE_ROUTE_MAPPING.items():
    data = get_page_seo_data(route)
    if data:
        PAGE_CONFIGS[filename] = {
            "title": data["title"],
            "description": data["description"],
            "keywords": data["keywords"],
            "canonical": data["canonical"],
            "robots": data["robots"],
            "schema_type": data["schema_type"],
            "geo_what_is": data["geo"]["what_is_this"],
            "geo_who_is": data["geo"]["who_is_it_for"],
            "geo_why_matters": data["geo"]["why_it_matters"],
            "geo_takeaways": data["geo"]["takeaways"],
            "geo_benefits": get_benefits_for_route(route),
            "faqs": data["faqs"]
        }

# Base JSON-LD Templates
def generate_base_jsonld(page_name, config):
    schema_type = config["schema_type"]
    
    aggregate_rating = {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "38",
        "bestRating": "5",
        "worstRating": "1"
    }
    
    review_data = [
        {
            "@type": "Review",
            "author": {
                "@type": "Person",
                "name": "Sarah Jenkins"
            },
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "5"
            },
            "reviewBody": "Blueshore Technologies successfully migrated our legacy core banking ledger to a microservices architecture. Outstanding engineering expertise and uptime assurance."
        }
    ]

    is_homepage = page_name == "index.html"

    org_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": "https://www.blueshoretech.com/#organization",
        "name": "Blueshore Technologies",
        "url": "https://www.blueshoretech.com",
        "logo": "https://www.blueshoretech.com/assets/logo.png",
        "image": "https://www.blueshoretech.com/assets/og-image.png",
        "description": "Award-winning enterprise software development company engineering high-performance digital solutions, AI automation, and scalable cloud architectures for global businesses.",
        "foundingDate": "2020",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Delhi NCR",
            "addressRegion": "Delhi",
            "addressCountry": "IN"
        },
        "email": "info@blueshoretech.com",
        "telephone": "+91-99907-12555",
        "sameAs": [
            "https://www.linkedin.com/company/blueshore-technologies-pvt-ltd/",
            "https://twitter.com/blueshoretechco"
        ]
    }
    
    if is_homepage:
        org_schema["aggregateRating"] = aggregate_rating
        org_schema["review"] = review_data

    org_ref = {
        "@type": "Organization",
        "@id": "https://www.blueshoretech.com/#organization"
    }

    local_business_schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://www.blueshoretech.com/#localbusiness",
        "name": "Blueshore Technologies Pvt. Ltd.",
        "image": "https://www.blueshoretech.com/assets/og-image.png",
        "telephone": "+91-99907-12555",
        "email": "info@blueshoretech.com",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Delhi NCR",
            "addressRegion": "Delhi",
            "addressCountry": "IN"
        },
        "url": "https://www.blueshoretech.com",
        "priceRange": "$$$",
        "parentOrganization": org_ref
    }

    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Blueshore Technologies",
        "url": "https://www.blueshoretech.com",
        "description": "Enterprise software development and digital transformation services for global businesses.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "https://www.blueshoretech.com/blog.html?q={search_term_string}"
            },
            "query-input": "required name=search_term_string"
        }
    }

    webpage_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": config["title"],
        "description": config["description"],
        "url": config["canonical"],
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [
                ".answer-summary",
                ".featured-answer"
            ]
        },
        "about": [
            {"@type": "Thing", "name": "Blueshore Technologies", "sameAs": "https://en.wikipedia.org/wiki/Software_development"},
            {"@type": "Thing", "name": "Custom Software Development", "sameAs": "https://en.wikipedia.org/wiki/Custom_software"},
            {"@type": "Thing", "name": "AI Automation Platform", "sameAs": "https://en.wikipedia.org/wiki/Artificial_intelligence"},
            {"@type": "Thing", "name": "Cloud Computing", "sameAs": "https://en.wikipedia.org/wiki/Cloud_computing"},
            {"@type": "Thing", "name": "Delhi NCR", "sameAs": "https://en.wikipedia.org/wiki/National_Capital_Region_(India)"}
        ],
        "publisher": org_ref
    }

    software_app_schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Blueshore AI Automation Platform",
        "operatingSystem": "All",
        "applicationCategory": "BusinessApplication",
        "description": "Enterprise-grade AI and intelligent automation platform designed to optimize workflow operations, data pipelines, and transactional scalability.",
        "offers": {
            "@type": "Offer",
            "price": "0.00",
            "priceCurrency": "USD",
            "description": "Custom enterprise deployment pricing available upon consultation."
        }
    }

    howto_schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How Blueshore Technologies Builds Custom Software & Cloud Architectures",
        "description": "Step-by-step enterprise engineering process from technical discovery to production deployment.",
        "totalTime": "P6W",
        "step": [
            {
                "@type": "HowToStep",
                "name": "Technical Discovery & Solution Design",
                "text": "Our software architects review your transaction loads, security requirements, and technical legacy constraints to design a customized engineering roadmap.",
                "url": "https://www.blueshoretech.com/services.html#discovery"
            },
            {
                "@type": "HowToStep",
                "name": "Agile Development & Code Sprints",
                "text": "Dedicated squads build full-stack code in 2-week sprints, checking in standard-compliant, documented repositories with continuous integration validation.",
                "url": "https://www.blueshoretech.com/services.html#development"
            },
            {
                "@type": "HowToStep",
                "name": "Security Audits & Zero-Trust Verification",
                "text": "Every release undergoes static analysis, vulnerability scanning, and container verification to comply with HIPAA/PCI-DSS standards.",
                "url": "https://www.blueshoretech.com/services.html#security"
            },
            {
                "@type": "HowToStep",
                "name": "Production Release & SLA Monitoring",
                "text": "We deploy scalable container clusters (Kubernetes) and offer 24/7 ongoing support with a guaranteed 2-hour response SLA.",
                "url": "https://www.blueshoretech.com/services.html#deployment"
            }
        ]
    }

    page_schema = None
    if schema_type == "AboutPage":
        page_schema = {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "name": config["title"],
            "description": config["description"],
            "url": config["canonical"],
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".answer-summary", ".featured-answer"]
            },
            "about": [
                {
                    "@type": "Person",
                    "name": "Abhishek Kashyap",
                    "jobTitle": "Co-Founder & Director",
                    "worksFor": {"@type": "Organization", "name": "Blueshore Technologies"}
                },
                {
                    "@type": "Person",
                    "name": "Ashish Kushwaha",
                    "jobTitle": "Co-Founder & Director",
                    "worksFor": {"@type": "Organization", "name": "Blueshore Technologies"}
                }
            ],
            "publisher": org_ref
        }
    elif schema_type == "Service":
        page_schema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Blueshore Technologies Services",
            "url": config["canonical"],
            "description": config["description"],
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@type": "Service",
                        "name": "Custom Software Development",
                        "description": "Bespoke enterprise applications handling millions of transactions with microservices, legacy modernization, and secure architecture."
                    }
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@type": "Service",
                        "name": "Cloud Architecture & DevOps",
                        "description": "Multi-cloud infrastructure design, CI/CD pipeline automation, and zero-trust security on AWS, Azure, and Google Cloud."
                    }
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "item": {
                        "@type": "Service",
                        "name": "AI & Automation Services",
                        "description": "AI-powered automation, machine learning integration, workflow automation, and intelligent data pipelines for enterprise operations."
                    }
                }
            ]
        }
    elif schema_type == "ContactPage":
        page_schema = {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": config["title"],
            "description": config["description"],
            "url": config["canonical"],
            "mainEntity": org_ref
        }
    elif schema_type == "CollectionPage":
        page_schema = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": config["title"],
            "description": config["description"],
            "url": config["canonical"],
            "publisher": org_ref
        }
    elif schema_type == "Blog":
        page_schema = {
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "Blueshore Technologies Insights",
            "description": config["description"],
            "url": config["canonical"],
            "publisher": org_ref
        }
    else:
        page_schema = webpage_schema

    faq_schema = None
    if config.get("faqs"):
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": faq["q"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"{faq['a']}\n{faq.get('details', '')}"
                    }
                } for faq in config["faqs"]
            ]
        }

    schemas = []
    schemas.append(webpage_schema)
    # Append the root Organization schema to every page
    schemas.append(org_schema)

    if page_name == "index.html":
        schemas.append(local_business_schema)
        schemas.append(website_schema)
        schemas.append(software_app_schema)
    else:
        if page_schema != webpage_schema:
            schemas.append(page_schema)
        
    if page_name == "services.html":
        schemas.append(software_app_schema)
        schemas.append(howto_schema)
        
    if faq_schema:
        schemas.append(faq_schema)

    import json
    json_blocks = ""
    for s in schemas:
        json_blocks += f'<script type="application/ld+json">\n{json.dumps(s, indent=2)}\n</script>\n'
    return json_blocks

# GEO & AEO Blocks Generator
def generate_geo_aeo_block(page_name, config):
    geo_what_is = config["geo_what_is"]
    geo_who_is = config["geo_who_is"]
    geo_why_matters = config["geo_why_matters"]
    geo_takeaways_html = "".join([f"<li>{item}</li>" for item in config["geo_takeaways"]])
    geo_benefits_html = "".join(config["geo_benefits"])
    
    faq_items_html = ""
    for idx, faq in enumerate(config["faqs"]):
        detailed = faq.get("details", "")
        faq_items_html += f"""
                <div class="bg-[#0B1221] border border-white/[0.06] rounded-xl overflow-hidden transition-all duration-300 hover:border-[#3790ff]/30">
                    <button type="button" class="w-full px-6 py-4 flex items-center justify-between text-left text-white font-semibold hover:text-[#3790ff] transition-colors" onclick="toggleFaq(this)" aria-expanded="false">
                        <span>{faq["q"]}</span>
                        <span class="material-symbols-outlined transition-transform duration-300 pointer-events-none">expand_more</span>
                    </button>
                    <div class="faq-content max-h-0 overflow-hidden transition-all duration-300 ease-in-out">
                        <div class="px-6 pb-6 text-sm text-slate-400 font-light leading-relaxed border-t border-white/[0.03] pt-4 space-y-3">
                            <p class="text-white font-medium pl-3 border-l-2 border-[#3790ff]">{faq["a"]}</p>
                            <p>{detailed}</p>
                        </div>
                    </div>
                </div>
        """

    citation_blockquote_html = f"""
                <blockquote class="answer-summary featured-answer text-lg text-white font-medium pl-4 border-l-4 border-[#3790ff] leading-relaxed mb-10 max-w-4xl mx-auto italic text-center md:text-left">
                    "{config["geo_what_is"]}"
                </blockquote>
    """

    return f"""
        <!-- GEO & AEO Content Block -->
        <section class="py-16 bg-[#030816] text-[#e2e8f0] border-t border-white/[0.06] font-['Inter'] relative overflow-hidden" aria-label="Factual Summary and Frequently Asked Questions">
            <div class="absolute inset-0 opacity-[0.02] pointer-events-none" style="background-image: radial-gradient(circle, #3790ff 1px, transparent 1px); background-size: 30px 30px;"></div>
            <div class="max-w-[1280px] mx-auto px-8 relative z-10">
                {citation_blockquote_html}
                
                <!-- GEO Block Header -->
                <div class="grid lg:grid-cols-3 gap-12 pb-14 border-b border-white/[0.06] text-left">
                    <div class="space-y-4">
                        <h3 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold">What Is This?</h3>
                        <p class="text-sm text-slate-400 leading-relaxed font-light">
                            {geo_what_is}
                        </p>
                        <div class="pt-2">
                            <h4 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-2">Who Is It For?</h4>
                            <p class="text-xs text-slate-500 leading-relaxed font-light">
                                {geo_who_is}
                            </p>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <h3 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold">Why It Matters</h3>
                        <p class="text-sm text-slate-300 leading-relaxed font-light">
                            {geo_why_matters}
                        </p>
                        <div>
                            <h4 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-2">Key Takeaways</h4>
                            <ul class="list-disc pl-4 text-xs text-slate-500 space-y-1.5 font-light">
                                {geo_takeaways_html}
                            </ul>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <h3 class="text-xs uppercase tracking-widest text-white font-bold">Core Benefits</h3>
                        <ul class="text-xs text-slate-400 space-y-2 font-light">
                            {geo_benefits_html}
                        </ul>
                        <div class="pt-2 border-t border-white/[0.06]">
                            <h4 class="text-xs uppercase tracking-widest text-[#3790ff] font-bold mb-1.5">E-E-A-T Authority</h4>
                            <p class="text-[10px] text-slate-500 leading-relaxed font-light">
                                Verified B2B systems engineering by Blueshore Technologies. 150+ products delivered, ISO 27001 readiness, zero-trust cloud standards, and Clutch Leader honors.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- AEO FAQ Accordion Block -->
                <div class="pt-14 max-w-4xl mx-auto">
                    <h3 class="text-2xl font-bold text-center text-white mb-10 tracking-tight">Common Questions (AEO & FAQ)</h3>
                    <div class="space-y-4" id="aeo-faq-accordion">
                        {faq_items_html}
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
        <!-- End GEO & AEO Content Block -->
    """

def optimize_html_file(file_path):
    page_name = os.path.basename(file_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix legacy internal redirects
    new_content = re.sub(r'href=["\'](?:https?://(?:www\.)?blueshoretech\.com)?/?index\.html["\']', 'href="/"', content, flags=re.IGNORECASE)
    if new_content != content:
        print(f"Fixed index.html link in: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        content = new_content

    if page_name not in PAGE_CONFIGS:
        return
        
    print(f"Optimizing SEO/Schema for: {file_path}")
    config = PAGE_CONFIGS[page_name]

    # Clean existing SEO tags and JSON-LD block scripts
    content = re.sub(r'<title>.*?</title>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+[^>]*name=["\'](description|keywords|robots|author)["\'][^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+[^>]*property=["\']og:[^"\']+["\'][^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+[^>]*name=["\']twitter:[^"\']+["\'][^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<link\s+[^>]*rel=["\'](canonical|preconnect|dns-prefetch)["\'][^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<script\s+type=["\']application/ld\+json["\']>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<!--\s*(Open Graph|Twitter Card|Structured Data|Primary SEO|JSON-LD).*?-->', '', content, flags=re.IGNORECASE)

    # Build the optimized head elements
    head_elements = f"""
    <title>{config["title"]}</title>
    <meta name="description" content="{config["description"]}">
    <meta name="keywords" content="{config["keywords"]}">
    <meta name="author" content="Blueshore Technologies">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <link rel="canonical" href="{config["canonical"]}">

    <!-- Open Graph Tags -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{config["canonical"]}">
    <meta property="og:site_name" content="Blueshore Technologies">
    <meta property="og:title" content="{config["title"]}">
    <meta property="og:description" content="{config["description"]}">
    <meta property="og:image" content="https://www.blueshoretech.com/assets/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Blueshore Technologies - Enterprise Solutions">
    <meta property="og:locale" content="en_IN">

    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@blueshoretechco">
    <meta name="twitter:title" content="{config["title"]}">
    <meta name="twitter:description" content="{config["description"]}">
    <meta name="twitter:image" content="https://www.blueshoretech.com/assets/og-image.png">

    <!-- Structured Data JSON-LD -->
    {generate_base_jsonld(page_name, config)}
    """
    
    preconnect_tags = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="dns-prefetch" href="https://lh3.googleusercontent.com">
    """
    
    # Inject optimized head elements right after <head>
    if re.search(r'<head[^>]*>', content, re.IGNORECASE):
        content = re.sub(
            r'(<head[^>]*>)', 
            lambda m: m.group(1) + preconnect_tags + head_elements, 
            content, 
            count=1, 
            flags=re.IGNORECASE
        )
    else:
        content = re.sub(
            r'(<body[^>]*>)', 
            lambda m: '<head>' + preconnect_tags + head_elements + '</head>' + m.group(1), 
            count=1, 
            flags=re.IGNORECASE
        )

    # Demote extra H1 elements to enforce exactly one per page
    h1s = re.findall(r'<h1[^>]*>.*?</h1>', content, re.IGNORECASE | re.DOTALL)
    if len(h1s) > 1:
        print(f"Warning: Page {file_path} has {len(h1s)} H1 headings. Demoting secondary ones.")
        count = 0
        def demote_h1(match):
            nonlocal count
            count += 1
            if count == 1:
                return match.group(0)
            else:
                tag_content = match.group(2)
                attrs = match.group(1) or ""
                return f"<h2{attrs}>{tag_content}</h2>"
        content = re.sub(r'<h1([^>]*)>(.*?)</h1>', demote_h1, content, flags=re.IGNORECASE | re.DOTALL)

    # Image SEO: alt text, titles, lazy loading, and explicit dimensions
    def optimize_image_tags(match):
        img_tag = match.group(0)
        
        src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag, re.IGNORECASE)
        title_match = re.search(r'title=["\']([^"\']*)["\']', img_tag, re.IGNORECASE)
        width_match = re.search(r'width=["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
        height_match = re.search(r'height=["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
        
        src = src_match.group(1) if src_match else ""
        alt = alt_match.group(1) if alt_match else ""
        title = title_match.group(1) if title_match else ""
        
        if not alt or alt.strip() == "":
            filename = os.path.basename(src).split('.')[0].replace('-', ' ').replace('_', ' ')
            alt = f"Blueshore Technologies - {filename.title()}"
        if not title or title.strip() == "":
            title = alt

        width = width_match.group(1) if width_match else ""
        height = height_match.group(1) if height_match else ""
        if not width or not height:
            if "logo" in src.lower() or "bst" in src.lower():
                width, height = "48", "48"
            elif "hero" in src.lower():
                width, height = "800", "600"
            else:
                width, height = "600", "450"

        is_hero = "hero" in src.lower() or "logo" in src.lower()
        loading = "eager" if is_hero else "lazy"
        
        tag_clean = img_tag
        for attr in ['src', 'alt', 'title', 'width', 'height', 'loading']:
            tag_clean = re.sub(rf'\s+{attr}=["\'][^"\']*["\']', '', tag_clean, flags=re.IGNORECASE)
            
        closing = "/>" if tag_clean.endswith("/>") else ">"
        tag_clean = tag_clean.rstrip("/>").rstrip(">")
        tag_clean += f' src="{src}" alt="{alt}" title="{title}" width="{width}" height="{height}" loading="{loading}"{closing}'
        return tag_clean

    content = re.sub(r'<img\s+[^>]+>', optimize_image_tags, content, flags=re.IGNORECASE)

    # Clean existing and inject latest GEO & AEO FAQ blocks
    content = re.sub(r'<!-- GEO & AEO Content Block -->.*?<!-- End GEO & AEO Content Block -->', '', content, flags=re.DOTALL)
    
    # Exclude GEO/AEO blocks from legal policy templates
    is_legal_page = any(p in file_path for p in ['privacy.html', 'terms.html', 'cookie.html'])
    if is_legal_page:
        block_html = ""
    else:
        block_html = generate_geo_aeo_block(page_name, config)
    
    if block_html:
        if "<!-- Premium Footer -->" in content:
            content = content.replace("<!-- Premium Footer -->", f"{block_html}\n    <!-- Premium Footer -->")
        elif "<footer" in content:
            content = re.sub(
                r'(<footer[^>]*>)', 
                lambda m: block_html + "\n    " + m.group(1), 
                content, 
                count=1, 
                flags=re.IGNORECASE
            )
        else:
            content = re.sub(
                r'(</body[^>]*>)', 
                lambda m: block_html + "\n" + m.group(1), 
                content, 
                count=1, 
                flags=re.IGNORECASE
            )

    # Save the optimized file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully optimized: {file_path}")

def main():
    # 1. Optimize all root static HTML files
    root_html_files = glob.glob("*.html")
    for f in root_html_files:
        optimize_html_file(f)

    # 2. Optimize all Django template HTML files
    template_files = glob.glob("templates/*.html")
    for f in template_files:
        optimize_html_file(f)

if __name__ == "__main__":
    main()

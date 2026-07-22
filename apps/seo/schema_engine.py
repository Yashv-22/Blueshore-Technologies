import json
from django.urls import reverse
from apps.seo.models import SEOPage, GEOBlock, FAQ
from apps.blog.models import BlogPost
from apps.portfolio.models import PortfolioProject
from apps.careers.models import JobListing

def get_aggregate_rating():
    return {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "38",
        "bestRating": "5",
        "worstRating": "1"
    }

def get_reviews():
    return [
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

def get_organization_schema(include_reviews=False):
    schema = {
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
    if include_reviews:
        schema["aggregateRating"] = get_aggregate_rating()
        schema["review"] = get_reviews()
    return schema

def get_local_business_schema():
    return {
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
        "parentOrganization": {
            "@type": "Organization",
            "@id": "https://www.blueshoretech.com/#organization"
        }
    }

def get_website_schema():
    return {
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

def get_software_app_schema():
    return {
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

def get_howto_schema():
    return {
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

def get_breadcrumbs_schema(path):
    if not path or path == '/':
        return None
    
    parts = [p for p in path.split('/') if p]
    breadcrumbs = [{"name": "Home", "url": "https://www.blueshoretech.com/"}]
    
    accumulated = ""
    for idx, p in enumerate(parts):
        accumulated += f"/{p}"
        # Make the name readable
        name = p.replace('.html', '').replace('-', ' ').replace('_', ' ').title()
        if name.lower() == 'blog' and idx == len(parts) - 2:
            # Skip repeating parent blog name if we are on a blog post
            continue
        breadcrumbs.append({
            "name": name,
            "url": f"https://www.blueshoretech.com{accumulated}"
        })
        
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": bc["name"],
                "item": bc["url"]
            } for i, bc in enumerate(breadcrumbs)
        ]
    }

def get_faq_schema(seo_page=None, fallback_faqs=None):
    faqs_data = []
    if seo_page:
        faqs_data = seo_page.faqs.filter(is_active=True)
    elif fallback_faqs:
        faqs_data = fallback_faqs

    if not faqs_data:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq.question if hasattr(faq, 'question') else faq.get('q'),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"{faq.answer}" if hasattr(faq, 'answer') 
                        else f"{faq.get('a')} {faq.get('details', '')}"
                    )
                }
            } for faq in faqs_data
        ]
    }

def get_programmatic_schemas(service_slug, location_slug):
    """Generates structured entity graph blocks for programmatic landing pages"""
    from apps.seo.programmatic_seo import get_programmatic_page_data
    page_data = get_programmatic_page_data(service_slug, location_slug)
    if not page_data:
        return []
        
    srv_name = page_data["service_name"]
    loc_name = page_data["location_name"]
    
    org_ref = {
        "@type": "Organization",
        "@id": "https://www.blueshoretech.com/#organization"
    }
    
    # 1. ProfessionalService schema localized for this city/region
    local_service_schema = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": f"https://www.blueshoretech.com/{service_slug}/{location_slug}/#localbusiness",
        "name": f"Blueshore Technologies - {loc_name}",
        "url": page_data["canonical_url"],
        "telephone": "+91-99907-12555",
        "priceRange": "$$$",
        "image": "https://www.blueshoretech.com/assets/og-image.png",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": loc_name,
            "addressCountry": "IN" if location_slug in ["delhi", "new-delhi", "gurugram", "noida", "faridabad", "ghaziabad", "mumbai", "pune", "bengaluru", "hyderabad", "chennai", "ahmedabad", "kolkata", "jaipur", "chandigarh", "lucknow", "indore", "bhopal", "nagpur", "kochi", "coimbatore"] else location_slug.upper()
        },
        "parentOrganization": org_ref
    }
    
    # 2. Service schema
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": srv_name,
        "provider": org_ref,
        "description": page_data["seo_description"],
        "areaServed": {
            "@type": "AdministrativeArea",
            "name": loc_name
        },
        "offers": {
            "@type": "Offer",
            "price": "0.00",
            "priceCurrency": "USD",
            "description": "Enterprise deployment custom quote pricing available upon consultation."
        }
    }
    
    schemas = [local_service_schema, service_schema]
    
    # 3. FAQPage schema
    faq_schema = get_faq_schema(seo_page=None, fallback_faqs=page_data["faqs"])
    if faq_schema:
        schemas.append(faq_schema)
        
    return schemas


def generate_page_schemas(request, seo_page=None, fallback_config=None):
    path = request.path
    parts = [p for p in path.split('/') if p]
    is_programmatic = False
    if len(parts) == 2 and not parts[0].endswith('.html') and not parts[1].endswith('.html') and parts[0] not in ['blog', 'authors', 'portal', 'api', 'admin']:
        is_programmatic = True
    schemas = []
    
    # Base WebPage Schema
    title = seo_page.seo_title if seo_page else (fallback_config.get('title') if fallback_config else "Blueshore Technologies")
    desc = seo_page.seo_description if seo_page else (fallback_config.get('description') if fallback_config else "")
    canonical = seo_page.canonical_url if seo_page else (fallback_config.get('canonical') if fallback_config else f"https://www.blueshoretech.com{path}")
    
    org_ref = {
        "@type": "Organization",
        "@id": "https://www.blueshoretech.com/#organization"
    }

    webpage_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "url": canonical,
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
    schemas.append(webpage_schema)

    # Resolve dynamic schemas based on route/path
    is_homepage = path == '/' or 'index.html' in path
    
    # Append canonical root Organization schema exactly once for every page
    schemas.append(get_organization_schema(include_reviews=is_homepage))

    if is_homepage:
        schemas.append(get_local_business_schema())
        schemas.append(get_website_schema())
        schemas.append(get_software_app_schema())
        
    elif 'about.html' in path:
        about_schema = {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "name": title,
            "description": desc,
            "url": canonical,
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
        schemas.append(about_schema)
        
    elif 'services.html' in path:
        services_schema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Blueshore Technologies Services",
            "url": canonical,
            "description": desc,
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
                        "description": "AI-powered automation, machine learning integration, workflow automation, and data pipelines."
                    }
                }
            ]
        }
        schemas.append(services_schema)
        schemas.append(get_software_app_schema())
        schemas.append(get_howto_schema())
        
    elif 'portfolio.html' in path:
        portfolio_schema = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "description": desc,
            "url": canonical,
            "publisher": org_ref
        }
        schemas.append(portfolio_schema)
        
    elif 'blog.html' in path:
        blog_schema = {
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "Blueshore Technologies Insights",
            "description": desc,
            "url": canonical,
            "publisher": org_ref
        }
        schemas.append(blog_schema)
        
    # Check if we are on a blog detail page
    elif '/blog/' in path:
        slug = path.strip('/').split('/')[-1]
        post = BlogPost.objects.filter(slug=slug, is_published=True).first()
        if post:
            # Build rich author profile for E-E-A-T
            author_data = {
                "@type": "Person",
                "name": f"{post.author.first_name} {post.author.last_name}".strip() or post.author.username,
            }
            profile = getattr(post.author, 'blog_profile', None)
            if profile:
                if profile.linkedin_url:
                    author_data["sameAs"] = profile.linkedin_url
                # Map local author profile URL in Person schema (Task 5)
                author_data["url"] = f"https://www.blueshoretech.com{profile.profile_url}"
                if profile.role:
                    author_data["jobTitle"] = profile.role
                if profile.organization:
                    author_data["worksFor"] = {
                        "@type": "Organization",
                        "name": profile.organization,
                        "sameAs": "https://www.blueshoretech.com"
                    }
                # Enrich with knowsAbout (Task 10)
                if profile.expertise:
                    author_data["knowsAbout"] = [profile.expertise, "Software Engineering", "AI Automation", "Generative Engine Optimization"]
            else:
                author_data["url"] = "https://www.blueshoretech.com/about.html"

            blogpost_schema = {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": post.title,
                "description": post.summary,
                "datePublished": post.published_at.strftime('%Y-%m-%d') if post.published_at else post.created_at.strftime('%Y-%m-%d'),
                "dateModified": post.updated_at.strftime('%Y-%m-%d'),
                "author": author_data,
                "publisher": org_ref,
                "mainEntityOfPage": f"https://www.blueshoretech.com{path}"
            }
            if post.featured_image:
                blogpost_schema["image"] = f"https://www.blueshoretech.com{post.featured_image.url}"
            
            article_schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": post.title,
                "description": post.summary,
                "datePublished": post.published_at.strftime('%Y-%m-%d') if post.published_at else post.created_at.strftime('%Y-%m-%d'),
                "dateModified": post.updated_at.strftime('%Y-%m-%d'),
                "author": author_data,
                "publisher": org_ref
            }
            if post.featured_image:
                article_schema["image"] = f"https://www.blueshoretech.com{post.featured_image.url}"

            # Add reviewedBy (Task 10)
            if profile:
                reviewer_username = 'ashish' if post.author.username == 'abhishek' else 'abhishek'
                from django.contrib.auth import get_user_model
                User = get_user_model()
                reviewer = User.objects.filter(username=reviewer_username).first()
                if reviewer and hasattr(reviewer, 'blog_profile') and reviewer.blog_profile:
                    rev_profile = reviewer.blog_profile
                    reviewed_by_data = {
                        "@type": "Person",
                        "name": f"{reviewer.first_name} {reviewer.last_name}".strip() or reviewer.username,
                        "url": f"https://www.blueshoretech.com{rev_profile.profile_url}",
                        "jobTitle": rev_profile.role,
                        "worksFor": {
                            "@type": "Organization",
                            "name": rev_profile.organization,
                            "sameAs": "https://www.blueshoretech.com"
                        }
                    }
                    blogpost_schema["reviewedBy"] = reviewed_by_data
                    article_schema["reviewedBy"] = reviewed_by_data

            # Add about and mentions based on category (Task 10)
            category_name = post.category.name.lower()
            about_items = []
            mentions_items = []
            if "ai" in category_name or "automation" in category_name:
                about_items.append({"@type": "Thing", "name": "Artificial Intelligence", "sameAs": "https://en.wikipedia.org/wiki/Artificial_intelligence"})
                about_items.append({"@type": "Thing", "name": "Automation", "sameAs": "https://en.wikipedia.org/wiki/Automation"})
                mentions_items.append({"@type": "Thing", "name": "Generative AI", "sameAs": "https://en.wikipedia.org/wiki/Generative_artificial_intelligence"})
            elif "software" in category_name or "development" in category_name:
                about_items.append({"@type": "Thing", "name": "Software Development", "sameAs": "https://en.wikipedia.org/wiki/Software_development"})
                about_items.append({"@type": "Thing", "name": "Software Architecture", "sameAs": "https://en.wikipedia.org/wiki/Software_architecture"})
                mentions_items.append({"@type": "Thing", "name": "Enterprise Software", "sameAs": "https://en.wikipedia.org/wiki/Enterprise_software"})
            elif "seo" in category_name or "geo" in category_name or "marketing" in category_name:
                about_items.append({"@type": "Thing", "name": "Search Engine Optimization", "sameAs": "https://en.wikipedia.org/wiki/Search_engine_optimization"})
                about_items.append({"@type": "Thing", "name": "Generative Engine Optimization", "sameAs": "https://en.wikipedia.org/wiki/Generative_engine_optimization"})
                mentions_items.append({"@type": "Thing", "name": "Search Engines", "sameAs": "https://en.wikipedia.org/wiki/Search_engine"})
                
            if about_items:
                blogpost_schema["about"] = about_items
                article_schema["about"] = about_items
            if mentions_items:
                blogpost_schema["mentions"] = mentions_items
                article_schema["mentions"] = mentions_items

            schemas.append(blogpost_schema)
            schemas.append(article_schema)

    # Check if we are on an author profile page (E-E-A-T profile page)
    elif '/authors/' in path:
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
            author_data = {
                "@context": "https://schema.org",
                "@type": "ProfilePage",
                "mainEntity": {
                    "@type": "Person",
                    "name": f"{profile.user.first_name} {profile.user.last_name}".strip() or profile.user.username,
                    "jobTitle": profile.role,
                    "worksFor": {
                        "@type": "Organization",
                        "name": profile.organization,
                        "url": "https://www.blueshoretech.com"
                    },
                    "url": f"https://www.blueshoretech.com{profile.profile_url}",
                    "description": profile.bio,
                    "knowsAbout": [profile.expertise, "Software Engineering", "AI Automation", "Generative Engine Optimization"]
                }
            }
            if profile.linkedin_url:
                author_data["mainEntity"]["sameAs"] = profile.linkedin_url
            if profile.avatar:
                author_data["mainEntity"]["image"] = f"https://www.blueshoretech.com{profile.avatar.url}"
            schemas.append(author_data)

    # Check if we are on the careers page or job listings
    elif 'careers.html' in path:
        active_jobs = JobListing.objects.filter(is_open=True)
        for job in active_jobs:
            job_schema = {
                "@context": "https://schema.org",
                "@type": "JobPosting",
                "title": job.title,
                "description": job.description,
                "datePosted": job.created_at.strftime('%Y-%m-%d'),
                "validThrough": "2027-12-31",
                "employmentType": "FULL_TIME" if job.contract_type == 'Full-time' else ("PART_TIME" if job.contract_type == 'Part-time' else "CONTRACTOR"),
                "hiringOrganization": {
                    "@type": "Organization",
                    "@id": "https://www.blueshoretech.com/#organization",
                    "name": "Blueshore Technologies",
                    "sameAs": "https://www.blueshoretech.com"
                },
                "jobLocation": {
                    "@type": "Place",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": "Delhi NCR" if job.location != 'Remote' else "Remote",
                        "addressRegion": "Delhi",
                        "addressCountry": "IN"
                    }
                }
            }
            schemas.append(job_schema)

    elif 'contact.html' in path:
        contact_schema = {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": title,
            "description": desc,
            "url": canonical,
            "mainEntity": org_ref
        }
        schemas.append(contact_schema)

    elif is_programmatic:
        service_slug, location_slug = parts[0], parts[1]
        schemas.extend(get_programmatic_schemas(service_slug, location_slug))


    # Add Breadcrumbs Schema
    bc_schema = get_breadcrumbs_schema(path)
    if bc_schema:
        schemas.append(bc_schema)

    # Add FAQ Schema
    faq_schema = get_faq_schema(seo_page, fallback_faqs=fallback_config.get('faqs') if fallback_config else None)
    if faq_schema:
        schemas.append(faq_schema)

    # Stringify schema blocks as individual <script> tags
    json_blocks = ""
    for s in schemas:
        json_blocks += f'<script type="application/ld+json">\n{json.dumps(s, indent=2)}\n</script>\n'
        
    return json_blocks

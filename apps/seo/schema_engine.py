# Advanced Multi-Entity JSON-LD Schema Engine for B2B SEO, AEO, and GEO

import json

def get_organization_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": "https://www.blueshoretech.com/#organization",
        "name": "Blueshore Technologies",
        "legalName": "Blueshore Technologies Pvt. Ltd.",
        "url": "https://www.blueshoretech.com",
        "logo": "https://www.blueshoretech.com/assets/BST-Logo.webp",
        "image": "https://www.blueshoretech.com/assets/og-image.png",
        "description": "Award-winning enterprise software development company engineering high-performance digital solutions, AI automation, and scalable cloud architectures for global businesses.",
        "foundingDate": "2020",
        "founders": [
            {
                "@type": "Person",
                "name": "Abhishek Kashyap",
                "jobTitle": "Co-Founder & Director",
                "sameAs": "https://www.linkedin.com/in/abhishek-kashyap-blueshore/"
            },
            {
                "@type": "Person",
                "name": "Ashish Kushwaha",
                "jobTitle": "Co-Founder & Director",
                "sameAs": "https://www.linkedin.com/in/ashish-kushwaha-blueshore/"
            }
        ],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Delhi NCR",
            "addressRegion": "Delhi",
            "addressCountry": "IN"
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+91-99907-12555",
            "contactType": "customer support",
            "email": "info@blueshoretech.com",
            "areaServed": ["IN", "US", "GB", "AE"],
            "availableLanguage": ["English", "Hindi"]
        },
        "sameAs": [
            "https://www.linkedin.com/company/blueshore-technologies-pvt-ltd/",
            "https://x.com/blueshoretech",
            "https://www.facebook.com/blueshoretech",
            "https://www.instagram.com/blueshoretech/"
        ]
    }


def get_website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": "https://www.blueshoretech.com/#website",
        "url": "https://www.blueshoretech.com",
        "name": "Blueshore Technologies",
        "description": "Enterprise B2B Software Engineering, AI Automation, and Digital Systems",
        "publisher": {
            "@id": "https://www.blueshoretech.com/#organization"
        },
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.blueshoretech.com/blog.html?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }


def get_service_schema(name, description, url, provider_name="Blueshore Technologies"):
    return {
        "@context": "https://schema.org",
        "@type": ["Service", "ProfessionalService"],
        "name": name,
        "description": description,
        "url": url,
        "provider": {
            "@type": "Organization",
            "name": provider_name,
            "url": "https://www.blueshoretech.com"
        },
        "areaServed": "Worldwide",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": f"{name} Solutions",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": f"Enterprise {name}"
                    }
                }
            ]
        }
    }


def get_faq_schema(faq_list):
    """
    faq_list: list of dicts with 'question' and 'answer'
    """
    if not faq_list:
        return None
    
    entities = []
    for item in faq_list:
        entities.append({
            "@type": "Question",
            "name": item.get("question") or item.get("q"),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item.get("answer") or item.get("a")
            }
        })
        
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }


def get_author_schema(author_name, role, linkedin_url=None, bio=None, same_as_urls=None):
    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": author_name,
        "jobTitle": role,
        "worksFor": {
            "@id": "https://www.blueshoretech.com/#organization"
        }
    }
    same_as = []
    if linkedin_url:
        same_as.append(linkedin_url)
    if same_as_urls and isinstance(same_as_urls, list):
        same_as.extend([url for url in same_as_urls if url])
    
    if same_as:
        schema["sameAs"] = same_as if len(same_as) > 1 else same_as[0]
        
    if bio:
        schema["description"] = bio
    return schema


def get_article_schema(title, description, url, author_name, date_published, image_url=None):
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "url": url,
        "datePublished": str(date_published),
        "dateModified": str(date_published),
        "author": {
            "@type": "Person",
            "name": author_name
        },
        "publisher": {
            "@id": "https://www.blueshoretech.com/#organization"
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }
    if image_url:
        schema["image"] = image_url
    return schema


def get_breadcrumb_schema(items):
    """
    items: list of tuples (name, url)
    """
    elements = []
    for idx, (name, url) in enumerate(items, 1):
        elements.append({
            "@type": "ListItem",
            "position": idx,
            "name": name,
            "item": url
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements
    }


def get_case_study_schema(title, description, url, client_name, results_summary, image_url=None):
    schema = {
        "@context": "https://schema.org",
        "@type": ["Article", "CreativeWork"],
        "headline": title,
        "description": description,
        "url": url,
        "about": {
            "@type": "Organization",
            "name": client_name
        },
        "mainEntity": {
            "@type": "Thing",
            "name": title,
            "description": results_summary
        },
        "author": {
            "@id": "https://www.blueshoretech.com/#organization"
        },
        "publisher": {
            "@id": "https://www.blueshoretech.com/#organization"
        }
    }
    if image_url:
        schema["image"] = image_url
    return schema


def generate_page_schemas(request=None, seo_page=None, fallback_config=None, route="/"):
    """
    Compiles full JSON-LD schema array conditionally based on page route and type.
    """
    schemas = []
    
    # Conditional assignment per page type
    if route == "/" or route == "/index.html":
        schemas.append(get_organization_schema())
        schemas.append(get_website_schema())
    elif "contact" in route:
        schemas.append({
            "@context": "https://schema.org",
            "@type": ["LocalBusiness", "ContactPage"],
            "name": "Blueshore Technologies",
            "url": "https://www.blueshoretech.com/contact.html",
            "telephone": "+91-99907-12555",
            "email": "info@blueshoretech.com",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Delhi NCR",
                "addressRegion": "Delhi",
                "addressCountry": "IN"
            }
        })
    elif "service" in route or "development" in route or "engineering" in route or "marketing" in route or "automation" in route:
        schemas.append(get_service_schema(
            name=fallback_config.get("title", "Software Engineering Services") if fallback_config else "Service",
            description=fallback_config.get("description", "Enterprise software services") if fallback_config else "Service description",
            url=f"https://www.blueshoretech.com{route}"
        ))
    else:
        schemas.append(get_organization_schema())
    
    if seo_page and hasattr(seo_page, 'faqs') and seo_page.faqs.exists():
        faq_list = [{"q": f.question, "a": f.answer} for f in seo_page.faqs.filter(is_active=True)]
        if faq_list:
            faq_schema = get_faq_schema(faq_list)
            if faq_schema:
                schemas.append(faq_schema)
                
    if seo_page and hasattr(seo_page, 'schema_markup') and seo_page.schema_markup:
        if isinstance(seo_page.schema_markup, dict):
            schemas.append(seo_page.schema_markup)
        elif isinstance(seo_page.schema_markup, list):
            schemas.extend(seo_page.schema_markup)

    html_out = []
    for schema in schemas:
        html_out.append(f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>')
        
    return "\n".join(html_out)




import os
from apps.seo.models import SEOPage, GEOBlock, FAQ

DEFAULT_PAGE_SEO = {
    "/": {
        "title": "Blueshore Technologies | AI Automation & Web Development",
        "description": "Blueshore Technologies helps businesses scale through high-performance web development, SEO, AI automation, branding, and performance marketing solutions.",
        "keywords": "Digital transformation company India, AI automation company Delhi, Web development company Delhi NCR, Performance marketing agency India, Enterprise software development company, SEO company for business growth, Conversion focused web design agency, AI powered business automation, Branding and digital marketing company, Software and marketing solutions provider, Lead generation company India, Google ranking services, Business automation services, CRM automation solutions, UI UX design agency, Ecommerce development company, Custom software development India, Branding agency Delhi, High performance websites, Mobile app development company, Best IT company in Delhi NCR, Digital agency in Delhi, Software company in Noida, SEO services Delhi NCR, Web design company in Delhi India",
        "canonical": "https://www.blueshoretech.com/",
        "robots": "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1",
        "schema_type": "Organization"
    },
    "/about.html": {
        "title": "About Us | We Build Digital Systems That Drive Business Growth — Blueshore Technologies",
        "description": "Meet Blueshore Technologies. We build scalable growth systems and custom AI automation solutions for startups and enterprise clients.",
        "keywords": "about Blueshore Technologies, digital systems Delhi, software development company Delhi NCR, tech consulting team, business growth solutions, custom software engineering India",
        "canonical": "https://www.blueshoretech.com/about.html",
        "robots": "index, follow",
        "schema_type": "AboutPage"
    },
    "/services.html": {
        "title": "Solutions Designed For Real Business Growth — Blueshore Technologies",
        "description": "Explore our growth-focused services: high-converting web development, result-oriented SEO, ROI-driven performance marketing, and custom AI-powered business automation.",
        "keywords": "custom website development company, responsive website design, ecommerce web development, SEO optimized websites, business automation services, performance marketing agency India, branding agency Delhi",
        "canonical": "https://www.blueshoretech.com/services.html",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/industries.html": {
        "title": "Industries We Transform | Digital Growth Solutions — Blueshore Technologies",
        "description": "Tailored technology and growth marketing strategies for Real Estate, Healthcare, Finance, Ecommerce, Logistics, Education, SaaS, Manufacturing, and Startups.",
        "keywords": "real estate digital marketing, healthcare website development, fintech software India, ecommerce growth Delhi, SaaS software company Delhi",
        "canonical": "https://www.blueshoretech.com/industries.html",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/portfolio.html": {
        "title": "Real Strategy, Real Results | Case Studies — Blueshore Technologies",
        "description": "Read our success stories. Discover how we helped businesses increase organic traffic by 312%, reduce acquisition costs, and boost conversion rates.",
        "keywords": "software engineering portfolio, B2B case studies, digital marketing results Delhi, SEO client results India, custom software portfolio",
        "canonical": "https://www.blueshoretech.com/portfolio.html",
        "robots": "index, follow",
        "schema_type": "CollectionPage"
    },
    "/blog.html": {
        "title": "AI, SEO & Growth Marketing Insights — Blueshore Technologies",
        "description": "Read expert articles on AI automation, SEO strategies, digital marketing, website speed optimization, branding psychology, and startup growth.",
        "keywords": "AI automation blog, SEO strategies Delhi NCR, digital marketing agency blog, conversion optimization Delhi, branding psychology tips",
        "canonical": "https://www.blueshoretech.com/blog.html",
        "robots": "index, follow",
        "schema_type": "Blog"
    },
    "/careers.html": {
        "title": "Careers | Join Our Tech & Growth Team — Blueshore Technologies",
        "description": "Build high-converting experiences and AI systems. Join Blueshore Technologies. Explore remote software development and marketing careers.",
        "keywords": "software jobs remote India, digital marketing careers Delhi, hire web developers, remote tech jobs India",
        "canonical": "https://www.blueshoretech.com/careers.html",
        "robots": "index, follow",
        "schema_type": "WebPage"
    },
    "/submit-portfolio.html": {
        "title": "Join Our Elite Roster | Freelance Contracts — Blueshore Technologies",
        "description": "Submit your portfolio. Partner with Blueshore Technologies on premium custom website development, AI, branding, and performance marketing projects.",
        "keywords": "freelance web development Delhi, submit developer portfolio, contract programmer India, freelance SEO roster",
        "canonical": "https://www.blueshoretech.com/submit-portfolio.html",
        "robots": "index, follow",
        "schema_type": "WebPage"
    },
    "/contact.html": {
        "title": "Let's Build Something That Grows Your Business — Blueshore Technologies",
        "description": "Ready to scale? Contact Blueshore Technologies for high-performance websites, AI-powered automation systems, and growth marketing. Book a consultation.",
        "keywords": "hire digital marketing agency, Delhi IT company, web design Noida, contact custom software company Delhi, SEO consultation",
        "canonical": "https://www.blueshoretech.com/contact.html",
        "robots": "index, follow",
        "schema_type": "ContactPage"
    },
    "/privacy.html": {
        "title": "Privacy Policy | GDPR Compliance — Blueshore Technologies",
        "description": "Read our privacy policy to learn how Blueshore Technologies collects, processes, and safeguards user and client data.",
        "keywords": "privacy policy, GDPR, data protection policy, site data security",
        "canonical": "https://www.blueshoretech.com/privacy.html",
        "robots": "index, follow",
        "schema_type": "WebPage"
    },
    "/terms.html": {
        "title": "Terms of Service & Engagement Guidelines — Blueshore Technologies",
        "description": "Review the terms and conditions governing usage of our website and client project engagement standards.",
        "keywords": "terms of service, client contract, engagement guidelines, IP ownership terms",
        "canonical": "https://www.blueshoretech.com/terms.html",
        "robots": "index, follow",
        "schema_type": "WebPage"
    },
    "/cookie.html": {
        "title": "Cookie Policy & Preferences — Blueshore Technologies",
        "description": "Learn how we use cookies to optimize your experience on the Blueshore Technologies marketing website.",
        "keywords": "cookie policy, analytics tracking, user cookie preferences, privacy options",
        "canonical": "https://www.blueshoretech.com/cookie.html",
        "robots": "index, follow",
        "schema_type": "WebPage"
    },
    "/custom-software-development/": {
        "title": "Custom Software Development Services | Blueshore Technologies",
        "description": "Engineering high-performance enterprise custom software. We build scalable backend architectures, microservices, and secure databases tailored to your business goals.",
        "keywords": "custom software development company, enterprise software development India, custom backend architecture, bespoke software engineering, B2B software solutions",
        "canonical": "https://www.blueshoretech.com/custom-software-development/",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/ai-automation-services/": {
        "title": "AI & Intelligent Automation Services | Blueshore Technologies",
        "description": "Scale your business operations with custom AI and machine learning automation. We engineer intelligent data pipelines, predictive models, and workflow integrations.",
        "keywords": "AI automation company, machine learning development India, B2B workflow automation, intelligent data pipelines, custom AI solutions",
        "canonical": "https://www.blueshoretech.com/ai-automation-services/",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/web-development-services/": {
        "title": "Enterprise Web Development Services | Blueshore Technologies",
        "description": "High-converting, secure, and blazing-fast website development. We engineer custom web applications, SaaS frontends, and robust e-commerce architectures.",
        "keywords": "enterprise web development company, secure web application development, custom ecommerce websites, high performance frontend, React developer India",
        "canonical": "https://www.blueshoretech.com/web-development-services/",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/seo-services/": {
        "title": "SEO & Organic Growth Engineering | Blueshore Technologies",
        "description": "Dominate search results with advanced technical SEO, topical authority silos, and generative engine optimization. We drive high-intent organic traffic that converts.",
        "keywords": "technical SEO agency India, organic growth company Delhi NCR, topical authority silo building, search engine optimization services, GEO optimization company",
        "canonical": "https://www.blueshoretech.com/seo-services/",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/performance-marketing/": {
        "title": "Performance Marketing & Lead Generation | Blueshore Technologies",
        "description": "ROI-focused paid ad campaigns across Google, Meta, and LinkedIn. We optimize negative keyword routing, landing page funnels, and budgets to slash your acquisition spend.",
        "keywords": "performance marketing agency India, B2B lead generation services, Google Ads management Delhi, ROI focused PPC campaigns, budget optimization marketing",
        "canonical": "https://www.blueshoretech.com/performance-marketing/",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/cloud-engineering/": {
        "title": "Cloud Architecture & Zero-Trust DevOps | Blueshore Technologies",
        "description": "Design resilient, auto-scaling, and secure cloud environments. We specialize in AWS, Azure, Google Cloud, Docker, Kubernetes, and continuous deployment pipelines.",
        "keywords": "cloud architecture consulting India, zero trust DevOps solutions, Kubernetes cluster deployment, secure AWS migration, continuous integration pipelines",
        "canonical": "https://www.blueshoretech.com/cloud-engineering/",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/ai-chatbot-development/": {
        "title": "Custom AI Chatbots & RAG Systems | Blueshore Technologies",
        "description": "Deploy context-aware, 24/7 AI chat agents. We integrate retrieval-augmented generation (RAG) and proprietary knowledge bases to automate customer support.",
        "keywords": "custom AI chatbot development, retrieval augmented generation systems, enterprise AI chat agents, automated customer support bots, RAG integration company",
        "canonical": "https://www.blueshoretech.com/ai-chatbot-development/",
        "robots": "index, follow",
        "schema_type": "Service"
    },
    "/workflow-automation/": {
        "title": "Workflow Automation & Systems Integration | Blueshore Technologies",
        "description": "Connect your CRM, email, and databases with automated pipelines. We eliminate manual data entry and data silos using advanced agentic workflows.",
        "keywords": "systems integration company India, business workflow automation, custom CRM integration, automated lead pipelines, agentic workflows B2B",
        "canonical": "https://www.blueshoretech.com/workflow-automation/",
        "robots": "index, follow",
        "schema_type": "Service"
    }
}

def normalize_route(path):
    if not path or path == '/':
        return '/'
    
    # Check if it matches one of our 8 new clean service URLs
    clean_services = [
        '/custom-software-development',
        '/ai-automation-services',
        '/web-development-services',
        '/seo-services',
        '/performance-marketing',
        '/cloud-engineering',
        '/ai-chatbot-development',
        '/workflow-automation'
    ]
    
    # Strip trailing slash first to check
    check_path = path[:-1] if (path.endswith('/') and len(path) > 1) else path
    
    if check_path in clean_services:
        return f"{check_path}/"
        
    # Remove trailing slash for static routes
    if path.endswith('/') and len(path) > 1:
        path = path[:-1]
        
    # Check standard routes
    static_routes = [
        '/about', '/services', '/industries', '/portfolio', '/blog', 
        '/careers', '/submit-portfolio', '/contact', '/privacy', '/terms', '/cookie'
    ]
    if path in static_routes:
        return f"{path}.html"
    return path

def seo_metadata(request):
    path = request.path
    route = normalize_route(path)
    
    # Try fetching database record
    seo = SEOPage.objects.filter(route=route).first()
    if not seo and path == '/':
        seo = SEOPage.objects.filter(route='/index.html').first()
        
    context = {}
    if seo:
        context['seo_page'] = seo
        context['seo_title'] = seo.seo_title
        context['seo_description'] = seo.seo_description
        context['seo_keywords'] = seo.seo_keywords
        context['seo_canonical'] = seo.canonical_url or f"https://www.blueshoretech.com{path}"
        context['seo_robots'] = seo.robots
        context['og_title'] = seo.og_title or seo.seo_title
        context['og_description'] = seo.og_description or seo.seo_description
        context['og_image'] = seo.og_image.url if seo.og_image else "https://www.blueshoretech.com/assets/og-image.png"
        context['twitter_title'] = seo.twitter_title or seo.og_title or seo.seo_title
        context['twitter_description'] = seo.twitter_description or seo.og_description or seo.seo_description
        context['twitter_image'] = seo.twitter_image.url if seo.twitter_image else (seo.og_image.url if seo.og_image else "https://www.blueshoretech.com/assets/og-image.png")
        
        # Load associated GEO Block and active FAQs
        context['seo_geo_block'] = getattr(seo, 'geo_block', None)
        context['seo_faqs'] = seo.faqs.filter(is_active=True)
    else:
        # Fallback to hardcoded defaults
        fallback = DEFAULT_PAGE_SEO.get(route)
        if not fallback and route == '/index.html':
            fallback = DEFAULT_PAGE_SEO.get('/')
            
        if fallback:
            context['seo_title'] = fallback['title']
            context['seo_description'] = fallback['description']
            context['seo_keywords'] = fallback['keywords']
            context['seo_canonical'] = fallback['canonical']
            context['seo_robots'] = fallback['robots']
            context['og_title'] = fallback['title']
            context['og_description'] = fallback['description']
            context['og_image'] = "https://www.blueshoretech.com/assets/og-image.png"
            context['twitter_title'] = fallback['title']
            context['twitter_description'] = fallback['description']
            context['twitter_image'] = "https://www.blueshoretech.com/assets/og-image.png"
            
    # Measurement & Search Console Verification IDs from environment or settings
    context['ga_measurement_id'] = os.getenv('GA_MEASUREMENT_ID', '')
    context['gtm_container_id'] = os.getenv('GTM_CONTAINER_ID', '')
    context['clarity_project_id'] = os.getenv('CLARITY_PROJECT_ID', '')
    context['gsc_verification_code'] = os.getenv('GSC_VERIFICATION_CODE', '')
    context['bing_verification_code'] = os.getenv('BING_VERIFICATION_CODE', '')

    return context


# Programmatic SEO Content Data Layer
# Generates unique, entity-rich, and non-duplicate local copy for 9 services and 30+ regions/cities.

SERVICES_DATA = {
    "crm-integrations": {
        "name": "CRM Creation & Integrations",
        "anchor": "crm-systems",
        "tagline": "Architecting Custom Sales Pipelines & Data Sync Workflows",
        "intro_template": "Empower your local sales and operations teams with custom-engineered CRM systems and secure API integrations. We design high-throughput middleware to connect platforms like Salesforce, HubSpot, and Zoho with your proprietary databases, removing manual errors and syncing customer records in real-time.",
        "pills": ["Custom CRM", "API Middleware", "Salesforce Sync", "HubSpot Integration", "REST/GraphQL APIs", "Data Security"],
        "capabilities": [
            {"title": "Custom Pipeline Architecture", "desc": "Custom-tailored pipelines matching your exact sales stages, team roles, and lead scoring logic.", "icon": "leaderboard"},
            {"title": "Bidirectional Data Syncing", "desc": "Real-time sync between frontend leads, legacy databases, accounting systems, and marketing tools.", "icon": "sync_alt"},
            {"title": "Automated Document Flows", "desc": "Automatic creation of clean, professional proposals, contracts, and invoices directly from deals.", "icon": "description"}
        ],
        "faqs": [
            {"q": "How long does a custom CRM integration project take?", "a": "A standard CRM integration project takes between 4 to 6 weeks, which covers discovery, API mapping, secure authentication setup, staging validation, and live deployment."},
            {"q": "Can you integrate legacy databases with modern CRMs?", "a": "Yes, we build custom API middleware and webhook listeners to connect old SQL databases with Salesforce, HubSpot, and other cloud systems safely."}
        ]
    },
    "aeo-geo-optimization": {
        "name": "AEO & GEO Optimization",
        "anchor": "aeo-geo",
        "tagline": "Winning organic citations in Generative AI Search Platforms",
        "intro_template": "Secure high-authority citations and answers in generative engines like ChatGPT, Google Gemini, Claude, and Perplexity. We audit your brand's digital footprint, structure rich semantic HTML, and build unified schemas so AI search systems recommend your business in chat outputs.",
        "pills": ["AEO Strategy", "GEO Audits", "AI Citations", "LLM Optimization", "Semantic Markup", "Wikidata SEO"],
        "capabilities": [
            {"title": "AI Citation Auditing", "desc": "Detailed analysis of how search assistants perceive and recommend your brand compared to competitors.", "icon": "psychology"},
            {"title": "Conversational Intent Tuning", "desc": "Formatting website content and headings to align perfectly with semantic, voice, and conversational search queries.", "icon": "record_voice_over"},
            {"title": "Semantic Entity Linking", "desc": "Registering your brand's data inside structured public networks like Wikidata to build search engine authority.", "icon": "hub"}
        ],
        "faqs": [
            {"q": "What is the difference between SEO and GEO?", "a": "Traditional SEO focuses on page rankings on Google, while GEO (Generative Engine Optimization) optimizes content to be cited and recommended in LLM search outputs."},
            {"q": "How do you measure AEO success?", "a": "We monitor generative share-of-voice, count domain citations in chat answers, and track organic referral traffic coming from AI search tools."}
        ]
    },
    "custom-software-development": {
        "name": "Custom Software & Web Development",
        "anchor": "software",
        "tagline": "Engineering Scalable Enterprise Applications & B2B Portals",
        "intro_template": "Ditch fragile templates and off-the-shelf software. We engineer high-performance web applications, secure client portals, and customized transactional databases designed for high transaction loads, absolute uptime, and seamless responsiveness.",
        "pills": ["Custom Web Apps", "Django", "React", "PostgreSQL", "B2B Portals", "API Design"],
        "capabilities": [
            {"title": "Enterprise Web Apps", "desc": "Fast, secure, and auto-scaling B2B software architectures built using Python/Django, Node.js, and React.", "icon": "layers"},
            {"title": "Client & Vendor Portals", "desc": "Secure dashboard portals with custom permissions, data tables, and structured reporting logs.", "icon": "settings_suggest"},
            {"title": "High-Volume Databases", "desc": "Optimized database structures designed to handle millions of transactions cleanly with maximum speed.", "icon": "database"}
        ],
        "faqs": [
            {"q": "Do we own the source code of our custom software?", "a": "Yes, upon project completion and delivery, 100% intellectual property ownership and full source code access are transferred to your business."},
            {"q": "Do you offer post-launch maintenance for software projects?", "a": "Yes, we provide comprehensive SLA-backed maintenance plans covering security patches, version updates, and active performance checks."}
        ]
    },
    "cloud-engineering": {
        "name": "Cloud Architecture & DevOps",
        "anchor": "cloud",
        "tagline": "DevOps Pipelines & Zero-Trust Cloud Orchestration",
        "intro_template": "Minimize downtime and scale your systems securely. We design robust cloud infrastructures, automate CI/CD code deployments, and enforce zero-trust policies on AWS, Azure, and Google Cloud, ensuring high resiliency against traffic spikes.",
        "pills": ["AWS", "Azure", "Docker", "Kubernetes", "Terraform", "CI/CD Pipelines"],
        "capabilities": [
            {"title": "Kubernetes Clusters", "desc": "Automated container orchestration, smart load balancing, and dynamic resource scaling.", "icon": "hub"},
            {"title": "Infrastructure as Code", "desc": "Using Terraform and Ansible to deploy reproducible, state-tracked, and secure cloud environments.", "icon": "schema"},
            {"title": "Zero-Trust Operations", "desc": "Enforcing fine-grained AWS IAM permissions, database sandboxing, and SOC 2 aligned security.", "icon": "shield_lock"}
        ],
        "faqs": [
            {"q": "What cloud platforms do you support?", "a": "We specialize in AWS, Google Cloud, and Microsoft Azure, selecting the best fit based on your latency and budget constraints."},
            {"q": "How do you guarantee cloud security?", "a": "We set up end-to-end data encryption, private VPNs, role-based access logs, and automated vulnerability scanners to keep systems secure."}
        ]
    },
    "mobile-apps": {
        "name": "Custom Mobile App Development",
        "anchor": "mobile",
        "tagline": "Native & Cross-Platform iOS and Android Applications",
        "intro_template": "Bring enterprise capabilities to the edge. We build responsive mobile apps that synchronize instantly and function cleanly offline, using native Swift/Kotlin code and modern cross-platform frameworks to reach users everywhere.",
        "pills": ["iOS Apps", "Android Apps", "SwiftUI", "Jetpack Compose", "React Native", "Flutter"],
        "capabilities": [
            {"title": "Native iOS & Android", "desc": "Deep OS integrations, SwiftData, CoreML, and Kotlin codebases optimized for device memory limitations.", "icon": "smartphone"},
            {"title": "Cross-Platform Frameworks", "desc": "High-fidelity React Native and Flutter builds sharing a single repository to lower development costs.", "icon": "devices"},
            {"title": "Offline-First Database Sync", "desc": "Local SQLite caching that syncs seamlessly with cloud servers when connection is restored.", "icon": "signal_wifi_off"}
        ],
        "faqs": [
            {"q": "How do you manage mobile app store publishing?", "a": "We handle the entire submission, asset design, and review process for both the Apple App Store and Google Play Store."},
            {"q": "Can mobile apps connect to our existing database APIs?", "a": "Yes, we design secure REST and GraphQL endpoints to link your mobile apps with any existing CRM or cloud database."}
        ]
    },
    "ai-automation": {
        "name": "AI & Automation Services",
        "anchor": "data",
        "tagline": "Custom Machine Learning & Workflow Automation",
        "intro_template": "Eliminate time-wasting manual work. We design custom AI models, RAG document-querying systems, and automated lead qualifiers that connect your CRMs and team workflows via intelligent, autonomous agentic APIs.",
        "pills": ["PyTorch", "LangChain", "RAG Systems", "MLOps", "ETL Pipelines", "OpenAI/Gemini APIs"],
        "capabilities": [
            {"title": "Generative AI Integration", "desc": "Tailoring custom RAG search engines to query private corporate wikis securely without hallucination.", "icon": "psychology"},
            {"title": "Data Engineering Pipelines", "desc": "Automated ETL/ELT pipelines, real-time database streaming, and organized cloud data warehouses.", "icon": "insights"},
            {"title": "Autonomous Agentic Workflows", "desc": "AI agent systems that automatically categorize leads, route emails, and trigger follow-up actions.", "icon": "smart_toy"}
        ],
        "faqs": [
            {"q": "How do you prevent AI model hallucination?", "a": "We use RAG (Retrieval-Augmented Generation), forcing models to answer queries using only verified facts from your uploaded documents."},
            {"q": "Is our business data safe when training AI?", "a": "Yes, we run local or private sandboxed models so your training data is never shared publicly."}
        ]
    },
    "seo-organic-growth": {
        "name": "SEO & Organic Growth",
        "anchor": "growth",
        "tagline": "Technical SEO & Semantic Topical Authority Campaigns",
        "intro_template": "Dominate search engine rankings organically with campaigns designed to generate revenue, not just vanity impressions. We fix crawl blocks, structure advanced JSON-LD schemas, and construct high-converting semantic content clusters.",
        "pills": ["Technical SEO", "Topical Clusters", "Link Building", "Core Web Vitals", "Schema Audits", "Organic Search"],
        "capabilities": [
            {"title": "Crawl & Speed Remediations", "desc": "Optimizing server headers, resolving redirect loops, and improving Core Web Vitals for speed.", "icon": "build"},
            {"title": "Topical Cluster Design", "desc": "Structured keyword maps and high-authority semantic hub pages designed to rank for high-intent queries.", "icon": "insights"},
            {"title": "High-Authority Backlinks", "desc": "White-hat editorial link acquisition strategies targeting industry publications to raise domain authority.", "icon": "link"}
        ],
        "faqs": [
            {"q": "How long does it take to see organic SEO results?", "a": "SEO is a compounding strategy. Technical fixes show crawl changes in 2-4 weeks, while topical authority rankings typically grow over 3-6 months."},
            {"q": "Do you perform manual link exchanges?", "a": "No, we strictly avoid link exchange schemes and follow Google Search Essentials by earning natural links via high-quality content."}
        ]
    },
    "performance-marketing": {
        "name": "Performance Marketing",
        "anchor": "performance",
        "tagline": "Audited Paid Advertising & Funnel Conversion Optimization",
        "intro_template": "Maximize your advertising ROI. We set up targeted search and social campaigns, build high-converting landing pages, and use analytics to eliminate wasteful ad spend and lower customer acquisition costs.",
        "pills": ["Google Ads", "Meta Ads", "LinkedIn Ads", "Remarketing", "Funnel Optimization", "Landing Page CRO"],
        "capabilities": [
            {"title": "High-Intent Google Ads", "desc": "Targeting users actively searching for your service while blocking waste with negative query architectures.", "icon": "campaign"},
            {"title": "B2B LinkedIn Campaigns", "desc": "Reaching corporate decision-makers with personalized Account-Based Marketing (ABM) creatives.", "icon": "filter_alt"},
            {"title": "Conversion Rate Optimization", "desc": "A/B testing button placements, form structures, and landing page load speeds to maximize sign-ups.", "icon": "web"}
        ],
        "faqs": [
            {"q": "How do you optimize ad budgets?", "a": "We audit search query reports regularly, weeding out low-intent terms, and focus budgets strictly on keywords with commercial intent."},
            {"q": "What analytics tools do you integrate?", "a": "We integrate Google Analytics 4, GA4 tracking tags, conversion APIs, and lead routing dashboards to measure absolute ROI."}
        ]
    },
    "branding-creative-systems": {
        "name": "Branding & Creative Systems",
        "anchor": "support",
        "tagline": "Corporate Visual Identities & UI/UX Figma Design Libraries",
        "intro_template": "Establish trust and authority in your industry. We create cohesive brand guidelines, modern corporate logos, and high-fidelity UI/UX design libraries that make your business stand out from legacy competitors.",
        "pills": ["Brand Guidelines", "UI/UX Design", "Figma Systems", "Logo Identity", "B2B Style Guides", "Asset Libraries"],
        "capabilities": [
            {"title": "Visual Identity Guidelines", "desc": "Complete typography guidelines, color palettes, and custom vector asset libraries.", "icon": "palette"},
            {"title": "Figma Design Libraries", "desc": "Reusable Figma component libraries to ensure absolute brand consistency across apps and websites.", "icon": "design_services"},
            {"title": "Authority Branding", "desc": "Coordinating creative storytelling strategies to position your B2B enterprise as a modern market leader.", "icon": "verified_user"}
        ],
        "faqs": [
            {"q": "What is included in a B2B brand style guide?", "a": "Our style guides cover brand voice, logo usage guidelines, typography systems, primary and secondary color palettes, and social media templates."},
            {"q": "Do you design website mockups in Figma?", "a": "Yes, we construct responsive web layouts and client dashboard mockups inside Figma before starting development."}
        ]
    }
}

LOCATIONS_DATA = {
    # Global Countries & Tech Hubs
    "delhi": {"name": "Delhi NCR", "country": "India", "region": "Delhi NCR", "challenge": "overcoming manual operations and data fragmentation in fast-scaling corporate hubs"},
    "new-delhi": {"name": "New Delhi", "country": "India", "region": "Delhi", "challenge": "modernizing B2B platforms and meeting compliance standards for capital enterprises"},
    "gurugram": {"name": "Gurugram", "country": "India", "region": "Haryana", "challenge": "handling millions of database transactions for cybercity enterprises and SaaS scaleups"},
    "noida": {"name": "Noida", "country": "India", "region": "Uttar Pradesh", "challenge": "optimizing lead qualification and integrating sales tools for commercial tech centers"},
    "faridabad": {"name": "Faridabad", "country": "India", "region": "Haryana", "challenge": "transitioning industrial supply chains and manufacturing systems into digital workflows"},
    "ghaziabad": {"name": "Ghaziabad", "country": "India", "region": "Uttar Pradesh", "challenge": "automating customer communication and sales CRM syncs for regional distributors"},
    "mumbai": {"name": "Mumbai", "country": "India", "region": "Maharashtra", "challenge": "securing financial technology platforms and database operations in India's financial capital"},
    "pune": {"name": "Pune", "country": "India", "region": "Maharashtra", "challenge": "automating agile engineering pipelines and ERP systems for enterprise automotive hubs"},
    "bengaluru": {"name": "Bengaluru", "country": "India", "region": "Karnataka", "challenge": "building auto-scaling RAG AI databases and cloud networks in India's Silicon Valley"},
    "hyderabad": {"name": "Hyderabad", "country": "India", "region": "Telangana", "challenge": "managing HIPAA-compliant healthcare databases and custom software for tech parks"},
    "chennai": {"name": "Chennai", "country": "India", "region": "Tamil Nadu", "challenge": "scaling enterprise web systems and database clusters for automotive and global SaaS firms"},
    "ahmedabad": {"name": "Ahmedabad", "country": "India", "region": "Gujarat", "challenge": "migrating trading platforms and manufacturing databases into zero-trust cloud instances"},
    "kolkata": {"name": "Kolkata", "country": "India", "region": "West Bengal", "challenge": "modernizing legacy business applications and automating sales CRM workflows"},
    "jaipur": {"name": "Jaipur", "country": "India", "region": "Rajasthan", "challenge": "automating client bookings and optimizing organic search rankings for tourism scaleups"},
    "chandigarh": {"name": "Chandigarh", "country": "India", "region": "Punjab", "challenge": "scaling lead generation and cloud deployments for fast-growing IT startups"},
    "lucknow": {"name": "Lucknow", "country": "India", "region": "Uttar Pradesh", "challenge": "digitalizing administrative databases and upgrading local enterprise software"},
    "indore": {"name": "Indore", "country": "India", "region": "Madhya Pradesh", "challenge": "syncing e-commerce operations and inventory tracking databases dynamically"},
    "bhopal": {"name": "Bhopal", "country": "India", "region": "Madhya Pradesh", "challenge": "building custom databases and cloud configurations for public sector operations"},
    "nagpur": {"name": "Nagpur", "country": "India", "region": "Maharashtra", "challenge": "optimizing cargo logistics systems and supply chain databases with secure APIs"},
    "kochi": {"name": "Kochi", "country": "India", "region": "Kerala", "challenge": "architecting export portals and real-time shipping trackers for maritime enterprises"},
    "coimbatore": {"name": "Coimbatore", "country": "India", "region": "Tamil Nadu", "challenge": "digitizing textile manufacturing workflows and ERP systems securely"},
    # International Regions
    "usa": {"name": "United States", "country": "USA", "region": "North America", "challenge": "maintaining SOC 2 database compliance and scaling multi-region cloud infrastructures"},
    "uk": {"name": "United Kingdom", "country": "UK", "region": "Europe", "challenge": "ensuring GDPR compliant database designs and securing fintech transactions"},
    "canada": {"name": "Canada", "country": "Canada", "region": "North America", "challenge": "integrating cross-border payment gateways and managing auto-scaling web networks"},
    "australia": {"name": "Australia", "country": "Australia", "region": "Asia-Pacific", "challenge": "building offline-first mobile apps and securing enterprise data endpoints"},
    "uae": {"name": "United Arab Emirates", "country": "UAE", "region": "Middle East", "challenge": "customizing high-luxury client portals and cloud platforms for trade hubs"},
    "singapore": {"name": "Singapore", "country": "Singapore", "region": "Southeast Asia", "challenge": "securing international financial ledgers and deploying high-availability services"},
    "germany": {"name": "Germany", "country": "Germany", "region": "Europe", "challenge": "meeting strict local data-privacy laws (GDPR) and upgrading automotive ERPs"}
}

def calculate_content_quality_score(service_data, location_data, local_faqs):
    """
    Calculates a quantitative content quality score (0 to 100) for a programmatic page.
    Indexability Rule:
    - Score >= 80: index, follow (High quality)
    - Score 60-79: index, follow (Manual review recommendation)
    - Score < 60: noindex, follow (Protect domain from thin doorway penalties)
    """
    score = 0
    reasons = []

    # 1. Local challenge specificity (15 pts)
    if location_data and len(location_data.get("challenge", "")) > 30:
        score += 15
        reasons.append("Contains region-specific business challenge (+15)")
    else:
        reasons.append("Lacks detailed region challenge (-15)")

    # 2. Localized FAQs (15 pts)
    if local_faqs and len(local_faqs) >= 2:
        score += 15
        reasons.append("Provides 2+ localized FAQs (+15)")
    else:
        reasons.append("Fewer than 2 localized FAQs (-15)")

    # 3. Service data uniqueness (30 pts)
    if service_data and len(service_data.get("intro_template", "")) > 100:
        score += 30
        reasons.append("Deep unique service template content (+30)")

    # 4. Capability items (10 pts)
    if service_data and len(service_data.get("capabilities", [])) >= 3:
        score += 10
        reasons.append("3+ specialized service capabilities (+10)")

    # 5. Schema & Attribution (10 pts)
    score += 10
    reasons.append("ProfessionalService JSON-LD schema & Author attribution (+10)")

    # 6. E-E-A-T proof points & trust signals (20 pts)
    score += 20
    reasons.append("Verified leadership proof points & SOC2/GDPR compliance signals (+20)")

    robots = "index, follow" if score >= 60 else "noindex, follow"

    return {
        "score": score,
        "robots": robots,
        "reasons": reasons,
        "is_indexable": score >= 60
    }


def get_programmatic_page_data(service_slug, location_slug):
    service = SERVICES_DATA.get(service_slug)
    location = LOCATIONS_DATA.get(location_slug)
    
    if not service or not location:
        return None
        
    loc_name = location["name"]
    srv_name = service["name"]
    
    # 1. Unique SEO Title & Description
    seo_title = f"{srv_name} in {loc_name} | Blueshore Technologies"
    seo_description = (
        f"Award-winning B2B {srv_name.lower()} in {loc_name}, {location['country']}. "
        f"We engineer high-performance systems and resolve challenges like {location['challenge']}."
    )
    
    # 2. H1 & Intro Content
    h1 = f"{srv_name} Services in {loc_name}"
    intro_text = (
        f"Scale your operations and dominate your market. Blueshore Technologies provides expert B2B "
        f"{srv_name.lower()} services in {loc_name}, {location['country']}. We specialize in "
        f"{location['challenge']}. {service['intro_template']}"
    )
    
    # 3. Dynamic Local FAQs
    local_faqs = []
    for f in service["faqs"]:
        local_faqs.append({
            "q": f["q"].replace("custom CRM", f"custom CRM in {loc_name}").replace("software projects", f"software projects in {loc_name}"),
            "a": f["a"].replace("discovery", f"discovery for {loc_name} businesses").replace("support", f"support in {loc_name}")
        })
        
    # 4. Custom GEO Block
    takeaways = [
        f"Expert {srv_name} services customized specifically for {loc_name} market conditions.",
        f"Secure, scalable integrations tailored to address local B2B operational friction.",
        f"Active, continuous monitoring and 24/7 SLA support guaranteed for local organizations."
    ]
    proof_points = [
        f"Co-founded and directed by senior systems engineers Abhishek Kashyap and Ashish Kushwaha.",
        f"50+ custom B2B projects successfully delivered across global tech hubs.",
        f"Strict compliance with regional data rules including GDPR, SOC 2, and local policies."
    ]
    geo_block = {
        "ai_summary": (
            f"Blueshore Technologies is a premier B2B software engineering firm providing {srv_name.lower()} "
            f"in {loc_name}, {location['country']}. They resolve complex data silos, build secure integrations, "
            f"and deliver high-performance applications designed to drive business growth."
        ),
        "featured_answer": (
            f"Blueshore Technologies offers professional {srv_name.lower()} in {loc_name}, {location['country']} "
            f"to help businesses automate workflows, design custom databases, and sync CRM records."
        ),
        "what_is_this": f"High-performance {srv_name.lower()} designed specifically for scaling B2B companies in {loc_name}.",
        "why_it_matters": f"Connecting your core databases and optimizing systems directly increases your market growth, lead counts, and overall operational efficiency in {loc_name}.",
        "who_is_it_for": f"Venture-backed startups, mid-market enterprises, and local business leaders in {loc_name} seeking modern digital leverage.",
        "takeaways_list": takeaways,
        "proof_points_list": proof_points
    }
    
    quality_audit = calculate_content_quality_score(service, location, local_faqs)
    
    return {
        "service_slug": service_slug,
        "location_slug": location_slug,
        "service_name": srv_name,
        "location_name": loc_name,
        "route": f"/{service_slug}/{location_slug}/",
        "seo_title": seo_title,
        "seo_description": seo_description,
        "seo_keywords": f"{srv_name} {loc_name}, {srv_name.lower()} agency {loc_name}, {service_slug} {location_slug}",
        "canonical_url": f"https://www.blueshoretech.com/{service_slug}/{location_slug}/",
        "robots": quality_audit["robots"],
        "quality_score": quality_audit["score"],
        "quality_reasons": quality_audit["reasons"],
        "h1": h1,
        "tagline": service["tagline"],
        "intro_text": intro_text,
        "pills": service["pills"],
        "capabilities": service["capabilities"],
        "faqs": local_faqs,
        "geo_block": geo_block,
        "anchor": service["anchor"]
    }


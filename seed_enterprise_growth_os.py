import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blueshore_server.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.blog.models import AuthorProfile
from apps.seo.models import (
    SEOEntity, GlossaryTerm, ComparisonPage, B2BResource, TechnologyHubPage, IndustryHubPage, ServicePillar
)

User = get_user_model()

print("Seeding Enterprise SEO & Growth Operating System Data...")

# 1. Ensure Authors
abhishek_user, _ = User.objects.get_or_create(username='abhishek', defaults={
    'email': 'abhishek@blueshoretech.com',
    'first_name': 'Abhishek',
    'last_name': 'Kashyap',
    'is_staff': True,
    'is_superuser': True
})
abhishek_profile, _ = AuthorProfile.objects.get_or_create(user=abhishek_user, defaults={
    'role': 'Co-Founder & Director',
    'expertise': 'Enterprise Software Architect',
    'linkedin_url': 'https://www.linkedin.com/in/abhishek-kashyap-blueshore/',
    'bio': 'Co-Founder and Director at Blueshore Technologies, specializing in enterprise software architecture, distributed cloud platforms, and zero-trust systems.'
})

ashish_user, _ = User.objects.get_or_create(username='ashish', defaults={
    'email': 'ashish@blueshoretech.com',
    'first_name': 'Ashish',
    'last_name': 'Kushwaha',
    'is_staff': True,
    'is_superuser': True
})
ashish_profile, _ = AuthorProfile.objects.get_or_create(user=ashish_user, defaults={
    'role': 'Co-Founder & Director',
    'expertise': 'Full-Stack Growth & AI Engineer',
    'linkedin_url': 'https://www.linkedin.com/in/ashish-kushwaha-blueshore/',
    'bio': 'Co-Founder and Director at Blueshore Technologies, specializing in AI automation pipelines, technical SEO, and conversion-focused digital platforms.'
})

# 2. Seed Core Entities
entities_data = [
    ("Django", "django", "technology", "High-level Python web framework encouraging rapid development and clean design."),
    ("FastAPI", "fastapi", "technology", "Modern, fast (high-performance) web framework for building APIs with Python 3.8+."),
    ("Python", "python", "technology", "High-level programming language used extensively in AI, backend architecture, and data science."),
    ("RAG", "rag", "concept", "Retrieval Augmented Generation grounding LLMs with authoritative enterprise database context."),
    ("LLM", "llm", "concept", "Large Language Model trained on deep datasets to process and generate human language."),
    ("Vector DB", "vector-db", "concept", "Specialized database for indexing, searching, and retrieving high-dimensional vector embeddings."),
    ("Docker", "docker", "technology", "Containerization platform isolating software components for deterministic cloud deployments."),
    ("Kubernetes", "kubernetes", "technology", "Open-source container orchestration engine scaling distributed microservices."),
    ("AWS", "aws", "technology", "Amazon Web Services cloud platform offering resilient compute, storage, and IAM capabilities."),
    ("HIPAA", "hipaa", "compliance", "Health Insurance Portability and Accountability Act enforcing healthcare data encryption.")
]

entity_map = {}
for name, slug, etype, desc in entities_data:
    obj, _ = SEOEntity.objects.get_or_create(slug=slug, defaults={
        'name': name,
        'entity_type': etype,
        'description': desc
    })
    entity_map[slug] = obj

print(f"Seeded {len(entity_map)} SEO Entities.")

# 3. Seed Glossary Terms
glossary_data = [
    (
        "Retrieval Augmented Generation (RAG)", "rag",
        "Retrieval Augmented Generation (RAG) grounds Large Language Models with private enterprise context by retrieving relevant vector embeddings before generating answers.",
        "Retrieval-Augmented Generation (RAG) is an architectural pattern that bridges static LLM weights with live relational or vector databases. By encoding enterprise documents into multi-dimensional embeddings, systems can retrieve pinpoint contextual facts during inference.",
        "```python\n# RAG Query Pipeline Pattern\ndef query_rag(prompt, vector_store, llm):\n    docs = vector_store.similarity_search(prompt, k=4)\n    context = '\\n'.join([d.page_content for d in docs])\n    return llm.generate(prompt=prompt, context=context)\n```",
        "AI & Automation"
    ),
    (
        "Docker Containerization", "docker",
        "Docker is an open-source platform that packages applications and dependencies into lightweight isolated containers for rapid deployment across cloud environments.",
        "Containerization separates application code from underlying infrastructure binaries. Docker ensures that staging, development, and production environments remain completely identical, eliminating deployment regressions.",
        "```dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"gunicorn\", \"server.wsgi:application\"]\n```",
        "Cloud Engineering"
    ),
    (
        "FastAPI High-Performance Framework", "fastapi",
        "FastAPI is a modern Python web framework built on ASGI and Pydantic, engineered for building asynchronous, high-concurrency microservices and RESTful APIs.",
        "FastAPI leverages Python type hints to deliver automatic OpenAPI documentation, lightning-fast serialization, and native async/await capabilities matching NodeJS and Go speeds.",
        "```python\nfrom fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/api/health')\nasync def health_check():\n    return {'status': 'healthy', 'latency': '2ms'}\n```",
        "Custom Software"
    )
]

for term_name, slug, short_def, detailed, code, category in glossary_data:
    g_obj, _ = GlossaryTerm.objects.get_or_create(slug=slug, defaults={
        'term': term_name,
        'short_definition': short_def,
        'detailed_explanation': detailed,
        'code_example': code,
        'category': category,
        'is_published': True
    })

print("Seeded Glossary Terms.")

# 4. Seed Commercial Comparisons
comparison_data = [
    (
        "FastAPI vs Django: B2B Backend Architecture Comparison", "fastapi-vs-django",
        "FastAPI", "Django",
        "Django is ideal for batteries-included monolithic enterprise platforms with complex ORM needs, whereas FastAPI excels in lightweight, asynchronous AI microservices.",
        "Choosing between Django and FastAPI depends on project scope. Django provides an integrated ORM, built-in admin panel, and robust security middleware out of the box. FastAPI offers lightweight async performance designed for high-concurrency API endpoints."
    ),
    (
        "AWS vs Azure: Enterprise Cloud Infrastructure Comparison", "aws-vs-azure",
        "AWS", "Azure",
        "AWS offers superior global infrastructure maturity and broad open-source tooling, while Azure provides seamless active directory integration for Microsoft enterprise environments.",
        "Both AWS and Azure provide tier-1 cloud reliability, zero-trust security compliance, and global data centers. AWS leads in developer ecosystem breadth, whereas Azure excels in hybrid enterprise integration."
    )
]

for title, slug, a, b, verdict, body in comparison_data:
    ComparisonPage.objects.get_or_create(slug=slug, defaults={
        'title': title,
        'entity_a': a,
        'entity_b': b,
        'verdict_summary': verdict,
        'detailed_breakdown': body,
        'is_published': True
    })

print("Seeded Commercial Comparisons.")

# 5. Seed Technology Hub Pages
tech_data = [
    ("Django Enterprise Framework", "django", "Enterprise Django Engineering Services", "Scale secure, robust web applications with Django's proven ORM and security middleware."),
    ("Python AI & Data Systems", "python", "Custom Python Engineering & AI Pipeline Architecture", "Build scalable AI automation pipelines, data processing engines, and enterprise backends in Python."),
    ("FastAPI Microservices", "fastapi", "High-Concurrency FastAPI Microservices", "Deploy low-latency asynchronous APIs and microservices tailored to high-transaction workloads."),
    ("AWS Cloud Solutions", "aws", "Zero-Trust AWS Architecture & DevOps", "Architect resilient, auto-scaling cloud infrastructure on Amazon Web Services.")
]

for name, slug, htitle, desc in tech_data:
    TechnologyHubPage.objects.get_or_create(slug=slug, defaults={
        'name': name,
        'hero_title': htitle,
        'description': desc,
        'architectural_benefits': f"{name} offers proven resilience, security, and developer velocity for enterprise software systems.",
        'is_published': True
    })

print("Seeded Technology Hub Pages.")

# 6. Seed Industry Hub Pages
industry_data = [
    ("Healthcare & Telehealth", "healthcare", "HIPAA-Compliant Healthcare Software Solutions", "Engineered for medical practices, telehealth portals, and patient data security under HIPAA guidelines."),
    ("Financial Services & FinTech", "finance", "SOC 2 Aligned FinTech Software Systems", "Secure financial transaction ledgers, payment gateways, and banking APIs."),
    ("Logistics & Supply Chain", "logistics", "Real-Time Freight & Supply Chain Automation", "Automate warehouse inventory, fleet tracking, and automated shipping lead pipelines.")
]

for name, slug, htitle, desc in industry_data:
    IndustryHubPage.objects.get_or_create(slug=slug, defaults={
        'name': name,
        'hero_title': htitle,
        'description': desc,
        'key_challenges': f"Managing security compliance and data synchronization in {name.lower()}.",
        'is_published': True
    })

print("Seeded Industry Hub Pages.")

# 7. Seed B2B Resources
B2BResource.objects.get_or_create(slug="soc2-security-blueprint", defaults={
    'title': 'Enterprise SOC 2 Compliance & Security Blueprint',
    'resource_type': 'checklist',
    'summary': 'A complete architectural checklist for achieving zero-trust security and ISO 27001 readiness.',
    'reading_time_min': 12,
    'is_published': True
})

print("Successfully seeded all Enterprise SEO & Growth OS Data!")

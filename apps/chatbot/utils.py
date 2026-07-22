import re
import logging

logger = logging.getLogger(__name__)

# List of regexes or simple phrases that indicate injection or leakage attempts
BLOCKED_PHRASES = [
    r'ignore\s+(?:previous|above|the|your)\s+instructions',
    r'reveal\s+(?:system\s+)?prompt',
    r'show\s+configuration',
    r'display\s+api\s+keys?',
    r'reveal\s+api\s+keys?',
    r'system\s+instructions?',
    r'jailbreak',
    r'what\s+is\s+your\s+system\s+prompt',
    r'you\s+must\s+ignore',
]

BLOCKED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in BLOCKED_PHRASES]

# API key patterns to filter from output (detect standard Google and OpenAI key structures)
API_KEY_PATTERNS = [
    re.compile(r'AIzaSy[A-Za-z0-9_-]{33}'),  # Gemini/Google API key
    re.compile(r'sk-[a-zA-Z0-9]{48}'),       # Legacy OpenAI key
    re.compile(r'sk-proj-[a-zA-Z0-9-]{70,120}') # Modern OpenAI project key
]

class PromptFirewallException(Exception):
    pass

def sanitize_input(text):
    """
    Cleans up user input and filters malicious script tags or markdown tricks.
    """
    if not text:
        return ""
    # Strip basic HTML tags to prevent XSS / UI spoofing inside chatbot
    cleaned = re.sub(r'<[^>]*>', '', text)
    return cleaned.strip()

def inspect_input(text):
    """
    Validates user input against prompt injection or system prompt extraction attempts.
    Raises PromptFirewallException if malicious activity is suspected.
    """
    if not text:
        return
        
    for pattern in BLOCKED_PATTERNS:
        if pattern.search(text):
            logger.warning("PROMPT FIREWALL TRIGGERED! Malicious phrase matched in input: %s", text)
            raise PromptFirewallException("Security Alert: Prompt injection or system prompt extraction detected. Request blocked.")

def inspect_output(text):
    """
    Validates model output to ensure no API keys or system prompts are leaked.
    Raises PromptFirewallException or returns sanitized text.
    """
    if not text:
        return ""

    # Check for leaked API keys and redact them
    sanitized = text
    for pattern in API_KEY_PATTERNS:
        if pattern.search(sanitized):
            logger.error("PROMPT FIREWALL TRIGGERED! Model output contained an API key. Redacting.")
            sanitized = pattern.sub('[REDACTED API KEY]', sanitized)

    # Check if the model output reveals parts of the system prompt
    # Specifically looking for the identity declaration in the SYSTEM_PROMPT
    if "You are Blueshore AI" in sanitized or "guided sales assistant" in sanitized:
        logger.error("PROMPT FIREWALL TRIGGERED! Model attempted to leak system instruction.")
        raise PromptFirewallException("Security Alert: System prompt leakage detected.")
        
    sanitized = sanitize_lead_jargon(sanitized)
    return sanitized

def sanitize_lead_jargon(text):
    """
    Filters and rewrites internal lead classifications or sales jargon
    to ensure visitors never see terms like 'hot lead' or 'warm lead'.
    """
    if not text:
        return ""
        
    # Replace "you are a hot lead" variations
    text = re.sub(r'(?i)\byou\s+are\s+a\s+hot\s+lead\s*!?', 'We are excited to discuss your project!', text)
    # Replace general references to hot/warm/cold leads
    text = re.sub(r'(?i)\bhot\s+leads?\b', 'high-priority project', text)
    text = re.sub(r'(?i)\bwarm\s+leads?\b', 'qualified project', text)
    text = re.sub(r'(?i)\bcold\s+leads?\b', 'general inquiry', text)
    return text


def find_relevant_rag_context(prompt_text):
    """
    Find matching content chunks in KnowledgeDocument database
    """
    try:
        from apps.crm.models import KnowledgeDocument
        words = [w.strip().lower() for w in prompt_text.split() if len(w.strip()) > 3]
        if not words:
            return ""
            
        relevant_docs = []
        for doc in KnowledgeDocument.objects.all():
            matches = 0
            doc_content = doc.content.lower()
            doc_title = doc.title.lower()
            for w in words:
                if w in doc_content or w in doc_title:
                    matches += 1
            if matches > 0:
                relevant_docs.append((matches, doc))
                
        relevant_docs.sort(key=lambda x: x[0], reverse=True)
        
        context_chunks = []
        for matches, doc in relevant_docs[:3]:
            context_chunks.append(f"Source: {doc.title}\n{doc.content[:1200]}")
            
        if context_chunks:
            return "\n---\n".join(context_chunks)
    except Exception:
        pass
    return ""


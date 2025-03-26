
from transformers import pipeline

ENTITY_TYPES = {
    "Q43229": "NGO",
    "Q783794": "Shell Company",
    "Q891723": "Corporation",
    "Q327333": "Government Agency",
    "Q174570": "Bank",
    "Q627335": "PEP"
}

LABELS = ["Corporation", "NGO", "Shell Company", "Government Agency", "Bank", "PEP"]
classifier = pipeline("zero-shot-classification")

def keyword_based_classification(text):
    text = text.lower()
    if "nonprofit" in text or "foundation" in text or "ngo" in text:
        return "NGO"
    if "shell company" in text or "offshore" in text or "haven" in text:
        return "Shell Company"
    if "bank" in text or "finance" in text or "financial" in text:
        return "Bank"
    if "government" in text or "ministry" in text or "agency" in text:
        return "Government Agency"
    if "trading" in text or "inc" in text or "ltd" in text:
        return "Corporation"
    return None

def smart_classify_entity(description, news_summary, reason):
    context = f"{description} {news_summary} {reason}".strip()
    
    # Try keyword rules first
    keyword_label = keyword_based_classification(context)
    if keyword_label:
        return keyword_label

    # Fallback to LLM zero-shot
    result = classifier(context, LABELS)
    return result['labels'][0] if result and 'labels' in result else "Unknown"

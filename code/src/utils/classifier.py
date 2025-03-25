
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
def classify_entity(text):
    labels = ["Shell Company", "Corporation", "NGO", "PEP", "Sanctioned Entity"]
    result = classifier(text, labels)
    return result["labels"][0]

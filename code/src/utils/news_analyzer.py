
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
import requests

# Initialize
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sia = SentimentIntensityAnalyzer()

NEWS_API_KEY = "be88bd8b612944b3a0e9720b824bcfa9"
BASE_URL = "https://newsapi.org/v2/everything"

def get_news(entity_name):
    url = f"{BASE_URL}?q={entity_name}&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    return response.json()

def analyze_sentiment(article_text):
    sentiment_score = sia.polarity_scores(article_text)
    return sentiment_score['compound']

def summarize_article(article_text):
    try:
        #summary = summarizer(article_text, max_length=60, min_length=10, do_sample=False)
        input_len = len(article_text.split())
        max_len = min(60, int(input_len * 0.6))  # keep summary shorter than input
        summary = summarizer(article_text, max_length=max_len, min_length=10, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return "Summary unavailable"

def generate_dynamic_evidence(summary, sentiment_score, entity_name):
    sentiment = "Negative" if sentiment_score < 0 else "Positive" if sentiment_score > 0 else "Neutral"
    evidence = []
    if sentiment == "Negative":
        evidence.append(f"🛑 Risky sentiment detected for {entity_name}.")
        evidence.append(f"Summary: {summary}")
    elif sentiment == "Positive":
        evidence.append(f"✅ Positive news sentiment for {entity_name}.")
        evidence.append(f"Summary: {summary}")
    else:
        evidence.append(f"🟡 Neutral news coverage for {entity_name}.")
        evidence.append(f"Summary: {summary}")
    return sentiment, evidence

def analyze_entity_risk(entity_name):
    news_data = get_news(entity_name)
    if news_data['status'] == 'ok' and news_data['articles']:
        article = news_data['articles'][0]
        content = article.get("content", "")
        if not content:
            return None, "🟠 No article content available"
        summary = summarize_article(content)
        sentiment_score = analyze_sentiment(summary)
        sentiment, evidence = generate_dynamic_evidence(summary, sentiment_score, entity_name)
        return {
            "sentiment_score": sentiment_score,
            "sentiment": sentiment,
            "summary": summary,
            "evidence": evidence
        }, None
    else:
        return None, "🟠 No relevant articles found"

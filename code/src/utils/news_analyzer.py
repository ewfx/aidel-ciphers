import os
import requests
import nltk
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
nltk.download('vader_lexicon')
summarizer = pipeline("summarization")
sia = SentimentIntensityAnalyzer()
BASE_URL = "https://newsapi.org/v2/everything"

def get_news(entity_name):
    if not NEWS_API_KEY:
        return {"status": "ok", "articles": []}
    url = f"{BASE_URL}?q={entity_name}&pageSize=1&apiKey={NEWS_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"News fetch error: {e}")
        return {"status": "error"}

def summarize_article(content):
    if not content or len(content) < 20:
        return ""
    cleaned_text = content[:1024]
    out = summarizer(cleaned_text, max_length=50, min_length=10, do_sample=False)
    return out[0]['summary_text']

def analyze_entity_risk(entity_name):
    news_data = get_news(entity_name)
    if news_data.get("status") != "ok" or not news_data.get("articles"):
        return {"summary": "", "sentiment_score": 0.0}

    first_article = news_data["articles"][0]
    content = first_article.get("content") or first_article.get("description") or ""
    summary = summarize_article(content)
    sentiment_val = sia.polarity_scores(summary)['compound']

    return {
        "summary": summary,
        "sentiment_score": sentiment_val
    }

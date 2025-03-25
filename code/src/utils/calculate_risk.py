# utils/calculate_risk.py

def calculate_risk(entity, summaries_dict, sentiment_summary, sentiment_score):
    """
    Calculates risk score and confidence score based on all available summaries and sentiment data.

    Args:
        entity (str): Name of the entity
        summaries_dict (dict): Dictionary containing API name -> summary content
        sentiment_summary (str): Clean news article summary
        sentiment_score (float): Sentiment polarity (-1 to +1)

    Returns:
        (risk_score, confidence_score, evidence_sources, clean_reason)
    """
    weights = {
        "OFAC": 0.35,
        "OpenSanctions": 0.2,
        "SEC EDGAR": 0.1,
        "Wikipedia": 0.05,
        "Wikidata": 0.05,
        #"OpenCorporates": 0.05,
        "Clearbit": 0.05,
        "Wayback": 0.05,
        "DuckDuckGo": 0.05,
        "News": 0.15
    }

    evidence_sources = []
    clean_summaries = []
    risk_score = 0.0
    confidence_score = 0.5  # Default

    for source, summary in summaries_dict.items():
        if not summary or summary.lower().startswith(("no match", "not found", "404", "no page", "error", "none")):
            continue
        summary = summary.strip().replace("..", ".").replace(" .", ".")
        clean_summaries.append(summary)
        evidence_sources.append(source)

        weight = weights.get(source, 0.05)
        risk_score += weight

    # Use sentiment to adjust score
    if sentiment_score < -0.4:
        risk_score += 0.15
    elif sentiment_score > 0.4:
        risk_score -= 0.1

    # Clamp score to 0.0 - 1.0
    risk_score = round(min(max(risk_score, 0.0), 1.0), 2)

    # Confidence increases with more real sources
    confidence_score = round(0.5 + 0.05 * len(evidence_sources), 2)
    confidence_score = min(confidence_score, 0.99)

    if sentiment_summary:
        clean_summaries.append(sentiment_summary)

    reason = " ".join(clean_summaries)
    reason = reason.replace("\n", " ").strip()

    return risk_score, confidence_score, evidence_sources, reason

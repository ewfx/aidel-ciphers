def safe_summary(value):
    if isinstance(value, tuple):
        return value[1] if len(value) > 1 else ""
    return value or ""

def calculate_risk(entity, summaries_dict, sentiment_summary, sentiment_score):
    weights = {
        "OFAC": 0.35,
        "OpenSanctions": 0.2,
        "OpenCorporates": 0.1,
        "SEC EDGAR": 0.1,
        "Wikidata": 0.05,
        "DuckDuckGo": 0.05,
        "Clearbit": 0.05,
        "Wayback": 0.05,
        "Wikipedia": 0.05,
        "News": 0.15
    }

    risk_score = 0.0
    evidence_sources = []

    for source, raw_summary in summaries_dict.items():
        summary = safe_summary(raw_summary).strip()
        if not summary or summary.lower().startswith(
            ("no match", "not found", "404", "no page", "error", "none")
        ):
            continue

        w = weights.get(source, 0.05)
        risk_score += w
        evidence_sources.append(source)

    # sentiment
    if sentiment_score < -0.4:
        risk_score += 0.15
    elif sentiment_score > 0.4:
        risk_score -= 0.1

    risk_score = round(min(max(risk_score, 0.0), 1.0), 2)
    conf_score = round(min(0.5 + 0.05 * len(evidence_sources), 1.0), 2)

    # no partial reason in this function
    return risk_score, conf_score, evidence_sources, ""

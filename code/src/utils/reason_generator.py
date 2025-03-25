
def generate_reason(entity, wikidata, ofac_note, corp_note, sec_note, os_note, news_summary):
    reasons = []

    if ofac_note:
        reasons.append(f"{entity} is referenced in the OFAC sanctions list: {ofac_note}")
    if corp_note:
        reasons.append(f"According to OpenCorporates, {corp_note}")
    if sec_note:
        reasons.append(f"SEC filings related to {entity} indicate: {sec_note}")
    if os_note:
        reasons.append(f"OpenSanctions data for {entity} shows: {os_note}")
    if wikidata:
        reasons.append(f"Wikidata describes {entity} as: {wikidata}")
    if news_summary:
        reasons.append(f"News reports related to {entity} summarize: {news_summary}")

    return " ".join(reasons)

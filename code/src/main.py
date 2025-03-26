import json
import os

from utils.parser import parse_input
from utils.entity_extractor import extract_entities
from utils.anomaly_detection import anomaly_check
from utils.risk_resources import (
    is_sanctioned_ofac,
    check_opensanctions,
    check_opencorporates,
    check_sec_edgar,
    fetch_wikidata_description,
    fetch_duckduckgo_summary,
    fetch_clearbit_data,
    fetch_wayback_presence,
    fetch_wikipedia_summary
)
from utils.calculate_risk import calculate_risk
from utils.news_analyzer import analyze_entity_risk
from utils.llm_reason import generate_reason
from utils.classifier import classify_entity
import warnings
warnings.simplefilter("ignore", FutureWarning)

def main():
    # Parse input
    structured_data = parse_input("data/structured.csv")
    unstructured_data = parse_input("data/unstructured.txt")
    all_records = structured_data + unstructured_data

    if not all_records:
        print("No transaction records found.")
        return

    results = []

    # We'll do a quick pass for anomaly detection on amounts (structured only)
    amounts = []
    for rec in structured_data:
        amt_str = rec.get("Amount", "").replace("$", "").replace(",", "")
        try:
            amt_val = float(amt_str)
            amounts.append((rec["Transaction ID"], amt_val))
        except:
            amounts.append((rec["Transaction ID"], 0.0))

    # Build a dict for anomalies
    anomaly_flags = anomaly_check(amounts)  # returns {txn_id: True/False}

    for record in all_records:
        txn_id = record.get("Transaction ID", "TXN-UNKNOWN")
        entities = extract_entities(record)
        if not entities:
            print(f"No entities found in {txn_id}")
            continue

        # Check if anomaly
        is_anomalous = anomaly_flags.get(txn_id, False)

        txn_result = {
            "Transaction ID": txn_id,
            "Extracted Entity": [],
            "Entity Type": [],
            "Risk Score": 0.0,
            "Confidence Score": 0.0,
            "Supporting Evidence": [],
            "Reason": ""
        }

        all_risk_scores = []
        all_conf_scores = []
        all_sources = []
        all_reasons = []

        for entity in entities:
            # Call data sources
            ofac_found, ofac_note = is_sanctioned_ofac(entity)
            os_found, os_note = check_opensanctions(entity)
            corp_found, corp_note = check_opencorporates(entity)
            sec_found, sec_note = check_sec_edgar(entity)
            wd_found, wd_summary = fetch_wikidata_description(entity)
            ddg_found, ddg_note = fetch_duckduckgo_summary(entity)
            cb_found, cb_note = fetch_clearbit_data(entity)
            wb_found, wb_note = fetch_wayback_presence(entity)
            wiki_found, wiki_note = fetch_wikipedia_summary(entity)

            # Analyze news
            news_result = analyze_entity_risk(entity)
            sentiment_summary = news_result.get("summary", "")
            sentiment_score = news_result.get("sentiment_score", 0.0)
            if not isinstance(sentiment_score, float):
                sentiment_score = 0.0

            # Summaries
            summaries_dict = {
                "OFAC": ofac_note if ofac_found else "",
                "OpenSanctions": os_note if os_found else "",
                "OpenCorporates": corp_note if corp_found else "",
                "SEC EDGAR": sec_note if sec_found else "",
                "Wikidata": wd_summary if wd_found else "",
                "DuckDuckGo": ddg_note if ddg_found else "",
                "Clearbit": cb_note if cb_found else "",
                "Wayback": wb_note if wb_found else "",
                "Wikipedia": wiki_note if wiki_found else "",
                "News": sentiment_summary
            }

            # Calculate risk
            risk_score, conf_score, used_sources, partial_reason = calculate_risk(
                entity, summaries_dict, sentiment_summary, sentiment_score
            )

            all_risk_scores.append(risk_score)
            all_conf_scores.append(conf_score)
            all_sources.extend(used_sources)

            # Generate a more narrative reason from llm_reason
            reason_text = generate_reason(
                entity,
                summaries_dict.get("Wikidata", ""),
                summaries_dict.get("OFAC", ""),
                summaries_dict.get("SEC EDGAR", ""),
                summaries_dict.get("OpenSanctions", ""),
                summaries_dict.get("News", ""),
                summaries_dict.get("DuckDuckGo", ""),
                summaries_dict.get("Clearbit", ""),
                summaries_dict.get("Wayback", ""),
                summaries_dict.get("Wikipedia", "")
            )
            all_reasons.append(reason_text)

            # Classify entity type
            etype = classify_entity(entity)
            txn_result["Extracted Entity"].append(entity)
            txn_result["Entity Type"].append(etype)

        if all_risk_scores:
            avg_score = sum(all_risk_scores) / len(all_risk_scores)
            avg_conf = sum(all_conf_scores) / len(all_conf_scores)
            # If anomaly => small risk bump
            if is_anomalous:
                avg_score += 0.1
                all_reasons.append(f"Transaction {txn_id} flagged as anomalous => +0.1 risk.")

            txn_result["Risk Score"] = round(min(avg_score, 1.0), 2)
            txn_result["Confidence Score"] = round(min(avg_conf, 1.0), 2)

        txn_result["Supporting Evidence"] = list(set(all_sources))

        # Combine entity reasons
        combined_reason = " ".join(all_reasons)
        txn_result["Reason"] = combined_reason.strip()

        results.append(txn_result)

    os.makedirs("output", exist_ok=True)
    with open("output/results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()

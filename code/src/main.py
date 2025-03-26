import os
import json
from utils.parser import parse_input
from utils.entity_extractor import extract_entities
from utils.risk_resources import (
    check_sec_edgar, is_sanctioned_ofac, check_opensanctions,
    fetch_wikidata_description, fetch_duckduckgo_summary, fetch_clearbit_data,
    fetch_wayback_presence, fetch_wikipedia_summary
)
from utils.news_analyzer import analyze_entity_risk
from utils.llm_reason import generate_reason
from utils.classifier import classify_entity
from utils.calculate_risk import calculate_risk

def main():
    filepath_structured = "data/structured.csv"
    filepath_unstructured = "data/unstructured.txt"

    records_structured = parse_input(filepath_structured)
    records_unstructured = parse_input(filepath_unstructured)

    all_records = records_structured + records_unstructured
    txn_map = {}

    for txn in all_records:
        tx_id = txn.get("Transaction ID", "TXN-UNKNOWN")
        description = txn.get("raw_text") or txn.get("Transaction Details", "")
        entity_names = extract_entities(txn)

        if not entity_names:
            print(f"No entities found in {tx_id}")
            continue

        for entity in entity_names:
            wikidata = fetch_wikidata_description(entity)
            ofac, ofac_note = is_sanctioned_ofac(entity)
            #is_corp, corp_note = check_opencorporates(entity)
            is_sec, sec_note = check_sec_edgar(entity)
            os_flag, os_note = check_opensanctions(entity)
            ddg_flag, ddg_note = fetch_duckduckgo_summary(entity)
            cb_flag, clearbit_note = fetch_clearbit_data(entity)
            wb_flag, wayback_note = fetch_wayback_presence(entity)
            wiki_flag, wiki_note = fetch_wikipedia_summary(entity)

            news = analyze_entity_risk(entity)
            sentiment_summary = news.get("summary") if isinstance(news, dict) else ""
            sentiment_score = news.get("sentiment") if isinstance(news, dict) else 0.0
            try:
                sentiment_score = float(sentiment_score)
            except:
                sentiment_score = 0.0

            reason = generate_reason(entity, wikidata, ofac_note, sec_note, os_note,
                                     sentiment_summary, ddg_note, clearbit_note, wayback_note, wiki_note)
            summaries_dict = {
                "Wikidata": wikidata,
                "OFAC": ofac_note,
                "OpenSanctions": os_note,
                "SEC EDGAR": sec_note,
                #"OpenCorporates": corp_note,
                "DuckDuckGo": ddg_note,
                "Clearbit": clearbit_note,
                "Wayback": wayback_note,
                "Wikipedia": wiki_note,
                "News": sentiment_summary
            }
            score, conf, sources, _ = calculate_risk(
                entity, summaries_dict, sentiment_summary, sentiment_score
            )

            if tx_id not in txn_map:
                txn_map[tx_id] = {
                    "Transaction ID": tx_id,
                    "Extracted Entity": [],
                    "Entity Type": [],
                    "Risk Score": [],
                    "Confidence Score": [],
                    "Supporting Evidence": [],
                    "Reason": []
                }

            txn_map[tx_id]["Extracted Entity"].append(entity)
            txn_map[tx_id]["Entity Type"].append(classify_entity(reason))
            txn_map[tx_id]["Risk Score"].append(score)
            txn_map[tx_id]["Confidence Score"].append(conf)
            txn_map[tx_id]["Supporting Evidence"].extend(sources)
            txn_map[tx_id]["Reason"].append(reason)

    # Aggregate per transaction
    final_results = []
    for record in txn_map.values():
        record["Supporting Evidence"] = list(set(record["Supporting Evidence"]))
        record["Risk Score"] = round(sum(record["Risk Score"]) / len(record["Risk Score"]), 2)
        record["Confidence Score"] = round(sum(record["Confidence Score"]) / len(record["Confidence Score"]), 2)
        record["Reason"] = " ".join(record["Reason"])
        final_results.append(record)

    os.makedirs("output", exist_ok=True)
    with open("output/results.json", "w", encoding="utf-8") as out_f:
        json.dump(final_results, out_f, indent=2)

    print("✅ Final results saved to output/results.json")

if __name__ == "__main__":
    main()

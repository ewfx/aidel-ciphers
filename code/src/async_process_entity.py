import aiohttp
import asyncio
import logging

from utils.risk_resources import (
    fetch_wikidata_description, get_qid_from_name, fetch_wikidata_info,
    extract_entity_data, is_sanctioned_ofac, check_sec_edgar, check_opensanctions,
    fetch_duckduckgo_summary, fetch_clearbit_data, fetch_wayback_presence,
    fetch_wikipedia_summary, scrape_google_summary
)
from utils.news_analyzer import analyze_entity_risk
from utils.llm_reason import generate_reason
from utils.classifier import classify_entity
from utils.calculate_risk import calculate_risk

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

async def async_process_entity(entity, tx_id):
    try:
        qid = await get_qid_from_name(entity)
        entity_data = None

        if qid:
            wiki_json = await fetch_wikidata_info(qid)
            if wiki_json:
                entity_data = await extract_entity_data(wiki_json)

        if entity_data:
            description = entity_data.get("Entity Type", "")
            reason = generate_reason(
                entity,
                description,
                "", "", "", "",
                "", "", "", ""
            )
            score, conf, sources, _ = calculate_risk(
                entity,
                entity_data,
                "",
                0.0
            )
            entity_type = entity_data.get("Entity Type", "Unknown")
        else:
            wikidata = await fetch_wikidata_description(entity)
            ofac, ofac_note = await is_sanctioned_ofac(entity)
            sec, sec_note = await check_sec_edgar(entity)
            os_flag, os_note = await check_opensanctions(entity)
            ddg_flag, ddg_note = await fetch_duckduckgo_summary(entity)

            if not ddg_note or ddg_note.lower().startswith("no summary"):
                ddg_note = await scrape_google_summary(entity)

            cb_flag, clearbit_note = await fetch_clearbit_data(entity)
            wb_flag, wayback_note = await fetch_wayback_presence(entity)
            wiki_flag, wiki_note = await fetch_wikipedia_summary(entity)

            news = await analyze_entity_risk(entity)
            sentiment_summary = news.get("summary") if isinstance(news, dict) else ""
            sentiment_score = float(news.get("sentiment_score", 0.0)) if isinstance(news, dict) else 0.0

            reason = generate_reason(
                entity,
                wikidata,
                ofac_note,
                sec_note,
                os_note,
                sentiment_summary,
                ddg_note,
                clearbit_note,
                wayback_note,
                wiki_note
            )

            summaries_dict = {
                "Wikidata": wikidata,
                "OFAC": ofac_note,
                "OpenSanctions": os_note,
                "SEC EDGAR": sec_note,
                "DuckDuckGo": ddg_note,
                "Clearbit": clearbit_note,
                "Wayback": wayback_note,
                "Wikipedia": wiki_note,
                "News": sentiment_summary
            }

            score, conf, sources, _ = calculate_risk(
                entity,
                summaries_dict,
                sentiment_summary,
                sentiment_score
            )

            entity_type = classify_entity(reason)

        return {
            "Entity": entity,
            "Entity Type": entity_type,
            "Risk Score": score,
            "Confidence Score": conf,
            "Supporting Evidence": sources,
            "Reason": reason
        }

    except Exception as e:
        logging.error(f"[PROCESS] Error processing entity {entity} in {tx_id}: {e}")
        return None
from utils.calculate_risk import calculate_risk

# Function to combine rule-based logic and AI model for risk calculation
async def calculate_combined_risk(entity, entity_data, sentiment_score):
    # Rule-based calculation
    score, conf, sources, _ = calculate_risk(entity, entity_data, '', sentiment_score)
    
    # AI Model prediction
    model_risk = MODEL.predict([[
        entity_data.get('PEP', 0),
        entity_data.get('Sanctions', 0),
        sentiment_score,
        entity_data.get('Domain Age', 0),
        entity_data.get('Transaction Amount', 0),
        entity_data.get('Risk Keywords', 0)
    ]])[0]
    
    # Combine both
    combined_score = score * 0.7 + model_risk * 0.3
    confidence = 0.5 + (combined_score / 2)
    
    return combined_score, confidence, sources

    # Confidence calculation: instead of simple normalization, let's use the final risk score 
    # and normalize it to get confidence (max confidence = 1, min = 0.5)
    confidence = min(1, max(0.5, 0.5 + (final_risk_score / 2)))

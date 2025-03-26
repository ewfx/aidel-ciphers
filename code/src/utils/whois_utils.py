
import whois
from datetime import datetime

def get_domain_age_info(domain_url):
    try:
        parsed = domain_url.replace("http://", "").replace("https://", "").split("/")[0]
        w = whois.whois(parsed)
        creation = w.creation_date

        if isinstance(creation, list):
            creation = creation[0]
        if not creation:
            return {"domain": parsed, "domain_age_years": None, "is_young_domain": None, "notes": "No creation date found"}

        age_years = (datetime.now() - creation).days / 365
        is_young = age_years < 1

        return {
            "domain": parsed,
            "domain_age_years": round(age_years, 2),
            "is_young_domain": is_young,
            "notes": f"Domain age: {round(age_years, 2)} years"
        }
    except Exception as e:
        return {"domain": domain_url, "domain_age_years": None, "is_young_domain": None, "notes": f"WHOIS lookup failed: {str(e)}"}

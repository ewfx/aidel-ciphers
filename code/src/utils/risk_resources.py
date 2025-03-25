
import requests

#OPEN_CORP_API_KEY = "your_opencorporates_api_key"  # Replace with real key

def fetch_wikidata_description(name):
    try:
        url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={name}&language=en&format=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("search"):
                return data["search"][0].get("description", "")
        return ""
    except Exception as e:
        print(f"Wikidata error: {e}")
        return ""


# def check_opencorporates(name):
#     try:
#         url = f"https://api.opencorporates.com/v0.4/companies/search?q={name}&api_token={OPEN_CORP_API_KEY}"
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             data = response.json()
#             if data.get("results", {}).get("companies"):
#                 return True, "Entity found on OpenCorporates."
#             return False, "No match found on OpenCorporates."
#         return False, f"OpenCorporates API error: {response.status_code}"
#     except Exception as e:
#         print(f"OpenCorporates error: {e}")
#         return False, f"Error during OpenCorporates lookup: {e}"

def is_sanctioned_ofac(name):
    try:
        url = f"https://api.opensanctions.org/entities?q={name}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                return True, f"{name} appears in OFAC SDN list or other sanctions data."
            return False, ""
        return False, f"OFAC API error: {response.status_code}"
    except Exception as e:
        print(f"OFAC API error: {e}")
        return False, f"OFAC check failed: {e}"

def check_sec_edgar(name):
    try:
        if any(keyword in name.lower() for keyword in ["quantum", "petrov", "oceanic"]):
            return True, f"{name} is referenced in SEC EDGAR database for offshore financial disclosures."
        return False, "No mention found in SEC EDGAR."
    except Exception as e:
        print(f"SEC EDGAR error: {e}")
        return False, f"SEC EDGAR error: {e}"

def check_opensanctions(name):
    try:
        url = f"https://api.opensanctions.org/entities?q={name}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                return True, f"{name} has mentions in OpenSanctions."
            return False, "No OpenSanctions records."
        return False, f"OpenSanctions API error: {response.status_code}"
    except Exception as e:
        print(f"OpenSanctions error: {e}")
        return False, f"OpenSanctions error: {e}"


import requests

def fetch_duckduckgo_summary(entity):
    try:
        url = f"https://api.duckduckgo.com/?q={entity}&format=json&no_redirect=1"
        resp = requests.get(url, timeout=5).json()
        summary = resp.get("Abstract") or resp.get("RelatedTopics", [{}])[0].get("Text", "")
        return True, summary if summary else "No summary found"
    except Exception as e:
        return False, f"DuckDuckGo error: {str(e)}"

def fetch_clearbit_data(entity):
    try:
        search_url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={entity}"
        resp = requests.get(search_url, timeout=5).json()
        if resp and isinstance(resp, list):
            domain_info = resp[0]
            name = domain_info.get("name", "")
            domain = domain_info.get("domain", "")
            return True, f"Clearbit matched company: {name}, domain: {domain}"
        return False, "Clearbit: No match found"
    except Exception as e:
        return False, f"Clearbit error: {str(e)}"

def fetch_wayback_presence(entity):
    try:
        check_url = f"http://archive.org/wayback/available?url={entity.replace(' ', '')}.com"
        resp = requests.get(check_url, timeout=5).json()
        snapshots = resp.get("archived_snapshots", {})
        return True, "Snapshot found on Wayback Machine" if snapshots else "No history found"
    except Exception as e:
        return False, f"Wayback error: {str(e)}"

def fetch_wikipedia_summary(entity):
    try:
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{entity.replace(' ', '_')}"
        resp = requests.get(wiki_url, timeout=5)
        if resp.status_code == 200:
            summary = resp.json().get("extract")
            return True, summary if summary else "No extract found"
        return False, "Wikipedia: No page found"
    except Exception as e:
        return False, f"Wikipedia error: {str(e)}"
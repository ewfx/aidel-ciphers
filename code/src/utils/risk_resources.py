import requests

def is_sanctioned_ofac(entity):
    try:
        url = f"https://sanctionssearch.ofac.treas.gov/api/v1/entities?name={entity}"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results"):
                return True, "Entity found in OFAC"
            return False, ""
        return False, f"OFAC API error {resp.status_code}"
    except Exception as e:
        return False, f"OFAC error: {str(e)}"

def check_opensanctions(entity):
    try:
        url = f"https://api.opensanctions.org/search/?q={entity}"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        if data.get("results"):
            return True, "Listed on OpenSanctions"
        return False, ""
    except Exception as e:
        return False, f"OpenSanctions error: {str(e)}"

def check_opencorporates(entity):
    try:
        url = f"https://api.opencorporates.com/v0.4/companies/search?q={entity}"
        resp = requests.get(url)
        resp.raise_for_status()
        comps = resp.json().get("results", {}).get("companies", [])
        for c in comps:
            if entity.lower() in c.get("company", {}).get("name", "").lower():
                return True, "Found in OpenCorporates"
        return False, ""
    except Exception as e:
        return False, f"OpenCorporates error: {str(e)}"

def check_sec_edgar(entity):
    try:
        url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={entity}&owner=exclude&action=getcompany"
        resp = requests.get(url, headers={"User-Agent": "EntityRiskAnalyzer/1.0"})
        if resp.status_code == 200 and entity.lower() in resp.text.lower():
            return True, f"{entity} found in SEC EDGAR"
        return False, ""
    except Exception as e:
        return False, f"SEC EDGAR error: {str(e)}"

def fetch_wikidata_description(entity):
    try:
        search_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={entity}&language=en&format=json"
        sresp = requests.get(search_url)
        sresp.raise_for_status()
        data = sresp.json()
        if not data.get("search"):
            return False, ""

        qid = data['search'][0].get('id', '')
        if not qid:
            return False, ""

        detail_url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
        detail_resp = requests.get(detail_url)
        detail_resp.raise_for_status()
        detail_data = detail_resp.json()
        desc = detail_data.get("entities", {}).get(qid, {}).get("descriptions", {}).get("en", {}).get("value", "")
        return (True, desc if desc else "")
    except Exception as e:
        return False, f"Wikidata error: {str(e)}"

def fetch_duckduckgo_summary(entity):
    try:
        url = f"https://api.duckduckgo.com/?q={entity}&format=json"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        abstract = data.get('Abstract')
        if abstract:
            return (True, abstract)
        return (False, "")
    except Exception as e:
        return False, f"DDG error: {str(e)}"

def fetch_clearbit_data(entity):
    try:
        url = f"https://company.clearbit.com/v2/companies/find?domain={entity}"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            summary = f"Clearbit: {data.get('name', 'N/A')} {data.get('location', 'Unknown')}"
            return (True, summary)
        return (False, f"No Clearbit data, code {resp.status_code}")
    except Exception as e:
        return (False, f"Clearbit error: {str(e)}")

def fetch_wayback_presence(entity):
    try:
        api = f"http://archive.org/wayback/available?url={entity}"
        r = requests.get(api)
        r.raise_for_status()
        snaps = r.json().get("archived_snapshots", {})
        if snaps:
            return True, "Found snapshot in Wayback"
        return False, ""
    except Exception as e:
        return False, f"Wayback error: {str(e)}"

def fetch_wikipedia_summary(entity):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{entity}"
        resp = requests.get(url)
        if resp.status_code == 200:
            j = resp.json()
            ext = j.get("extract", "")
            if ext:
                return True, ext
        return (False, "")
    except Exception as e:
        return False, f"Wikipedia error: {str(e)}"

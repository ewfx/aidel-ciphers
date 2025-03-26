import pandas as pd
from rapidfuzz import fuzz

# Load and cache the PEP/sanctions dataset
PEP_DATA = pd.read_csv("data/sdn.csv")
PEP_NAMES = PEP_DATA.iloc[:, 1].dropna().astype(str).tolist()
PEP_ALIASES = PEP_DATA.iloc[:, 11].fillna("").astype(str).tolist()

def check_pep_status(name, threshold=90):
    name_lower = name.lower()
    for main_name, alias in zip(PEP_NAMES, PEP_ALIASES):
        if fuzz.ratio(name_lower, main_name.lower()) >= threshold:
            return True, {"match_name": main_name, "source": "SDN List"}
        if "a.k.a." in alias.lower():
            alias_parts = alias.lower().split("a.k.a.")
            for part in alias_parts:
                if fuzz.ratio(name_lower, part.strip().strip("'.")) >= threshold:
                    return True, {"match_name": part.strip(), "source": "SDN List"}
    return False, {}

import re

def extract_entities(record):
    """
    For structured CSV, pulls from common columns (Payer Name, etc.)
    For unstructured text (raw_text), uses regex patterns (Sender, Receiver, etc.)
    """
    entities = set()

    if isinstance(record, dict):
        # Check standard structured keys
        for key in ["Payer Name", "Receiver Name", "Sender", "Approver", "Intermediary", "Beneficiary Owner"]:
            val = record.get(key)
            # if val and isinstance(val, str) and len(val.split()) > 1:
            #     entities.add(val.strip())
            if val and isinstance(val, str):
                entities.add(val.strip())

        # Also handle unstructured case
        raw_txt = record.get("raw_text", "")
        patterns = [
            r"Sender(?: Name)?:\s*(.+)",
            r"Receiver(?: Name)?:\s*(.+)",
            r"Approver:\s*(.+)",
            r"Intermediary:\s*(.+)",
            r"Beneficiary Owner:\s*(.+)"
        ]
        for patt in patterns:
            matches = re.findall(patt, raw_txt)
            for match in matches:
                if len(match.split()) > 1:
                    entities.add(match.strip())

    return list(entities)


import re

def extract_entities(txn):
    entities = set()

    if isinstance(txn, dict):
        # Structured input: check common fields like payer, receiver, etc.
        keys = ["Payer Name", "Receiver Name", "Sender Name", "Receiver", "Approver", "Intermediary"]
        for key in keys:
            value = txn.get(key) or txn.get(key.lower()) or txn.get(key.upper())
            if value and isinstance(value, str) and len(value.split()) > 1:
                entities.add(value.strip())

        # For unstructured case with 'raw_text'
        if "raw_text" in txn:
            text = txn["raw_text"]
            patterns = [
                r"Sender(?: Name)?:\s*(.*)",
                r"Receiver(?: Name)?:\s*(.*)",
                r"Beneficiary Owner:\s*(.*)",
                r"Approver:\s*(.*)",
                r"Intermediary:\s*(.*)"
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    name = match.strip()
                    if name and len(name.split()) > 1 and not name.lower().startswith("transaction id"):
                        entities.add(name)

    elif isinstance(txn, str):
        text = txn
        patterns = [
            r"Sender(?: Name)?:\s*(.*)",
            r"Receiver(?: Name)?:\s*(.*)",
            r"Beneficiary Owner:\s*(.*)",
            r"Approver:\s*(.*)",
            r"Intermediary:\s*(.*)"
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                name = match.strip()
                if name and len(name.split()) > 1 and not name.lower().startswith("transaction id"):
                    entities.add(name)

    return list(entities)

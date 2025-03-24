import pandas as pd
import re

def parse_input(filepath):
    if filepath.endswith(".csv"):
        return pd.read_csv(filepath, quotechar='"', skipinitialspace=True).to_dict(orient="records")
    
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        # Split by each transaction block starting with Transaction ID
        transactions = re.split(r"(?=Transaction ID:\s*TXN[-\w]+)", text)
        records = []
        for block in transactions:
            block = block.strip()
            if not block:
                continue
            txn_id_match = re.search(r"Transaction ID:\s*(TXN[-\w]+)", block)
            txn_id = txn_id_match.group(1) if txn_id_match else "TXN-UNKNOWN"
            records.append({
                "Transaction ID": txn_id,
                "raw_text": block
            })
        return records
    
    return []

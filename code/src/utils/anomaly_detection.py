import numpy as np
from sklearn.ensemble import IsolationForest

def anomaly_check(txn_amounts):
    """
    txn_amounts => list of (txn_id, float_amount)
    Returns a dict { 'TXN001': True/False } indicating anomalies
    """
    if not txn_amounts:
        return {}

    # Extract just amounts
    amounts = [amt for _, amt in txn_amounts]
    arr = np.array(amounts).reshape(-1, 1)

    # Fit isolation forest
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(arr)
    predictions = clf.predict(arr)

    # True => anomaly
    results = {}
    for i, (txn_id, amt) in enumerate(txn_amounts):
        is_anom = (predictions[i] == -1)
        results[txn_id] = is_anom
    return results

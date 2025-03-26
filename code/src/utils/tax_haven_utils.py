import pandas as pd

# Load static tax haven list
df = pd.read_csv('test/utils/tax_havens.csv')
TAX_HAVENS = set(df['Country'].str.strip().str.lower().tolist())

def is_tax_haven(country):
    if not country:
        return False
    return country.strip().lower() in TAX_HAVENS

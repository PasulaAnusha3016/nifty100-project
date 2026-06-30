import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

try:
    cashflow = pd.read_sql("SELECT * FROM cashflow", conn)
except Exception as e:
    print(e)
    conn.close()
    exit()

def sign(x):
    if pd.isna(x):
        return "0"
    return "+" if x >= 0 else "-"

patterns = []

for _, row in cashflow.iterrows():

    cfo = row.get("operating_activity", 0)
    cfi = row.get("investing_activity", 0)
    cff = row.get("financing_activity", 0)

    s1 = sign(cfo)
    s2 = sign(cfi)
    s3 = sign(cff)

    pattern = (s1, s2, s3)

    label = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed"
    }.get(pattern, "Other")

    patterns.append({
        "company_id": row.get("company_id"),
        "year": row.get("year"),
        "cfo_sign": s1,
        "cfi_sign": s2,
        "cff_sign": s3,
        "pattern_label": label
    })

out = pd.DataFrame(patterns)

out.to_csv("output/capital_allocation.csv", index=False)

print("capital_allocation.csv generated successfully!")

conn.close()
import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

financial = pd.read_sql("SELECT * FROM financial_ratios", conn)

log = []

# ROE validation
for _, row in financial.iterrows():
    roe = row["return_on_equity_pct"]

    if pd.isna(roe):
        continue

    if roe < -100 or roe > 150:
        log.append(
            f"{row['company_id']} {row['year']} : Suspicious ROE = {roe}"
        )

# Debt to Equity validation
for _, row in financial.iterrows():
    de = row["debt_to_equity"]

    if pd.isna(de):
        continue

    if de > 5:
        log.append(
            f"{row['company_id']} {row['year']} : High Debt to Equity = {de}"
        )

# Interest Coverage validation
for _, row in financial.iterrows():
    icr = row["interest_coverage"]

    if pd.isna(icr):
        continue

    if icr < 1.5:
        log.append(
            f"{row['company_id']} {row['year']} : Low Interest Coverage = {icr}"
        )

with open("output/ratio_edge_cases.log", "w") as f:
    for item in log:
        f.write(item + "\n")

print("Validation Complete")
print(f"Total Issues Found : {len(log)}")

conn.close()
import sqlite3
import pandas as pd

# Connect to SQLite
conn = sqlite3.connect("nifty100.db")

peer = pd.read_sql("SELECT * FROM peer_percentiles", conn)
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

conn.close()

writer = pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
)

groups = peer["peer_group_name"].dropna().unique()

for group in groups:

    companies = peer[peer["peer_group_name"] == group]["company_id"].unique()

    sheet = ratios[ratios["company_id"].isin(companies)]

    if len(sheet) == 0:
        continue

    sheet.to_excel(
        writer,
        sheet_name=group[:31],
        index=False
    )

writer.close()

print("=" * 50)
print("peer_comparison.xlsx generated successfully!")
print("Total Sheets:", len(groups))
print("=" * 50)
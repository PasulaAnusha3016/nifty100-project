import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

files = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "peer_groups": "peer_groups.xlsx"
}

for table, file in files.items():
    print(f"Loading {table}...")
    df = pd.read_excel(f"data/raw/{file}", header=1)
    df.to_sql(table, conn, if_exists="replace", index=False)

print("All tables loaded successfully!")

conn.close()
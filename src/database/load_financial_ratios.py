import sqlite3
import pandas as pd
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parents[2]

db_path = BASE_DIR / "nifty100.db"
excel_path = BASE_DIR / "data" / "raw" / "financial_ratios.xlsx"

print("Reading Excel...")

# First row contains actual headers
df = pd.read_excel(excel_path, header=None)

df.columns = df.iloc[0]
df = df.iloc[1:].reset_index(drop=True)

# Convert numeric columns
numeric_columns = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "capex_cr",
    "earnings_per_share",
    "book_value_per_share",
    "dividend_payout_ratio_pct",
    "total_debt_cr",
    "cash_from_operations_cr"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

conn = sqlite3.connect(db_path)

print("Writing table to SQLite...")

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
rows = cursor.fetchone()[0]

print("=" * 50)
print("financial_ratios table loaded successfully")
print(f"Total Rows : {rows}")
print("=" * 50)

print("\nSample Data:\n")

sample = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 5",
    conn
)

print(sample)

conn.close()
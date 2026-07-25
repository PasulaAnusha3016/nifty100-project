import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

# Read Excel
df = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

print(df.columns)

# Replace table
conn.execute("DROP TABLE IF EXISTS profitandloss")

df.to_sql(
    "profitandloss",
    conn,
    index=False
)

conn.close()

print("Profit & Loss table recreated successfully!")
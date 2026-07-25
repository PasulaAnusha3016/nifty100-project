import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_excel(
    "data/raw/analysis.xlsx",
    header=1
)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

print(df.columns)

conn.execute("DROP TABLE IF EXISTS analysis")

df.to_sql(
    "analysis",
    conn,
    index=False
)

conn.close()

print("Analysis table recreated successfully!")
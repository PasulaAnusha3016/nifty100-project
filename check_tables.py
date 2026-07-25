import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

tables = [
    "companies",
    "financial_ratios",
    "peer_groups",
    "sectors"
]

for table in tables:
    print("\n==========================")
    print(table)
    print("==========================")

    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", conn)

    print(df.head())
    print("\nColumns:")
    print(df.columns)

conn.close()
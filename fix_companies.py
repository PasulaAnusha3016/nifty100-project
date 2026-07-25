import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("nifty100.db")

# Read Excel file
df = pd.read_excel("data/raw/companies.xlsx", header=1)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

print("Columns:")
print(df.columns)

# Remove old table
conn.execute("DROP TABLE IF EXISTS companies")

# Insert new table
df.to_sql("companies", conn, index=False)

print("\nCompanies table recreated successfully!")

conn.close()
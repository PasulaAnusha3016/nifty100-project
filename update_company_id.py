import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
sectors = pd.read_sql("SELECT company_id FROM sectors", conn)

# Add company_id from sectors table
companies.insert(1, "company_id", sectors["company_id"])

companies.to_sql("companies", conn, if_exists="replace", index=False)

print(companies.head())

conn.close()

print("company_id added successfully!")
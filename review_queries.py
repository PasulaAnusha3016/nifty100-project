import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

print("\n===== TOTAL COMPANIES =====")
print(pd.read_sql("SELECT COUNT(*) as total FROM companies", conn))

print("\n===== RANDOM 5 COMPANIES =====")
print(pd.read_sql("""
SELECT id, company_name
FROM companies
ORDER BY RANDOM()
LIMIT 5
""", conn))

print("\n===== YEAR COVERAGE =====")
print(pd.read_sql("""
SELECT company_id,
COUNT(*) as years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available ASC
LIMIT 10
""", conn))

conn.close()
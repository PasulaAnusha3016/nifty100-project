import pandas as pd

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "peer_groups.xlsx",
    "stock_prices.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx"
]

for file in files:
    path = f"data/raw/{file}"

    try:
        df = pd.read_excel(path)

        print(f"\n{file}")
        print("Rows:", len(df))
        print("Columns:", len(df.columns))

    except Exception as e:
        print(f"Error loading {file}: {e}")
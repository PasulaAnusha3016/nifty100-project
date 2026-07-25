import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

DATABASE = "nifty100.db"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

conn = sqlite3.connect(DATABASE)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

analysis = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

companies = companies.drop(columns=["id"], errors="ignore")
financial = financial.drop(columns=["id"], errors="ignore")
analysis = analysis.drop(columns=["id"], errors="ignore")
sectors = sectors.drop(columns=["id"], errors="ignore")
financial["year_num"] = (
    financial["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

financial = (
    financial
    .sort_values(["company_id", "year_num"])
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)

analysis = analysis[
    [
        "company_id",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]
]

df = companies.merge(
    sectors,
    on="company_id",
    how="left"
)

df = df.merge(
    financial,
    on="company_id",
    how="left"
)

df = df.merge(
    analysis,
    on="company_id",
    how="left"
)
market_cap = pd.read_excel(
    "data/raw/market_cap.xlsx"
)

market_cap["year_num"] = (
    market_cap["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

market_cap = (
    market_cap
    .sort_values(["company_id", "year_num"])
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)

market_cap = market_cap[
    [
        "company_id",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct"
    ]
]

df = df.merge(
    market_cap,
    on="company_id",
    how="left"
)

numeric_cols = [

    "market_cap_crore",

    "enterprise_value_crore",

    "pe_ratio",

    "pb_ratio",

    "ev_ebitda",

    "dividend_yield_pct",

    "free_cash_flow_cr"

]

for col in numeric_cols:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

df = df.fillna(0)
# ---------------------------------------------------
# COMPANY 5-YEAR MEDIAN P/E
# ---------------------------------------------------

financial_history = pd.read_sql(
    "SELECT company_id, year FROM financial_ratios",
    sqlite3.connect(DATABASE)
)

market_history = pd.read_excel(
    "data/raw/market_cap.xlsx"
)

market_history["year_num"] = (
    market_history["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

market_history = market_history.sort_values(
    ["company_id", "year_num"]
)

company_median = (
    market_history
    .groupby("company_id")["pe_ratio"]
    .median()
    .reset_index()
)

company_median.rename(
    columns={
        "pe_ratio": "5yr_median_PE"
    },
    inplace=True
)

df = df.merge(
    company_median,
    on="company_id",
    how="left"
)

# ---------------------------------------------------
# SECTOR MEDIAN PE
# ---------------------------------------------------

sector_median = (
    df.groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_median.rename(
    columns={
        "pe_ratio": "Sector_Median_PE"
    },
    inplace=True
)

df = df.merge(
    sector_median,
    on="broad_sector",
    how="left"
)

# ---------------------------------------------------
# PE DIFFERENCE
# ---------------------------------------------------

df["PE_vs_sector_median_pct"] = (
    (
        df["pe_ratio"]
        -
        df["Sector_Median_PE"]
    )
    /
    df["Sector_Median_PE"]
) * 100

df["PE_vs_sector_median_pct"] = (
    df["PE_vs_sector_median_pct"]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
)

# ---------------------------------------------------
# FLAG
# ---------------------------------------------------

def valuation_flag(row):

    if pd.isna(row["pe_ratio"]):
        return "Fair"

    if row["pe_ratio"] > row["Sector_Median_PE"] * 1.5:
        return "Caution"

    if row["pe_ratio"] < row["Sector_Median_PE"] * 0.7:
        return "Discount"

    return "Fair"

df["flag"] = df.apply(
    valuation_flag,
    axis=1
)
print(df.columns.tolist())
print(df[["free_cash_flow_cr", "market_cap_crore"]].head())
df["FCF_yield_pct"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

df["FCF_yield_pct"] = (
    df["FCF_yield_pct"]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
)
print(df.columns.tolist())
print(df[["free_cash_flow_cr", "market_cap_crore"]].head())

valuation_summary = df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "5yr_median_PE",
        "PE_vs_sector_median_pct",
        "flag"
    ]
].copy()
print(f"Companies Processed : {valuation_summary['company_id'].nunique()}")
print("Unique Companies:", valuation_summary["company_id"].nunique())

valuation_summary.rename(
    columns={
        "broad_sector": "sector",
        "pe_ratio": "P/E",
        "pb_ratio": "P/B",
        "ev_ebitda": "EV/EBITDA"
    },
    inplace=True
)

# ---------------------------------------------------
# SAVE EXCEL
# ---------------------------------------------------

valuation_summary.to_excel(
    OUTPUT / "valuation_summary.xlsx",
    index=False
)

# ---------------------------------------------------
# SAVE FLAGGED COMPANIES
# ---------------------------------------------------

valuation_flags = valuation_summary[
    valuation_summary["flag"].isin(
        [
            "Caution",
            "Discount"
        ]
    )
].copy()

valuation_flags.to_csv(
    OUTPUT / "valuation_flags.csv",
    index=False
)

# ---------------------------------------------------
# DASHBOARD SUMMARY
# ---------------------------------------------------

print()
print("=" * 60)
print("VALUATION MODULE COMPLETED")
print("=" * 60)
print(f"Companies Processed : {len(valuation_summary)}")
print(f"Caution Companies  : {(valuation_summary['flag'] == 'Caution').sum()}")
print(f"Discount Companies : {(valuation_summary['flag'] == 'Discount').sum()}")
print(f"Fair Companies     : {(valuation_summary['flag'] == 'Fair').sum()}")
print()

print(
    "valuation_summary.xlsx saved to:",
    OUTPUT / "valuation_summary.xlsx"
)

print(
    "valuation_flags.csv saved to:",
    OUTPUT / "valuation_flags.csv"
)

print("=" * 60)
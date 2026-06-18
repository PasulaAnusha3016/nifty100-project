import pandas as pd

print("===== DATA QUALITY VALIDATION =====")

# Load Files
companies = pd.read_excel("data/raw/companies.xlsx", header=1)
pnl = pd.read_excel("data/raw/profitandloss.xlsx", header=1)
bs = pd.read_excel("data/raw/balancesheet.xlsx", header=1)

# DQ-01 Primary Key Uniqueness
duplicates = companies[companies.duplicated(subset=["id"])]

if len(duplicates) == 0:
    print("DQ-01 Passed: Company IDs are unique")
else:
    print("DQ-01 Failed")

# DQ-02 company_id + year uniqueness
duplicates = pnl[pnl.duplicated(subset=["company_id", "year"], keep=False)]

if len(duplicates) == 0:
    print(" DQ-02 Passed: company_id + year unique")
else:
    print(" DQ-02 Failed")
    print("\nDQ-02 Duplicate Records:")
    print(duplicates[["company_id", "year"]].head(20))

# DQ-03 Foreign Key Integrity
invalid = pnl[~pnl["company_id"].isin(companies["id"])]

if len(invalid) == 0:
    print("DQ-03 Passed: Foreign Keys valid")
else:
    print(" DQ-03 Failed")
    print("\nDQ-03 Invalid Company IDs:")
    print(invalid[["company_id"]].drop_duplicates())

# DQ-04 Balance Sheet Check
liability_sum = (
    bs["equity_capital"]
    + bs["reserves"]
    + bs["borrowings"]
    + bs["other_liabilities"]
)

difference = abs(liability_sum - bs["total_liabilities"])

failed_bs = bs[difference > 1]

if len(failed_bs) == 0:
    print(" DQ-04 Passed: Balance Sheet matches")
else:
    print(f" DQ-04 Failed: {len(failed_bs)} records")

# DQ-05 OPM Cross Check
calculated_opm = (pnl["operating_profit"] / pnl["sales"]) * 100

difference = abs(calculated_opm - pnl["opm_percentage"])

failed_opm = pnl[difference > 1]

if len(failed_opm) == 0:
    print(" DQ-05 Passed")
else:
    print(f" DQ-05 Failed: {len(failed_opm)} rows")

# DQ-06 Positive Sales
failed_sales = pnl[pnl["sales"] <= 0]

if len(failed_sales) == 0:
    print(" DQ-06 Passed")
else:
    print(f" DQ-06 Failed: {len(failed_sales)} rows")
    print("\nDQ-06 Sales <= 0:")
    print(failed_sales[["company_id", "year", "sales"]])

print("\n===== VALIDATION COMPLETED =====")
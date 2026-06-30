import sqlite3
import pandas as pd
from pathlib import Path

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
)

DB_PATH = Path("nifty100.db")

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("SELECT * FROM financial_ratios", conn)

if len(df) == 0:
    print("financial_ratios table is empty.")
else:

    df["net_profit_margin_pct"] = df.apply(
        lambda x: net_profit_margin(x["net_profit"], x["sales"]), axis=1
    )

    df["operating_profit_margin_pct"] = df.apply(
        lambda x: operating_profit_margin(x["operating_profit"], x["sales"]), axis=1
    )

    df["return_on_equity_pct"] = df.apply(
        lambda x: return_on_equity(
            x["net_profit"],
            x["equity_capital"],
            x["reserves"],
        ),
        axis=1,
    )

    df["return_on_capital_employed_pct"] = df.apply(
        lambda x: return_on_capital_employed(
            x["operating_profit"],
            x["equity_capital"],
            x["reserves"],
            x["borrowings"],
        ),
        axis=1,
    )

    df["return_on_assets_pct"] = df.apply(
        lambda x: return_on_assets(
            x["net_profit"],
            x["total_assets"],
        ),
        axis=1,
    )

    df["debt_to_equity_ratio"] = df.apply(
        lambda x: debt_to_equity(
            x["borrowings"],
            x["equity_capital"],
            x["reserves"],
        ),
        axis=1,
    )

    df["interest_coverage_ratio"] = df.apply(
        lambda x: interest_coverage(
            x["operating_profit"],
            x["other_income"],
            x["interest"],
        ),
        axis=1,
    )

    df["asset_turnover_ratio"] = df.apply(
        lambda x: asset_turnover(
            x["sales"],
            x["total_assets"],
        ),
        axis=1,
    )

    df.to_sql(
        "financial_ratios",
        conn,
        if_exists="replace",
        index=False,
    )

    print("Financial ratios populated successfully.")

conn.close()
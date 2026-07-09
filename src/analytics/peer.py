import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("nifty100.db")

# Load tables
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
peers = pd.read_sql("SELECT * FROM peer_groups", conn)

# Merge company with peer group
df = ratios.merge(peers, on="company_id", how="left")

# Metrics to rank
metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "asset_turnover"
]

results = []

for group in df["peer_group_name"].dropna().unique():

    group_df = df[df["peer_group_name"] == group].copy()

    for metric in metrics:

        if metric not in group_df.columns:
            continue

        ascending = metric == "debt_to_equity"

        group_df["percentile_rank"] = (
            group_df[metric]
            .rank(pct=True, ascending=ascending) * 100
        )

        for _, row in group_df.iterrows():

            results.append({
                "company_id": row["company_id"],
                "peer_group_name": group,
                "metric": metric,
                "value": row[metric],
                "percentile_rank": round(row["percentile_rank"],2),
                "year": row["year"]
            })

peer_df = pd.DataFrame(results)

peer_df.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

print("="*50)
print("Peer Percentiles Generated Successfully")
print("Rows:", len(peer_df))
print("="*50)

print(peer_df.head())

conn.close()
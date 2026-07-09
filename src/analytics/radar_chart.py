import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import os

# Connect to SQLite
conn = sqlite3.connect("nifty100.db")

# Read data
df = pd.read_sql("SELECT * FROM financial_ratios", conn)

conn.close()

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "asset_turnover"
]

os.makedirs("reports/radar_charts", exist_ok=True)

companies = df["company_id"].unique()[:20]   # First 20 companies

for company in companies:

    data = df[df["company_id"] == company].iloc[-1]

    values = []

    for metric in metrics:
        value = data.get(metric, 0)

        if pd.isna(value):
            value = 0

        values.append(float(value))

    values += values[:1]

    angles = [n / float(len(metrics)) * 2 * pi for n in range(len(metrics))]
    angles += angles[:1]

    plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=8)

    plt.title(company)

    plt.savefig(f"reports/radar_charts/{company}_radar.png")

    plt.close()

print("="*50)
print("Radar Charts Generated Successfully")
print("Location: reports/radar_charts")
print("="*50)
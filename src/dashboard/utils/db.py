import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.set_page_config(
    page_title="Nifty 100 Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty 100 Analytics Dashboard")

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

years = sorted(
    ratios["year"].dropna().unique()
)

selected_year = st.sidebar.selectbox(
    "Financial Year",
    years,
    index=len(years)-1
)

latest = ratios[
    ratios["year"] == selected_year
].copy()

st.write("Rows:", len(latest))
st.write("Companies:", latest["company_id"].nunique())
st.dataframe(latest.head())

st.subheader(f"Financial Snapshot : {selected_year}")

avg_roe = latest["return_on_equity_pct"].median()

median_de = latest["debt_to_equity"].median()

total_companies = latest["company_id"].nunique()

debt_free = len(
    latest[
        latest["debt_to_equity"] == 0
    ]
)

if "price_to_earnings" in latest.columns:
    median_pe = latest["price_to_earnings"].median()
else:
    median_pe = 0

if "revenue_cagr_5yr" in latest.columns:
    revenue_cagr = latest["revenue_cagr_5yr"].median()
else:
    revenue_cagr = 0

c1,c2,c3 = st.columns(3)

c1.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
)

c2.metric(
    "Median P/E",
    f"{median_pe:.2f}"
)

c3.metric(
    "Median Debt / Equity",
    f"{median_de:.2f}"
)

c4,c5,c6 = st.columns(3)

c4.metric(
    "Total Companies",
    total_companies
)

c5.metric(
    "Median Revenue CAGR",
    f"{revenue_cagr:.2f}%"
)

c6.metric(
    "Debt Free Companies",
    debt_free
)

st.divider()

st.subheader("Sector Distribution")
sector_count = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    hole=0.45
)

fig.update_layout(
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Top 5 Companies by Quality Score")

quality = latest.merge(
    companies[
        [
            "company_id",
            "company_name"
        ]
    ],
    on="company_id",
    how="left"
)

quality["quality_score"] = (
    quality["return_on_equity_pct"].fillna(0)
    + quality["interest_coverage"].fillna(0)
    + quality["asset_turnover"].fillna(0)
    - quality["debt_to_equity"].fillna(0)
)

top5 = quality.sort_values(
    "quality_score",
    ascending=False
).head(5)

table = top5[
    [
        "company_name",
        "quality_score",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage"
    ]
].copy()

table.columns = [
    "Company",
    "Quality Score",
    "ROE (%)",
    "Debt / Equity",
    "Interest Coverage"
]

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.success("Home Dashboard Loaded Successfully ✅")
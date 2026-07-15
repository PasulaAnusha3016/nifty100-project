import streamlit as st
import pandas as pd
import sqlite3

st.title("Home Dashboard")


conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("SELECT * FROM financial_ratios", conn)

conn.close()


years = sorted(df["year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    years,
    index=len(years) - 1
)

filtered_df = df[df["year"] == selected_year]


avg_roe = round(filtered_df["return_on_equity_pct"].mean(), 2)

median_de = round(filtered_df["debt_to_equity"].median(), 2)

total_companies = filtered_df["company_id"].nunique()

median_asset_turnover = round(filtered_df["asset_turnover"].median(), 2)

debt_free = len(filtered_df[filtered_df["debt_to_equity"] == 0])

total_records = len(filtered_df)


col1, col2, col3 = st.columns(3)

col1.metric("Average ROE", f"{avg_roe}%")
col2.metric("Median D/E", median_de)
col3.metric("Companies", total_companies)

col4, col5, col6 = st.columns(3)

col4.metric("Median Asset Turnover", median_asset_turnover)
col5.metric("Debt Free Companies", debt_free)
col6.metric("Total Records", total_records)

st.divider()
import plotly.express as px

# Load sector data
conn = sqlite3.connect("nifty100.db")

sector_df = pd.read_sql(
    "SELECT broad_sector, COUNT(company_id) AS company_count FROM sectors GROUP BY broad_sector",
    conn
)

conn.close()

st.subheader("Sector Breakdown")

fig = px.pie(
    sector_df,
    names="broad_sector",
    values="company_count",
    hole=0.5,
    title="Companies by Sector"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("Top 5 Companies by Composite Quality Score")

top5 = (
    filtered_df[
        ["company_id", "composite_quality_score"]
    ]
    .sort_values(
        by="composite_quality_score",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top5,
    use_container_width=True
)

st.subheader(f"Financial Ratios - {selected_year}")

st.dataframe(filtered_df.head(10))
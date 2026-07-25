import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Home Dashboard")

conn = sqlite3.connect("nifty100.db")

financial_df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sector_df = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

years = [
    "Mar 2013",
    "Mar 2014",
    "Mar 2015",
    "Mar 2016",
    "Mar 2017",
    "Mar 2018",
    "Mar 2019",
    "Mar 2020",
    "Mar 2021",
    "Mar 2022",
    "Mar 2023",
    "Mar 2024"
]

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    years,
    index=len(years)-1
)


filtered_df = financial_df[
    financial_df["year"] == selected_year
]

avg_roe = round(filtered_df["return_on_equity_pct"].mean(),2)
median_de = round(filtered_df["debt_to_equity"].median(),2)
total_companies = filtered_df["company_id"].nunique()
median_asset_turnover = round(filtered_df["asset_turnover"].median(),2)
debt_free = filtered_df[
    filtered_df["debt_to_equity"]==0
]["company_id"].nunique()
total_records = len(filtered_df)

c1,c2,c3 = st.columns(3)

c1.metric("Average ROE",f"{avg_roe}%")
c2.metric("Median D/E",median_de)
c3.metric("Companies",total_companies)

c4,c5,c6 = st.columns(3)

c4.metric("Median Asset Turnover",median_asset_turnover)
c5.metric("Debt Free Companies",debt_free)
c6.metric("Total Records",total_records)

st.divider()

st.subheader("Sector Distribution")

sector_chart = (
    sector_df
    .groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_chart,
    names="broad_sector",
    values="Companies",
    hole=0.5
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

st.subheader("Top 5 Companies by ROE")

top5 = (
    filtered_df[
        ["company_id","return_on_equity_pct"]
    ]
    .sort_values(
        by="return_on_equity_pct",
        ascending=False
    )
    .head(5)
)

top5.columns=[
    "Company",
    "ROE (%)"
]

st.dataframe(
    top5,
    hide_index=True,
    use_container_width=True
)
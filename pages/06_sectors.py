import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Sector Analysis",
    layout="wide"
)

st.header("Sector Analysis")

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

financial = financial[
    financial["year"].str.startswith("Mar")
].copy()

profit = profit[
    profit["year"].str.startswith("Mar")
].copy()

financial["year_num"] = (
    financial["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

profit["year_num"] = (
    profit["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

financial = financial[
    financial["year"].str.startswith("Mar")
].copy()

profit = profit[
    (profit["year"].str.startswith("Mar")) &
    (profit["year"] != "TTM")
].copy()

financial_latest = (
    financial
    .sort_values(["company_id", "year_num"])
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)

profit_latest = (
    profit
    .sort_values(["company_id", "year_num"])
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)
df = companies.merge(
    sectors,
    on="company_id",
    how="left"
)

df = df.merge(
    financial_latest,
    on="company_id",
    how="left"
)

df = df.merge(
    profit_latest[
        [
            "company_id",
            "sales"
        ]
    ],
    on="company_id",
    how="left"
)

numeric_columns = [

    "sales",

    "return_on_equity_pct",

    "debt_to_equity",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "interest_coverage",

    "asset_turnover",

    "free_cash_flow_cr"

]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.fillna(0)

size_map = {

    "Large Cap":120,

    "Mid Cap":80,

    "Small Cap":40

}

df["bubble_size"] = df[
    "market_cap_category"
].map(size_map)

df["bubble_size"] = df[
    "bubble_size"
].fillna(60)

sector = st.sidebar.selectbox(

    "Select Sector",

    sorted(
        df["broad_sector"].dropna().unique()
    )

)

sector_df = df[
    df["broad_sector"] == sector
].copy()

st.subheader(sector)
k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Companies",
    int(sector_df["company_id"].nunique())
)

k2.metric(
    "Median ROE",
    f"{sector_df['return_on_equity_pct'].median():.2f}%"
)

k3.metric(
    "Average Revenue",
    f"{sector_df['sales'].mean():,.0f}"
)

k4.metric(
    "Median Debt / Equity",
    f"{sector_df['debt_to_equity'].median():.2f}"
)

st.divider()

st.subheader("Revenue vs ROE")

fig = px.scatter(

    sector_df,

    x="sales",

    y="return_on_equity_pct",

    size="bubble_size",

    color="sub_sector",

    hover_name="company_name",

    hover_data=[

        "company_id",

        "market_cap_category",

        "sales",

        "return_on_equity_pct"

    ],

    labels={

        "sales":"Revenue",

        "return_on_equity_pct":"ROE (%)"

    },

    title=f"{sector} Companies"

)

fig.update_traces(

    marker=dict(

        opacity=0.75,

        line=dict(

            width=1,

            color="black"

        )

    )

)

fig.update_layout(

    height=650,

    xaxis_title="Revenue",

    yaxis_title="ROE (%)",

    legend_title="Sub Sector"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

st.subheader("Sector Snapshot")

c1, c2 = st.columns(2)

with c1:

    st.info(f"""

Sector

**{sector}**

Companies

**{sector_df['company_id'].nunique()}**

Average Revenue

**{sector_df['sales'].mean():,.0f}**

Median ROE

**{sector_df['return_on_equity_pct'].median():.2f}%**

""")

with c2:

    st.success(f"""

Median Net Profit Margin

**{sector_df['net_profit_margin_pct'].median():.2f}%**

Median Debt / Equity

**{sector_df['debt_to_equity'].median():.2f}**

Median Interest Coverage

**{sector_df['interest_coverage'].median():.2f}**

Median Asset Turnover

**{sector_df['asset_turnover'].median():.2f}**

""")

st.divider()
st.subheader("Sector Median Financial Metrics")

median_metrics = pd.DataFrame({

    "Metric":[

        "ROE",

        "Debt / Equity",

        "Net Profit Margin",

        "Operating Margin",

        "Interest Coverage",

        "Asset Turnover",

        "Free Cash Flow"

    ],

    "Value":[

        sector_df["return_on_equity_pct"].median(),

        sector_df["debt_to_equity"].median(),

        sector_df["net_profit_margin_pct"].median(),

        sector_df["operating_profit_margin_pct"].median(),

        sector_df["interest_coverage"].median(),

        sector_df["asset_turnover"].median(),

        sector_df["free_cash_flow_cr"].median()

    ]

})

fig = px.bar(

    median_metrics,

    x="Metric",

    y="Value",

    text="Value",

    color="Metric",

    title=f"{sector} Median Financial Metrics"

)

fig.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig.update_layout(

    height=550,

    showlegend=False,

    xaxis_title="",

    yaxis_title="Median Value"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

st.subheader("Top Companies in Sector")

top_df = sector_df[[

    "company_name",

    "sales",

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "debt_to_equity",

    "free_cash_flow_cr"

]].copy()

top_df = top_df.sort_values(

    by="return_on_equity_pct",

    ascending=False

)

top_df.columns = [

    "Company",

    "Revenue",

    "ROE (%)",

    "Net Profit Margin",

    "Debt / Equity",

    "Free Cash Flow"

]

st.dataframe(

    top_df,

    use_container_width=True,

    hide_index=True

)

st.divider()
st.subheader("Sub-sector Analysis")

subsector_summary = (

    sector_df

    .groupby("sub_sector", as_index=False)

    .agg(

        Companies=("company_id", "count"),

        Avg_Revenue=("sales", "mean"),

        Avg_ROE=("return_on_equity_pct", "mean"),

        Avg_Debt=("debt_to_equity", "mean")

    )

)

fig = px.bar(

    subsector_summary,

    x="sub_sector",

    y="Avg_ROE",

    color="Companies",

    text="Avg_ROE",

    title="Average ROE by Sub-sector"

)

fig.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig.update_layout(

    height=500,

    xaxis_title="Sub-sector",

    yaxis_title="Average ROE (%)"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

st.subheader("Sector Leaderboard")

leaderboard = sector_df[[

    "company_name",

    "sales",

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "interest_coverage",

    "asset_turnover"

]].copy()

leaderboard["Composite Score"] = (

    leaderboard["return_on_equity_pct"] * 0.40 +

    leaderboard["net_profit_margin_pct"] * 0.25 +

    leaderboard["interest_coverage"] * 0.20 +

    leaderboard["asset_turnover"] * 0.15

)

leaderboard = leaderboard.sort_values(

    "Composite Score",

    ascending=False

)

leaderboard = leaderboard.reset_index(drop=True)

leaderboard.index = leaderboard.index + 1

st.dataframe(

    leaderboard,

    use_container_width=True

)

st.divider()
st.subheader("Sector Insights")

highest_revenue = sector_df.loc[
    sector_df["sales"].idxmax()
]

highest_roe = sector_df.loc[
    sector_df["return_on_equity_pct"].idxmax()
]

lowest_debt = sector_df.loc[
    sector_df["debt_to_equity"].idxmin()
]

col1, col2, col3 = st.columns(3)

with col1:

    st.success(f"""
### Highest Revenue

**{highest_revenue['company_name']}**

Revenue

{highest_revenue['sales']:,.0f}
""")

with col2:

    st.info(f"""
### Highest ROE

**{highest_roe['company_name']}**

ROE

{highest_roe['return_on_equity_pct']:.2f}%
""")

with col3:

    st.warning(f"""
### Lowest Debt

**{lowest_debt['company_name']}**

Debt / Equity

{lowest_debt['debt_to_equity']:.2f}
""")

st.divider()

st.subheader("Download Sector Data")

download_df = sector_df[[
    "company_id",
    "company_name",
    "broad_sector",
    "sub_sector",
    "sales",
    "return_on_equity_pct",
    "debt_to_equity",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "market_cap_category"
]].copy()

download_df.columns = [
    "Ticker",
    "Company",
    "Sector",
    "Sub Sector",
    "Revenue",
    "ROE",
    "Debt_Equity",
    "Net_Profit_Margin",
    "Operating_Margin",
    "Interest_Coverage",
    "Asset_Turnover",
    "Free_Cash_Flow",
    "Market_Cap_Category"
]

csv = download_df.to_csv(index=False)

st.download_button(
    label="📥 Download Sector Analysis CSV",
    data=csv,
    file_name=f"{sector.replace(' ','_')}_Sector_Analysis.csv",
    mime="text/csv"
)

st.divider()

st.info("""
### Data Note

• Financial metrics are taken from the latest available annual report.

• Bubble size represents the Market Cap Category because
numeric market capitalization is not available in the database.

• Charts automatically update whenever another sector is selected.
""")

st.caption(
    "Nifty 100 Analytics Dashboard | Sprint 4 | Sector Analysis"
)
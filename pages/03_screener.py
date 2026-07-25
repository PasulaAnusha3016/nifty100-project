import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Company Screener",
    layout="wide"
)

st.title("Company Screener")

# -----------------------------
# Database
# -----------------------------

conn = sqlite3.connect("nifty100.db")

financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# -----------------------------
# Year Selection
# -----------------------------

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
    "Financial Year",
    years,
    index=len(years)-1
)

financial = financial[
    financial["year"] == selected_year
].copy()

financial = financial.fillna(0)

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filters")

roe_filter = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    100,
    15
)

de_filter = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    10.0,
    1.0
)

fcf_filter = st.sidebar.slider(
    "Minimum Free Cash Flow",
    -5000,
    50000,
    0
)

npm_filter = st.sidebar.slider(
    "Minimum Net Profit Margin",
    0,
    100,
    10
)

opm_filter = st.sidebar.slider(
    "Minimum Operating Margin",
    -100,
    100,
    10
)

interest_filter = st.sidebar.slider(
    "Minimum Interest Coverage",
    0,
    500,
    5
)

asset_filter = st.sidebar.slider(
    "Minimum Asset Turnover",
    0.0,
    5.0,
    0.50
)

capex_filter = st.sidebar.slider(
    "Maximum Capex",
    -10000,
    50000,
    50000
)

dividend_filter = st.sidebar.slider(
    "Minimum Dividend Payout (%)",
    0,
    100,
    0
)

debt_filter = st.sidebar.slider(
    "Maximum Total Debt",
    0,
    500000,
    500000
)
# -----------------------------
# Preset Filters
# -----------------------------

st.sidebar.header("Quick Presets")

preset = st.sidebar.radio(

    "Choose Preset",

    [

        "Custom",

        "Quality",

        "Value",

        "Growth",

        "Dividend",

        "Debt-Free",

        "Turnaround"

    ]

)

if preset == "Quality":

    roe_filter = 20
    de_filter = 0.50
    npm_filter = 15
    interest_filter = 10
    asset_filter = 0.75

elif preset == "Value":

    roe_filter = 10
    de_filter = 1.00
    dividend_filter = 20

elif preset == "Growth":

    roe_filter = 18
    npm_filter = 15
    asset_filter = 0.80

elif preset == "Dividend":

    dividend_filter = 30

elif preset == "Debt-Free":

    de_filter = 0

elif preset == "Turnaround":

    roe_filter = 5
    npm_filter = 5
    de_filter = 2

# -----------------------------
# Apply Filters
# -----------------------------

filtered = financial.copy()

filtered = filtered[

    filtered["return_on_equity_pct"] >= roe_filter

]

filtered = filtered[

    filtered["debt_to_equity"] <= de_filter

]

filtered = filtered[

    filtered["free_cash_flow_cr"] >= fcf_filter

]

filtered = filtered[

    filtered["net_profit_margin_pct"] >= npm_filter

]

filtered = filtered[

    filtered["operating_profit_margin_pct"] >= opm_filter

]

filtered = filtered[

    filtered["interest_coverage"] >= interest_filter

]

filtered = filtered[

    filtered["asset_turnover"] >= asset_filter

]

filtered = filtered[

    filtered["capex_cr"] <= capex_filter

]

filtered = filtered[

    filtered["dividend_payout_ratio_pct"] >= dividend_filter

]

filtered = filtered[

    filtered["total_debt_cr"] <= debt_filter

]

# -----------------------------
# Composite Quality Score
# -----------------------------

filtered["quality_score"] = (

    filtered["return_on_equity_pct"]

    +

    filtered["interest_coverage"]

    +

    filtered["asset_turnover"]

    +

    filtered["net_profit_margin_pct"]

    -

    filtered["debt_to_equity"]

)

# -----------------------------
# Merge Company Details
# -----------------------------

filtered = filtered.merge(

    companies[

        [

            "company_id",

            "company_name"

        ]

    ],

    on="company_id",

    how="left"

)

filtered = filtered.merge(

    sectors[

        [

            "company_id",

            "broad_sector"

        ]

    ],

    on="company_id",

    how="left"

)
# ------------------------------------
# Dashboard Summary
# ------------------------------------

st.title("Company Screener")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies Matching",
    len(filtered)
)

c2.metric(
    "Average ROE",
    round(
        filtered["return_on_equity_pct"].mean(),
        2
    ) if not filtered.empty else 0
)

c3.metric(
    "Average Quality Score",
    round(
        filtered["quality_score"].mean(),
        2
    ) if not filtered.empty else 0
)

st.divider()

# ------------------------------------
# Sort Results
# ------------------------------------

sort_by = st.selectbox(

    "Sort Results By",

    [

        "Quality Score",

        "ROE",

        "Net Profit Margin",

        "Free Cash Flow",

        "Debt / Equity"

    ]

)

if sort_by == "Quality Score":

    filtered = filtered.sort_values(
        "quality_score",
        ascending=False
    )

elif sort_by == "ROE":

    filtered = filtered.sort_values(
        "return_on_equity_pct",
        ascending=False
    )

elif sort_by == "Net Profit Margin":

    filtered = filtered.sort_values(
        "net_profit_margin_pct",
        ascending=False
    )

elif sort_by == "Free Cash Flow":

    filtered = filtered.sort_values(
        "free_cash_flow_cr",
        ascending=False
    )

elif sort_by == "Debt / Equity":

    filtered = filtered.sort_values(
        "debt_to_equity"
    )

# ------------------------------------
# Display Table
# ------------------------------------

display = filtered[

    [

        "company_name",

        "broad_sector",

        "quality_score",

        "return_on_equity_pct",

        "debt_to_equity",

        "net_profit_margin_pct",

        "operating_profit_margin_pct",

        "interest_coverage",

        "asset_turnover",

        "free_cash_flow_cr"

    ]

].copy()

display.columns = [

    "Company",

    "Sector",

    "Quality Score",

    "ROE (%)",

    "Debt / Equity",

    "Net Profit Margin",

    "Operating Margin",

    "Interest Coverage",

    "Asset Turnover",

    "Free Cash Flow"

]

st.subheader("Screening Results")

st.dataframe(

    display,

    hide_index=True,

    use_container_width=True

)

st.write(

    f"**{len(display)} companies match your filters.**"

)

st.divider()
# ---------------------------------------------
# Top Companies by Quality Score
# ---------------------------------------------

st.subheader("Top 10 Companies by Quality Score")

top10 = display.sort_values(
    by="Quality Score",
    ascending=False
).head(10)

st.dataframe(
    top10,
    hide_index=True,
    use_container_width=True
)

st.divider()

# ---------------------------------------------
# Sector Distribution
# ---------------------------------------------

st.subheader("Sector Distribution")

sector_summary = (
    filtered
    .groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

if not sector_summary.empty:

    fig = px.bar(
        sector_summary,
        x="broad_sector",
        y="Companies",
        color="Companies",
        text="Companies"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Companies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No sector data available.")

st.divider()

# ---------------------------------------------
# Final Summary
# ---------------------------------------------

summary1, summary2 = st.columns(2)

with summary1:

    st.info(
        f"""
Selected Financial Year

**{selected_year}**

Companies Matched

**{len(display)}**
"""
    )

with summary2:

    if not filtered.empty:

        best = filtered.iloc[0]["company_name"]

        st.success(
            f"""
Highest Ranked Company

**{best}**

Quality Score

**{round(filtered.iloc[0]['quality_score'],2)}**
"""
        )

    else:

        st.warning("No companies available.")

st.divider()

st.caption(
    "Nifty 100 Analytics Dashboard | Sprint 4 | Company Screener"
)
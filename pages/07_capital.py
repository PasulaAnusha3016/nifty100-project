import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Capital Allocation Map",
    layout="wide"
)

st.header("Capital Allocation Map")

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

financial_latest = (
    financial
    .sort_values(
        ["company_id", "year_num"]
    )
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)

profit_latest = (
    profit
    .sort_values(
        ["company_id", "year_num"]
    )
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)

df = companies.merge(
    financial_latest,
    on="company_id",
    how="left"
)

df = df.merge(
    profit_latest[
        [
            "company_id",
            "sales",
            "net_profit"
        ]
    ],
    on="company_id",
    how="left"
)

numeric_cols = [

    "return_on_equity_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "dividend_payout_ratio_pct",

    "capex_cr",

    "sales",

    "net_profit"

]

for col in numeric_cols:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.fillna(0)
def classify_company(row):

    roe = row["return_on_equity_pct"]
    debt = row["debt_to_equity"]
    fcf = row["free_cash_flow_cr"]
    payout = row["dividend_payout_ratio_pct"]
    capex = row["capex_cr"]

    if roe >= 20 and debt <= 0.5:
        return "Capital Efficient"

    elif payout >= 40:
        return "Dividend Compounder"

    elif capex > fcf:
        return "Aggressive Expansion"

    elif fcf > 0 and debt <= 1:
        return "Cash Generator"

    elif debt > 2:
        return "Highly Leveraged"

    elif roe < 10 and debt > 1:
        return "Turnaround"

    elif capex <= 0:
        return "Asset Light"

    else:
        return "Balanced Allocation"


df["Capital Pattern"] = df.apply(
    classify_company,
    axis=1
)

patterns = sorted(
    df["Capital Pattern"].unique()
)

selected_pattern = st.sidebar.selectbox(
    "Capital Allocation Pattern",
    patterns
)

pattern_df = df[
    df["Capital Pattern"] == selected_pattern
].copy()

# ---------------------------------------
# KPI CARDS
# ---------------------------------------

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Companies",
    int(pattern_df["company_id"].nunique())
)

k2.metric(
    "Median ROE",
    f"{pattern_df['return_on_equity_pct'].median():.2f}%"
)

k3.metric(
    "Average FCF",
    f"{pattern_df['free_cash_flow_cr'].mean():,.0f}"
)

k4.metric(
    "Median Debt / Equity",
    f"{pattern_df['debt_to_equity'].median():.2f}"
)

st.divider()
st.subheader("Capital Allocation Treemap")

treemap_df = (

    df.groupby(
        ["Capital Pattern", "company_name"],
        as_index=False
    )

    .agg(

        Revenue=("sales", "sum"),

        ROE=("return_on_equity_pct", "mean")

    )

)

fig = px.treemap(

    treemap_df,

    path=[
        "Capital Pattern",
        "company_name"
    ],

    values="Revenue",

    color="ROE",

    color_continuous_scale="RdYlGn",

    hover_data=[
        "Revenue",
        "ROE"
    ]

)

fig.update_layout(

    height=700,

    margin=dict(
        t=50,
        l=20,
        r=20,
        b=20
    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ---------------------------------------
# PATTERN DISTRIBUTION
# ---------------------------------------

st.subheader("Capital Allocation Distribution")

distribution = (

    df.groupby(
        "Capital Pattern",
        as_index=False
    )

    .size()

)

distribution.columns = [

    "Capital Pattern",

    "Companies"

]

fig = px.bar(

    distribution,

    x="Capital Pattern",

    y="Companies",

    text="Companies",

    color="Capital Pattern"

)

fig.update_traces(

    textposition="outside"

)

fig.update_layout(

    showlegend=False,

    height=500,

    xaxis_title="Capital Allocation Pattern",

    yaxis_title="Number of Companies"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()
# ---------------------------------------
# COMPANIES IN SELECTED PATTERN
# ---------------------------------------

st.subheader(f"Companies in '{selected_pattern}'")

company_table = pattern_df[
    [
        "company_name",
        "sales",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "dividend_payout_ratio_pct",
        "capex_cr"
    ]
].copy()

company_table.columns = [

    "Company",

    "Revenue",

    "ROE (%)",

    "Debt / Equity",

    "Free Cash Flow",

    "Dividend Payout (%)",

    "CapEx"

]

company_table = company_table.sort_values(

    "ROE (%)",

    ascending=False

)

st.dataframe(

    company_table,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ---------------------------------------
# PATTERN INSIGHTS
# ---------------------------------------

highest_roe = pattern_df.loc[
    pattern_df["return_on_equity_pct"].idxmax()
]

highest_fcf = pattern_df.loc[
    pattern_df["free_cash_flow_cr"].idxmax()
]

lowest_debt = pattern_df.loc[
    pattern_df["debt_to_equity"].idxmin()
]

c1, c2, c3 = st.columns(3)

with c1:

    st.success(f"""

### Highest ROE

**{highest_roe['company_name']}**

ROE

{highest_roe['return_on_equity_pct']:.2f}%

""")

with c2:

    st.info(f"""

### Highest Free Cash Flow

**{highest_fcf['company_name']}**

FCF

{highest_fcf['free_cash_flow_cr']:,.0f}

""")

with c3:

    st.warning(f"""

### Lowest Debt

**{lowest_debt['company_name']}**

Debt / Equity

{lowest_debt['debt_to_equity']:.2f}

""")

st.divider()

# ---------------------------------------
# PATTERN SUMMARY
# ---------------------------------------

st.subheader("Pattern Summary")

left, right = st.columns(2)

with left:

    st.info(f"""

Pattern

**{selected_pattern}**

Companies

**{len(pattern_df)}**

Average Revenue

**{pattern_df['sales'].mean():,.0f}**

Average ROE

**{pattern_df['return_on_equity_pct'].mean():.2f}%**

""")

with right:

    st.success(f"""

Average Free Cash Flow

**{pattern_df['free_cash_flow_cr'].mean():,.0f}**

Average Debt / Equity

**{pattern_df['debt_to_equity'].mean():.2f}**

Average Dividend Payout

**{pattern_df['dividend_payout_ratio_pct'].mean():.2f}%**

""")

st.divider()
st.subheader("Download Capital Allocation Data")

download_df = pattern_df[
    [
        "company_id",
        "company_name",
        "Capital Pattern",
        "sales",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "dividend_payout_ratio_pct",
        "capex_cr"
    ]
].copy()

download_df.columns = [

    "Ticker",

    "Company",

    "Capital Pattern",

    "Revenue",

    "ROE (%)",

    "Debt / Equity",

    "Free Cash Flow",

    "Dividend Payout (%)",

    "CapEx"

]

csv = download_df.to_csv(index=False)

st.download_button(

    label="📥 Download Capital Allocation CSV",

    data=csv,

    file_name=f"{selected_pattern.replace(' ','_')}_Capital_Allocation.csv",

    mime="text/csv"

)

st.divider()

st.subheader("Capital Allocation Overview")

summary = (

    df.groupby(
        "Capital Pattern",
        as_index=False
    )

    .agg(

        Companies=("company_id", "count"),

        Avg_ROE=("return_on_equity_pct", "mean"),

        Avg_Debt=("debt_to_equity", "mean"),

        Avg_FCF=("free_cash_flow_cr", "mean")

    )

)

summary.columns = [

    "Capital Pattern",

    "Companies",

    "Average ROE",

    "Average Debt",

    "Average Free Cash Flow"

]

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)

st.divider()

st.info(
    """
**Capital Allocation Interpretation**

• Capital Efficient → High ROE with low leverage

• Cash Generator → Strong Free Cash Flow with manageable debt

• Dividend Compounder → High dividend payout companies

• Aggressive Expansion → Heavy CapEx investments

• Highly Leveraged → Debt-intensive companies

• Asset Light → Low CapEx business model

• Balanced Allocation → Healthy balance across all metrics

• Turnaround → Lower profitability with improving fundamentals
"""
)

st.divider()

st.caption(
    "Nifty 100 Analytics Dashboard | Sprint 4 | Capital Allocation Map"
)
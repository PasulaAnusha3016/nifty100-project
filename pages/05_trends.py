import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)
st.header("Trend Analysis")

# -----------------------------
# DATABASE
# -----------------------------

conn = sqlite3.connect("nifty100.db")

financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

companies = pd.read_sql(
    "SELECT company_id, company_name FROM companies",
    conn
)

conn.close()

# -----------------------------
# SIDEBAR
# -----------------------------

company = st.sidebar.selectbox(

    "Select Company",

    sorted(companies["company_name"])

)

company_id = companies.loc[
    companies["company_name"] == company,
    "company_id"
].values[0]

financial = financial[
    financial["company_id"] == company_id
].copy()

profit = profit[
    profit["company_id"] == company_id
].copy()

financial = financial.sort_values("year")

profit = profit.sort_values("year")

financial = financial.fillna(0)

profit = profit.fillna(0)

# ---------------------------------------
# KPI CARDS
# ---------------------------------------

latest = financial.sort_values("year").iloc[-1]

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "ROE (%)",
    round(latest["return_on_equity_pct"], 2)
)

k2.metric(
    "Debt / Equity",
    round(latest["debt_to_equity"], 2)
)

k3.metric(
    "Net Profit Margin",
    round(latest["net_profit_margin_pct"], 2)
)

k4.metric(
    "Free Cash Flow",
    round(latest["free_cash_flow_cr"], 2)
)

st.divider()

# ---------------------------------------
# REVENUE TREND
# ---------------------------------------

st.subheader("Revenue Trend (10 Years)")

profit["sales"] = pd.to_numeric(
    profit["sales"],
    errors="coerce"
)

profit = profit.dropna(subset=["sales"])

fig = px.line(

    profit,

    x="year",

    y="sales",

    markers=True,

    title="Revenue Growth"

)

fig.update_layout(

    xaxis_title="Financial Year",

    yaxis_title="Revenue"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()
# ---------------------------------------
# NET PROFIT TREND
# ---------------------------------------

st.subheader("Net Profit Trend (10 Years)")

profit["net_profit"] = pd.to_numeric(
    profit["net_profit"],
    errors="coerce"
)

profit = profit.dropna(subset=["net_profit"])

fig = px.line(

    profit,

    x="year",

    y="net_profit",

    markers=True,

    title="Net Profit Growth"

)

fig.update_layout(

    xaxis_title="Financial Year",

    yaxis_title="Net Profit"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ---------------------------------------
# ROE TREND
# ---------------------------------------

st.subheader("Return on Equity (ROE) Trend")

financial["return_on_equity_pct"] = pd.to_numeric(

    financial["return_on_equity_pct"],

    errors="coerce"

)

fig = px.line(

    financial,

    x="year",

    y="return_on_equity_pct",

    markers=True,

    title="ROE (%) Over Time"

)

fig.update_layout(

    xaxis_title="Financial Year",

    yaxis_title="ROE (%)"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()
# ---------------------------------------
# DEBT / EQUITY TREND
# ---------------------------------------

st.subheader("Debt / Equity Trend")

financial["debt_to_equity"] = pd.to_numeric(
    financial["debt_to_equity"],
    errors="coerce"
)

fig = px.line(
    financial,
    x="year",
    y="debt_to_equity",
    markers=True,
    title="Debt / Equity Over Time"
)

fig.update_layout(
    xaxis_title="Financial Year",
    yaxis_title="Debt / Equity Ratio"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# FREE CASH FLOW TREND
# ---------------------------------------

st.subheader("Free Cash Flow Trend")

financial["free_cash_flow_cr"] = pd.to_numeric(
    financial["free_cash_flow_cr"],
    errors="coerce"
)

fig = px.bar(
    financial,
    x="year",
    y="free_cash_flow_cr",
    title="Free Cash Flow (₹ Cr)"
)

fig.update_layout(
    xaxis_title="Financial Year",
    yaxis_title="Free Cash Flow (₹ Cr)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
# ---------------------------------------
# REVENUE CAGR SUMMARY
# ---------------------------------------

st.subheader("Trend Summary")

summary1, summary2 = st.columns(2)

first_sales = profit["sales"].dropna()

if len(first_sales) >= 2:

    start_sales = first_sales.iloc[0]
    end_sales = first_sales.iloc[-1]

    years_count = len(first_sales) - 1

    if start_sales > 0:

        revenue_cagr = (
            ((end_sales / start_sales) ** (1 / years_count)) - 1
        ) * 100

    else:

        revenue_cagr = 0

else:

    revenue_cagr = 0

with summary1:

    st.metric(
        "Revenue CAGR",
        f"{revenue_cagr:.2f}%"
    )

    st.metric(
        "Latest Revenue",
        round(
            profit["sales"].iloc[-1],
            2
        )
    )

with summary2:

    st.metric(
        "Latest Net Profit",
        round(
            profit["net_profit"].iloc[-1],
            2
        )
    )

    st.metric(
        "Latest ROE",
        round(
            financial["return_on_equity_pct"].iloc[-1],
            2
        )
    )

st.divider()

# ---------------------------------------
# DOWNLOAD DATA
# ---------------------------------------

st.subheader("Download Trend Data")

trend_data = financial.merge(

    profit,

    on=[
        "company_id",
        "year"
    ],

    how="left"

)

csv = trend_data.to_csv(
    index=False
)

st.download_button(

    label="Download Trend Data (CSV)",

    data=csv,

    file_name=f"{company_id}_trend_analysis.csv",

    mime="text/csv"

)

st.divider()

# ---------------------------------------
# FOOTER
# ---------------------------------------

st.caption(
    "Nifty 100 Analytics Dashboard | Sprint 4 | Trend Analysis"
)
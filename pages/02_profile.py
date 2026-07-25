import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Company Profile",
    layout="wide"
)

st.title("Company Profile")

# -------------------------
# Database Connection
# -------------------------

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

analysis = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

proscons = pd.read_sql(
    "SELECT * FROM prosandcons",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# -------------------------
# Company Search
# -------------------------

company_names = companies[
    ["company_id","company_name"]
].copy()

company_names["Display"] = (
    company_names["company_id"]
    + " - "
    + company_names["company_name"]
)

selected = st.selectbox(
    "Search Company",
    sorted(company_names["Display"])
)

selected_company = selected.split(" - ")[0]

# -------------------------
# Company Information
# -------------------------

company = companies[
    companies["company_id"] == selected_company
]

if company.empty:

    st.warning(
        "Ticker not found — please try another."
    )

    st.stop()

company = company.iloc[0]

sector_info = sectors[
    sectors["company_id"] == selected_company
]

if not sector_info.empty:

    sector_info = sector_info.iloc[0]

    sector_name = sector_info["broad_sector"]

    sub_sector = sector_info["sub_sector"]

else:

    sector_name = "N/A"

    sub_sector = "N/A"

st.markdown("---")

left,right = st.columns([1,3])

with left:

    try:

        st.image(
            company["company_logo"],
            width=150
        )

    except:

        st.info("Logo not available")

with right:

    st.subheader(company["company_name"])

    info1,info2 = st.columns(2)

    with info1:

        st.write("**Ticker**")
        st.write(company["company_id"])

        st.write("**Sector**")
        st.write(sector_name)

        st.write("**Sub Sector**")
        st.write(sub_sector)

    with info2:

        st.write("**Face Value**")
        st.write(company["face_value"])

        st.write("**Book Value**")
        st.write(company["book_value"])

        st.write("**Website**")
        st.write(company["website"])

st.markdown("### About Company")

st.write(
    company["about_company"]
)

st.divider()

# -------------------------
# Latest Financial Data
# -------------------------

latest = financial[
    financial["company_id"] == selected_company
].copy()

if latest.empty:

    st.warning(
        "Financial data not available for this company."
    )

    st.stop()

latest = latest.sort_values("year")

latest = latest.iloc[-1]
k1,k2,k3 = st.columns(3)

k1.metric(
    "ROE (%)",
    round(
        latest["return_on_equity_pct"],
        2
    )
)

k2.metric(
    "Debt / Equity",
    round(
        latest["debt_to_equity"],
        2
    )
)

k3.metric(
    "Net Profit Margin",
    round(
        latest["net_profit_margin_pct"],
        2
    )
)

k4,k5,k6 = st.columns(3)

k4.metric(
    "Operating Margin",
    round(
        latest["operating_profit_margin_pct"],
        2
    )
)

k5.metric(
    "Interest Coverage",
    round(
        latest["interest_coverage"],
        2
    )
)

k6.metric(
    "Free Cash Flow",
    round(
        latest["free_cash_flow_cr"],
        2
    )
)

st.divider()
# -------------------------
# Revenue & Net Profit Trend
# -------------------------

st.subheader("Revenue & Net Profit (10 Years)")

profit_data = profit[
    profit["company_id"] == selected_company
].copy()

profit_data = profit_data[
    profit_data["year"] != "TTM"
]

profit_data["sales"] = pd.to_numeric(
    profit_data["sales"],
    errors="coerce"
)

profit_data["net_profit"] = pd.to_numeric(
    profit_data["net_profit"],
    errors="coerce"
)

profit_data = profit_data.sort_values("year")

col1, col2 = st.columns(2)

with col1:

    fig_sales = px.bar(
        profit_data,
        x="year",
        y="sales",
        title="Revenue (10 Years)",
        text_auto=True
    )

    fig_sales.update_layout(
        xaxis_title="Year",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )

with col2:

    fig_profit = px.bar(
        profit_data,
        x="year",
        y="net_profit",
        title="Net Profit (10 Years)",
        text_auto=True
    )

    fig_profit.update_layout(
        xaxis_title="Year",
        yaxis_title="Net Profit"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

st.divider()

# -------------------------
# ROE vs ROCE Trend
# -------------------------

st.subheader("ROE vs ROCE")

trend = financial[
    financial["company_id"] == selected_company
].copy()

trend = trend.sort_values("year")

trend["ROE"] = pd.to_numeric(
    trend["return_on_equity_pct"],
    errors="coerce"
)

roce_value = company["roce_percentage"]

trend["ROCE"] = roce_value

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=trend["year"],
        y=trend["ROE"],
        mode="lines+markers",
        name="ROE"

    )

)

fig.add_trace(

    go.Scatter(

        x=trend["year"],
        y=trend["ROCE"],
        mode="lines+markers",
        name="ROCE"

    )

)

fig.update_layout(

    title="ROE vs ROCE (10 Years)",

    xaxis_title="Year",

    yaxis_title="Percentage",

    legend_title="Metrics"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# -------------------------
# Pros & Cons
# -------------------------

st.subheader("Pros & Cons")

pc = proscons[
    proscons["company_id"] == selected_company
]

if not pc.empty:

    p1, p2 = st.columns(2)

    with p1:

        st.success("Pros")

        for item in pc["pros"].dropna():

            st.markdown(f"- {item}")

    with p2:

        st.error("Cons")

        for item in pc["cons"].dropna():

            st.markdown(f"- {item}")

else:

    st.info("No Pros & Cons available.")

st.divider()
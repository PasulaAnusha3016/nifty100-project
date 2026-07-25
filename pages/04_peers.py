import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Peer Comparison",
    layout="wide"
)

st.title("Peer Comparison")

# -----------------------------------
# DATABASE
# -----------------------------------

conn = sqlite3.connect("nifty100.db")

peer_groups = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

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

# -----------------------------------
# YEAR SELECTOR
# -----------------------------------

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

# -----------------------------------
# PEER GROUP
# -----------------------------------

peer_group = st.sidebar.selectbox(

    "Peer Group",

    sorted(
        peer_groups["peer_group_name"].dropna().unique()
    )

)

peer_df = peer_groups[
    peer_groups["peer_group_name"] == peer_group
]

# -----------------------------------
# FINANCIAL DATA
# -----------------------------------

comparison = financial.merge(

    peer_df,

    on="company_id",

    how="inner"

)

comparison = comparison.merge(

    companies[
        [
            "company_id",
            "company_name"
        ]
    ],

    on="company_id",

    how="left"

)

comparison = comparison.merge(

    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],

    on="company_id",

    how="left"

)

comparison = comparison[
    comparison["year"] == selected_year
]

comparison = comparison.drop_duplicates(
    subset="company_id"
)

# -----------------------------------
# COMPANY SELECTOR
# -----------------------------------


# -----------------------------------
# QUALITY SCORE
# -----------------------------------

comparison["quality_score"] = (

    comparison["return_on_equity_pct"].fillna(0)

    +

    comparison["interest_coverage"].fillna(0)

    +

    comparison["asset_turnover"].fillna(0)

    +

    comparison["net_profit_margin_pct"].fillna(0)

    -

    comparison["debt_to_equity"].fillna(0)

)
# -----------------------------------
# COMPANY SELECTOR
# -----------------------------------

selected_company = st.selectbox(

    "Select Company",

    sorted(
        comparison["company_name"].dropna().unique()
    )

)

company_data = comparison[
    comparison["company_name"] == selected_company
]

if company_data.empty:

    st.warning(
        "Company not available in selected peer group."
    )

    st.stop()

company_data = company_data.iloc[0]

# -----------------------------------
# PEER AVERAGES
# -----------------------------------

peer_average = comparison[

    [

        "return_on_equity_pct",

        "debt_to_equity",

        "net_profit_margin_pct",

        "operating_profit_margin_pct",

        "interest_coverage",

        "asset_turnover",

        "free_cash_flow_cr",

        "quality_score"

    ]

].mean()

# -----------------------------------
# COMPANY VALUES
# -----------------------------------

company_values = [

    company_data["return_on_equity_pct"],

    company_data["debt_to_equity"],

    company_data["net_profit_margin_pct"],

    company_data["operating_profit_margin_pct"],

    company_data["interest_coverage"],

    company_data["asset_turnover"],

    company_data["free_cash_flow_cr"],

    company_data["quality_score"]

]

peer_radar = [
    peer_average["return_on_equity_pct"],
    peer_average["debt_to_equity"],
    peer_average["net_profit_margin_pct"],
    peer_average["operating_profit_margin_pct"],
    peer_average["interest_coverage"],
    peer_average["asset_turnover"]
]
company_radar = [
    company_data["return_on_equity_pct"],
    company_data["debt_to_equity"],
    company_data["net_profit_margin_pct"],
    company_data["operating_profit_margin_pct"],
    company_data["interest_coverage"],
    company_data["asset_turnover"]
]


# -----------------------------------
# KPI SUMMARY
# -----------------------------------

st.subheader("Selected Company")

k1, k2, k3 = st.columns(3)

k1.metric(

    "ROE",

    round(

        company_data["return_on_equity_pct"],

        2

    )

)

k2.metric(

    "Debt / Equity",

    round(

        company_data["debt_to_equity"],

        2

    )

)

k3.metric(

    "Quality Score",

    round(

        company_data["quality_score"],

        2

    )

)

st.divider()

st.subheader("Company vs Peer Average")

peer1, peer2, peer3 = st.columns(3)

peer1.metric(
    "ROE",
    round(company_data["return_on_equity_pct"],2),
    round(
        company_data["return_on_equity_pct"] -
        peer_average["return_on_equity_pct"],
        2
    )
)

peer2.metric(
    "Net Profit Margin",
    round(company_data["net_profit_margin_pct"],2),
    round(
        company_data["net_profit_margin_pct"] -
        peer_average["net_profit_margin_pct"],
        2
    )
)

peer3.metric(
    "Interest Coverage",
    round(company_data["interest_coverage"],2),
    round(
        company_data["interest_coverage"] -
        peer_average["interest_coverage"],
        2
    )
)

peer4, peer5, peer6 = st.columns(3)

peer4.metric(
    "Debt / Equity",
    round(company_data["debt_to_equity"],2),
    round(
        company_data["debt_to_equity"] -
        peer_average["debt_to_equity"],
        2
    )
)

peer5.metric(
    "Asset Turnover",
    round(company_data["asset_turnover"],2),
    round(
        company_data["asset_turnover"] -
        peer_average["asset_turnover"],
        2
    )
)

peer6.metric(
    "Free Cash Flow",
    round(company_data["free_cash_flow_cr"],2),
    round(
        company_data["free_cash_flow_cr"] -
        peer_average["free_cash_flow_cr"],
        2
    )
)

st.divider()
# -----------------------------------
# PEER COMPARISON RADAR
# -----------------------------------

st.subheader("Peer Comparison Radar")

radar_columns = [

    "return_on_equity_pct",

    "debt_to_equity",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "interest_coverage",

    "asset_turnover"

]

radar_labels = [

    "ROE",

    "Debt / Equity",

    "Net Margin",

    "Operating Margin",

    "Interest Coverage",

    "Asset Turnover"

]

company_radar = []
peer_radar = []

for col in radar_columns:

    max_value = comparison[col].fillna(0).max()

    if max_value == 0:
        max_value = 1

    company_radar.append(

        (float(company_data[col]) / max_value) * 100

    )

    peer_radar.append(

        (float(peer_average[col]) / max_value) * 100

    )

company_radar.append(company_radar[0])
peer_radar.append(peer_radar[0])
radar_labels.append(radar_labels[0])

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=company_radar,

        theta=radar_labels,

        fill="toself",

        name=selected_company,

        line=dict(width=3)

    )

)

fig.add_trace(

    go.Scatterpolar(

        r=peer_radar,

        theta=radar_labels,

        fill="toself",

        name="Peer Average",

        line=dict(width=3)

    )

)

fig.update_layout(

    title="Normalized Financial Comparison",

    polar=dict(

        radialaxis=dict(

            visible=True,

            range=[0,100]

        )

    ),

    height=650,

    showlegend=True

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# -----------------------------------
# QUALITY SCORE RANKING
# -----------------------------------

st.subheader("Quality Score Ranking")

ranking = comparison[

    [

        "company_name",

        "quality_score"

    ]

].copy()

ranking = ranking.sort_values(

    by="quality_score",

    ascending=False

)

fig = px.bar(

    ranking,

    x="quality_score",

    y="company_name",

    orientation="h",

    text="quality_score",

    title="Peer Ranking by Quality Score"

)

fig.update_layout(

    height=450,

    xaxis_title="Quality Score",

    yaxis_title=""

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

st.subheader("Peer Comparison Table")

table = comparison[

    [

        "company_name",

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

table.columns = [

    "Company",

    "Quality Score",

    "ROE (%)",

    "Debt / Equity",

    "Net Profit Margin",

    "Operating Margin",

    "Interest Coverage",

    "Asset Turnover",

    "Free Cash Flow"

]

# -----------------------------------
# SORT BY QUALITY SCORE
# -----------------------------------

table = table.sort_values(

    by="Quality Score",

    ascending=False

)

# -----------------------------------
# BENCHMARK HIGHLIGHT
# -----------------------------------

benchmark = comparison[

    comparison["is_benchmark"] == 1

]["company_name"].tolist()

def highlight_rows(row):

    if row["Company"] in benchmark:

        return [

            "background-color:#d4edda"

        ] * len(row)

    elif row["Company"] == selected_company:

        return [

            "background-color:#d1ecf1"

        ] * len(row)

    else:

        return [

            ""

        ] * len(row)

st.dataframe(

    table.style.apply(

        highlight_rows,

        axis=1

    ),

    hide_index=True,

    use_container_width=True

)

st.divider()

# -----------------------------------
# PEER SUMMARY
# -----------------------------------

left, right = st.columns(2)

with left:

    st.info(

        f"""

Peer Group

**{peer_group}**

Companies Compared

**{len(table)}**

"""
    )

with right:

    st.success(

        f"""

Selected Company

**{selected_company}**

Quality Score

**{round(company_data['quality_score'],2)}**

"""
    )

st.divider()
# -----------------------------------
# DOWNLOAD CSV
# -----------------------------------

st.subheader("Download Comparison")

csv = table.to_csv(
    index=False
)

st.download_button(

    label="Download Peer Comparison CSV",

    data=csv,

    file_name=f"{peer_group}_peer_comparison.csv",

    mime="text/csv"

)

st.divider()

# -----------------------------------
# TOP PERFORMER
# -----------------------------------

st.subheader("Top Performing Company")

if not table.empty:

    winner = table.iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Company",

        winner["Company"]

    )

    c2.metric(

        "Quality Score",

        round(

            winner["Quality Score"],

            2

        )

    )

    c3.metric(

        "ROE (%)",

        round(

            winner["ROE (%)"],

            2

        )

    )

else:

    st.warning(

        "No companies available."

    )

st.divider()

# -----------------------------------
# EMPTY DATA HANDLING
# -----------------------------------

if comparison.empty:

    st.warning(

        "No peer comparison data available for this Financial Year."

    )

# -----------------------------------
# FOOTER
# -----------------------------------

st.caption(

    "Nifty 100 Analytics Dashboard | Sprint 4 | Peer Comparison"

)

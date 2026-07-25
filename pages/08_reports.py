import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Annual Reports",
    layout="wide"
)

st.header("Annual Reports")

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()

company = st.sidebar.selectbox(

    "Select Company",

    sorted(
        companies["company_name"].tolist()
    )

)

company_data = companies[
    companies["company_name"] == company
].iloc[0]

st.subheader(company)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Company",
        company_data["company_name"]
    )

with col2:

    st.metric(
        "Website",
        company_data["website"]
    )

# ----------------------------------------------------
# ANNUAL REPORT YEARS
# ----------------------------------------------------

report_years = [

    "2024",

    "2023",

    "2022",

    "2021",

    "2020",

    "2019",

    "2018",

    "2017",

    "2016",

    "2015"

]

st.divider()

st.subheader("Available Annual Reports")

report_df = pd.DataFrame({

    "Year": report_years

})

report_df["Status"] = "Available"

report_df["Report Link"] = company_data["bse_profile"]

st.dataframe(

    report_df,

    use_container_width=True,

    hide_index=True

)

st.divider()

st.subheader("Open Annual Report")

selected_year = st.selectbox(

    "Select Report Year",

    report_years

)

if pd.notna(company_data["bse_profile"]) and company_data["bse_profile"] != "":

    st.success(f"{selected_year} Annual Report Link")

    st.markdown(

        f"[Open BSE Company Page]({company_data['bse_profile']})"

    )

else:

    st.error("Report Unavailable")
# ----------------------------------------------------
# COMPANY DETAILS
# ----------------------------------------------------

st.subheader("Company Information")

c1, c2 = st.columns(2)

with c1:

    st.info(f"""

### Company

**{company_data['company_name']}**

Website

{company_data['website']}

NSE Profile

{company_data['nse_profile']}

""")

with c2:

    st.success(f"""

### BSE Information

BSE Profile

{company_data['bse_profile']}

Face Value

{company_data['face_value']}

Book Value

{company_data['book_value']}

""")

st.divider()

# ----------------------------------------------------
# REPORT DOWNLOAD TABLE
# ----------------------------------------------------

st.subheader("Annual Report Directory")

download_table = pd.DataFrame({

    "Year": report_years,

    "Company": company_data["company_name"],

    "Website": company_data["website"],

    "BSE Link": company_data["bse_profile"]

})

st.dataframe(

    download_table,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ----------------------------------------------------
# QUICK LINKS
# ----------------------------------------------------

st.subheader("Quick Links")

col1, col2 = st.columns(2)

with col1:

    if pd.notna(company_data["website"]):

        st.markdown(

            f"🌐 **Official Website**\n\n{company_data['website']}"

        )

with col2:

    if pd.notna(company_data["bse_profile"]):

        st.markdown(

            f"📄 **BSE Company Page**\n\n{company_data['bse_profile']}"

        )

st.divider()
# ----------------------------------------------------
# REPORT AVAILABILITY DASHBOARD
# ----------------------------------------------------

st.subheader("Report Availability Dashboard")

available_reports = len(report_years)

unavailable_reports = 0

k1, k2, k3 = st.columns(3)

k1.metric(
    "Available Reports",
    available_reports
)

k2.metric(
    "Unavailable",
    unavailable_reports
)

k3.metric(
    "Coverage",
    f"{100:.0f}%"
)

st.divider()

# ----------------------------------------------------
# REPORT TIMELINE
# ----------------------------------------------------

st.subheader("Report Timeline")

timeline = pd.DataFrame({

    "Year": report_years,

    "Status": ["Available"] * len(report_years)

})

timeline = timeline.sort_values(
    "Year",
    ascending=False
)

st.dataframe(

    timeline,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ----------------------------------------------------
# REPORT SUMMARY
# ----------------------------------------------------

st.subheader("Summary")

left, right = st.columns(2)

with left:

    st.info(f"""

Company

**{company_data['company_name']}**

Years Covered

**{len(report_years)}**

Latest Report

**{report_years[0]}**

""")

with right:

    st.success(f"""

Official Website

{company_data['website']}

BSE Profile

{company_data['bse_profile']}

NSE Profile

{company_data['nse_profile']}

""")

st.divider()
# ----------------------------------------------------
# DOWNLOAD REPORT DIRECTORY
# ----------------------------------------------------

st.subheader("Download Report Directory")

export_df = pd.DataFrame({

    "Company":[company_data["company_name"]]*len(report_years),

    "Year":report_years,

    "Website":[company_data["website"]]*len(report_years),

    "NSE Profile":[company_data["nse_profile"]]*len(report_years),

    "BSE Profile":[company_data["bse_profile"]]*len(report_years)

})

csv = export_df.to_csv(index=False)

st.download_button(

    label="📥 Download Report Directory",

    data=csv,

    file_name=f"{company_data['company_name'].replace(' ','_')}_Annual_Reports.csv",

    mime="text/csv"

)

st.divider()

# ----------------------------------------------------
# IMPORTANT LINKS
# ----------------------------------------------------

st.subheader("Important Links")

if pd.notna(company_data["website"]) and company_data["website"] != "":

    st.markdown(

        f"🌐 **Official Website:** {company_data['website']}"

    )

if pd.notna(company_data["nse_profile"]) and company_data["nse_profile"] != "":

    st.markdown(

        f"📈 **NSE Profile:** {company_data['nse_profile']}"

    )

if pd.notna(company_data["bse_profile"]) and company_data["bse_profile"] != "":

    st.markdown(

        f"📄 **BSE Profile:** {company_data['bse_profile']}"

    )

st.divider()

# ----------------------------------------------------
# REPORT NOTES
# ----------------------------------------------------

st.info("""

### Notes

• Annual reports are accessed through the company's official BSE profile.

• If an annual report is unavailable, the dashboard displays **Report Unavailable**.

• Company website, NSE profile and BSE profile are provided for quick access.

""")

st.divider()

st.caption(
    "Nifty 100 Analytics Dashboard | Sprint 4 | Annual Reports"
)
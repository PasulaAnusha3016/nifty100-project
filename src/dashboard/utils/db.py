import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

DB_PATH = Path(__file__).parents[3] / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios(ticker=None, year=None):
    conn = get_connection()

    query = "SELECT * FROM financial_ratios"

    conditions = []

    if ticker:
        conditions.append(f"company_id='{ticker}'")

    if year:
        conditions.append(f"year='{year}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_pl(ticker=None):
    conn = get_connection()

    if ticker:
        query = f"SELECT * FROM profitandloss WHERE company_id='{ticker}'"
    else:
        query = "SELECT * FROM profitandloss"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(ticker=None):
    conn = get_connection()

    if ticker:
        query = f"SELECT * FROM balancesheet WHERE company_id='{ticker}'"
    else:
        query = "SELECT * FROM balancesheet"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cf(ticker=None):
    conn = get_connection()

    if ticker:
        query = f"SELECT * FROM cashflow WHERE company_id='{ticker}'"
    else:
        query = "SELECT * FROM cashflow"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()

    df = pd.read_sql("SELECT * FROM sectors", conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name=None):
    conn = get_connection()

    if group_name:
        query = f"SELECT * FROM peer_groups WHERE peer_group_name='{group_name}'"
    else:
        query = "SELECT * FROM peer_groups"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_valuation(ticker=None):
    conn = get_connection()

    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table'",
        conn
    )["name"].tolist()

    if "valuation" not in tables:
        conn.close()
        return pd.DataFrame()

    if ticker:
        query = f"SELECT * FROM valuation WHERE company_id='{ticker}'"
    else:
        query = "SELECT * FROM valuation"

    df = pd.read_sql(query, conn)

    conn.close()

    return df
import sys
import os

sys.path.append(os.path.abspath("."))

from src.etl.normaliser import normalize_year
from src.etl.normaliser import normalize_ticker


def test_normalize_year_string():
    assert normalize_year("2024") == 2024


def test_normalize_year_integer():
    assert normalize_year(2023) == 2023


def test_normalize_year_spaces():
    assert normalize_year(" 2022 ") == 2022


def test_normalize_ticker_lowercase():
    assert normalize_ticker("tcs") == "TCS"


def test_normalize_ticker_spaces():
    assert normalize_ticker(" infy ") == "INFY"
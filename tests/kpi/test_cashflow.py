from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


def test_free_cash_flow():
    assert free_cash_flow(500, -200) == 300


def test_cfo_quality():
    assert cfo_quality_score(200, 100) == "High Quality"


def test_cfo_quality_none():
    assert cfo_quality_score(100, 0) is None


def test_capex():
    assert capex_intensity(-100, 5000) == "Asset Light"


def test_fcf_conversion():
    assert fcf_conversion_rate(300, 600) == 50.0


def test_pattern():
    assert capital_allocation_pattern(100, -50, -20) == "Reinvestor"
from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage,
    icr_label,
    high_leverage_flag,
    net_debt,
    asset_turnover,
)


def test_net_profit_margin():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(200, 1000) == 20.0


def test_return_on_equity():
    assert return_on_equity(100, 200, 300) == 20.0


def test_return_on_equity_negative():
    assert return_on_equity(100, -200, 100) is None


def test_return_on_capital_employed():
    assert return_on_capital_employed(150, 200, 300, 500) == 15.0


def test_return_on_assets():
    assert return_on_assets(100, 1000) == 10.0


def test_return_on_assets_zero():
    assert return_on_assets(100, 0) is None


def test_debt_to_equity():
    assert debt_to_equity(100, 200, 300) == 0.2


def test_debt_free():
    assert debt_to_equity(0, 200, 300) == 0


def test_interest_coverage():
    assert interest_coverage(200, 50, 50) == 5.0


def test_interest_zero():
    assert interest_coverage(200, 50, 0) is None


def test_icr_label():
    assert icr_label(0) == "Debt Free"


def test_high_leverage():
    assert high_leverage_flag(6, "Technology") is True


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0
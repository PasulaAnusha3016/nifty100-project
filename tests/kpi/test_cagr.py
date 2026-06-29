from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)


def test_revenue_cagr():
    value, flag = revenue_cagr(100, 200, 5)
    assert flag == "NORMAL"


def test_pat_cagr():
    value, flag = pat_cagr(100, 300, 5)
    assert flag == "NORMAL"


def test_eps_cagr():
    value, flag = eps_cagr(10, 20, 5)
    assert flag == "NORMAL"


def test_turnaround():
    value, flag = revenue_cagr(-100, 200, 5)
    assert flag == "TURNAROUND"


def test_decline():
    value, flag = revenue_cagr(100, -200, 5)
    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():
    value, flag = revenue_cagr(-100, -50, 5)
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = revenue_cagr(0, 100, 5)
    assert flag == "ZERO_BASE"


def test_invalid_period():
    value, flag = revenue_cagr(100, 200, 0)
    assert flag == "INVALID_PERIOD"
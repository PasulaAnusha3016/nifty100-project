def free_cash_flow(operating_activity, investing_activity):
    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):
    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"
    elif ratio >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    if sales == 0:
        return None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        return "Asset Light"
    elif intensity <= 8:
        return "Moderate"
    else:
        return "Capital Intensive"


def fcf_conversion_rate(fcf, operating_profit):
    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


def capital_allocation_pattern(cfo, cfi, cff):
    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-",
    )

    patterns = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed",
    }

    return patterns.get(signs, "Unknown")
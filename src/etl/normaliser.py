def normalize_year(year):
    if year is None:
        return None

    return int(str(year).strip())


def normalize_ticker(ticker):
    if ticker is None:
        return None

    return str(ticker).strip().upper()
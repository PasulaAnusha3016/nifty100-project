from src.screener.engine import ScreenerEngine


class ScreenerPresets:

    def __init__(self):
        self.engine = ScreenerEngine()

    def quality_compounder(self):

        df = self.engine.df.copy()

        df = df[
            (df["return_on_equity_pct"] > 15) &
            (df["debt_to_equity"] < 1.0) &
            (df["free_cash_flow_cr"] > 0)
        ]

        return df

    def value_pick(self):

        df = self.engine.df.copy()

        if "price_to_earnings" not in df.columns:
            return df.head(0)

        df = df[
            (df["price_to_earnings"] < 20) &
            (df["debt_to_equity"] < 2)
        ]

        return df

    def growth_accelerator(self):

        df = self.engine.df.copy()

        if "pat_cagr_5yr" not in df.columns:
            return df.head(0)

        df = df[
            (df["pat_cagr_5yr"] > 20)
        ]

        return df

    def dividend_champion(self):

        df = self.engine.df.copy()

        df = df[
            (df["dividend_payout_ratio_pct"] < 80) &
            (df["free_cash_flow_cr"] > 0)
        ]

        return df

    def debt_free_bluechip(self):

        df = self.engine.df.copy()

        df = df[
            (df["debt_to_equity"] == 0) &
            (df["return_on_equity_pct"] > 12)
        ]

        return df

    def turnaround_watch(self):

        df = self.engine.df.copy()

        if "revenue_cagr_3yr" not in df.columns:
            return df.head(0)

        df = df[
            (df["revenue_cagr_3yr"] > 10)
        ]

        return df


if __name__ == "__main__":

    preset = ScreenerPresets()

    print("Quality Compounder")
    print(preset.quality_compounder().head())

    print()

    print("Value Pick")
    print(preset.value_pick().head())

    print()

    print("Growth Accelerator")
    print(preset.growth_accelerator().head())

    print()

    print("Dividend Champion")
    print(preset.dividend_champion().head())

    print()

    print("Debt Free Bluechip")
    print(preset.debt_free_bluechip().head())

    print()

    print("Turnaround Watch")
    print(preset.turnaround_watch().head())
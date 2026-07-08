import sqlite3
import yaml
import pandas as pd
import numpy as np


class ScreenerEngine:

    def __init__(self,
                 db_path="nifty100.db",
                 config_path="config/screener_config.yaml"):

        self.db_path = db_path
        self.config_path = config_path

        self.conn = sqlite3.connect(self.db_path)

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def add_composite_quality_score(self):

        score = np.zeros(len(self.df))

        if "return_on_equity_pct" in self.df.columns:
            score += self.df["return_on_equity_pct"].fillna(0)

        if "net_profit_margin_pct" in self.df.columns:
            score += self.df["net_profit_margin_pct"].fillna(0)

        if "asset_turnover" in self.df.columns:
            score += self.df["asset_turnover"].fillna(0) * 10

        if "interest_coverage" in self.df.columns:
            score += self.df["interest_coverage"].fillna(0)

        if "debt_to_equity" in self.df.columns:
            score -= self.df["debt_to_equity"].fillna(0) * 5

        self.df["composite_quality_score"] = score

    def apply_filter(self, column, operator, value):

        if column not in self.df.columns:
            return

        if operator == ">":
            self.df = self.df[self.df[column] > value]

        elif operator == ">=":
            self.df = self.df[self.df[column] >= value]

        elif operator == "<":
            self.df = self.df[self.df[column] < value]

        elif operator == "<=":
            self.df = self.df[self.df[column] <= value]

        elif operator == "==":
            self.df = self.df[self.df[column] == value]

    def run_filters(self):

        filters = self.config["filters"]

        for f in filters:

            self.apply_filter(
                f["column"],
                f["operator"],
                f["value"]
            )

        self.add_composite_quality_score()

        self.df = self.df.sort_values(
            by="composite_quality_score",
            ascending=False
        )

        return self.df

    def export_excel(self,
                     filename="output/screener_output.xlsx"):

        self.df.to_excel(
            filename,
            index=False
        )

        print("Exported:", filename)


if __name__ == "__main__":

    engine = ScreenerEngine()

    result = engine.run_filters()

    print(result.head())

    engine.export_excel()
import pandas as pd

from src.config import PRIVATE_DATA, PUBLIC_DATA


def build_analysis_dataset():
    market_path = PUBLIC_DATA / "market_data_monthly.csv"
    vessel_path = PRIVATE_DATA / "vessel_value_monthly.csv"

    market = pd.read_csv(market_path, parse_dates=["Date"])
    vessel = pd.read_csv(vessel_path, parse_dates=["date"])

    market = market.rename(columns={"Date": "date"})

    analysis = pd.merge(
        market,
        vessel,
        on="date",
        how="inner"
    )

    analysis = analysis.sort_values("date").reset_index(drop=True)

    return analysis


if __name__ == "__main__":
    analysis = build_analysis_dataset()

    print(analysis.head())
    print(analysis.tail())
    print(analysis.info())
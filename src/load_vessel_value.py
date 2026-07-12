import pandas as pd

from src.config import CLARKSONS_DATA



def load_vessel_value(start_date="2010-02-01"):
    file_path = CLARKSONS_DATA / "vessel_value.xlsx"

    vessel = pd.read_excel(file_path)

    vessel = vessel[["date", "ship_value"]].copy()

    vessel["date"] = pd.to_datetime(
        vessel["date"],
        format="%b-%y"
    ) + pd.offsets.MonthEnd(0)

    vessel = vessel.sort_values("date")

    vessel = vessel[vessel["date"] >= start_date]

    vessel["ship_return"] = vessel["ship_value"].pct_change()

    vessel = vessel.dropna()

    return vessel


if __name__ == "__main__":
    vessel = load_vessel_value()
    print(vessel.head())
    print(vessel.tail())
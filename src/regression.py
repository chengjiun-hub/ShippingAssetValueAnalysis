import pandas as pd
import statsmodels.api as sm

from src.config import PRIVATE_DATA


def build_regression_dataset() -> pd.DataFrame:
    analysis = pd.read_csv(
        PRIVATE_DATA / "analysis_dataset.csv",
        parse_dates=["date"],
    )

    regression = analysis.copy()

    regression["vix_level_lag2"] = (
        regression["vix_level"].shift(2)
    )

    regression["wti_return_lag3"] = (
        regression["wti_return"].shift(3)
    )

    regression = regression[
        [
            "date",
            "ship_return",
            "vix_level_lag2",
            "wti_return_lag3",
        ]
    ]

    regression = regression.dropna().reset_index(drop=True)

    return regression


def run_ols(
    data: pd.DataFrame,
    feature_columns: list[str],
    target_column: str = "ship_return",
):
    X = data[feature_columns].copy()
    X = sm.add_constant(X)

    y = data[target_column].copy()

    model = sm.OLS(y, X).fit()

    return model


if __name__ == "__main__":
    regression = build_regression_dataset()

    print("Regression dataset")
    print(regression.head())
    print()
    regression.info()

    print("\nModel 1: WTI Return Lag 3")
    model_wti = run_ols(
        data=regression,
        feature_columns=["wti_return_lag3"],
    )
    print(model_wti.summary())

    print("\nModel 2: VIX Level Lag 2")
    model_vix = run_ols(
        data=regression,
        feature_columns=["vix_level_lag2"],
    )
    print(model_vix.summary())

    print("\nModel 3: Combined Model")
    model_combined = run_ols(
        data=regression,
        feature_columns=[
            "wti_return_lag3",
            "vix_level_lag2",
        ],
    )
    print(model_combined.summary())
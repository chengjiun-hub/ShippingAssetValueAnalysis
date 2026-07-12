import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr

from src.config import PRIVATE_DATA


SIGNIFICANCE_LEVEL = 0.05


def calculate_lead_lag_correlation(
    data: pd.DataFrame,
    feature_column: str,
    target_column: str = "ship_return",
    max_lag: int = 12,
) -> pd.DataFrame:
    """
    Calculate Pearson correlation and p-value between a lagged feature
    and the current target variable.

    Lag interpretation
    ------------------
    lag = 0:
        Feature and target are measured in the same month.

    lag = 1:
        The feature leads the target by one month.

    lag = 3:
        The feature leads the target by three months.
    """
    required_columns = {feature_column, target_column}

    missing_columns = required_columns.difference(data.columns)

    if missing_columns:
        raise KeyError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if max_lag < 0:
        raise ValueError("max_lag must be zero or greater.")

    results = []

    for lag in range(max_lag + 1):
        test_data = pd.DataFrame(
            {
                "target": data[target_column],
                "feature": data[feature_column].shift(lag),
            }
        ).dropna()

        if len(test_data) < 3:
            raise ValueError(
                f"Not enough observations for lag {lag}."
            )

        correlation, p_value = pearsonr(
            test_data["target"],
            test_data["feature"],
        )

        results.append(
            {
                "feature": feature_column,
                "lag_months": lag,
                "correlation": correlation,
                "p_value": p_value,
                "observations": len(test_data),
            }
        )

    return pd.DataFrame(results)


def build_lead_lag_table(
    max_lag: int = 12,
) -> pd.DataFrame:
    """
    Build the lead-lag result table for all candidate market indicators.
    """
    analysis_path = PRIVATE_DATA / "analysis_dataset.csv"

    if not analysis_path.exists():
        raise FileNotFoundError(
            f"Analysis dataset not found: {analysis_path}"
        )

    analysis = pd.read_csv(
        analysis_path,
        parse_dates=["date"],
    )

    features = [
        "vix_level",
        "vix_return",
        "wti_return",
    ]

    result_tables = []

    for feature in features:
        feature_result = calculate_lead_lag_correlation(
            data=analysis,
            feature_column=feature,
            target_column="ship_return",
            max_lag=max_lag,
        )

        result_tables.append(feature_result)

    return pd.concat(
        result_tables,
        ignore_index=True,
    )


def get_feature_results(
    result_df: pd.DataFrame,
    feature_name: str,
) -> pd.DataFrame:
    """
    Filter the full result table for one feature.
    """
    feature_df = (
        result_df[result_df["feature"] == feature_name]
        .copy()
        .sort_values("lag_months")
        .reset_index(drop=True)
    )

    if feature_df.empty:
        raise ValueError(
            f"No lead-lag results found for '{feature_name}'."
        )

    return feature_df


def get_best_lag(
    result_df: pd.DataFrame,
    feature_name: str,
    significance_level: float = SIGNIFICANCE_LEVEL,
) -> tuple[pd.Series, bool]:
    """
    Identify the best lag for one feature.

    Selection rule
    --------------
    1. If one or more lags satisfy p < significance_level, select the
       statistically significant lag with the largest absolute correlation.
    2. Otherwise, select the lag with the largest absolute correlation and
       label it as not statistically significant.
    """
    feature_df = get_feature_results(
        result_df=result_df,
        feature_name=feature_name,
    )

    significant_df = feature_df[
        feature_df["p_value"] < significance_level
    ]

    if not significant_df.empty:
        best_index = significant_df["correlation"].abs().idxmax()
        best_result = significant_df.loc[best_index]

        return best_result, True

    best_index = feature_df["correlation"].abs().idxmax()
    best_result = feature_df.loc[best_index]

    return best_result, False


def format_feature_name(
    feature_name: str,
) -> str:
    """
    Convert internal column names into readable chart labels.
    """
    feature_labels = {
        "vix_level": "VIX Level",
        "vix_return": "VIX Return",
        "wti_return": "WTI Return",
    }

    return feature_labels.get(
        feature_name,
        feature_name.replace("_", " ").title(),
    )


def plot_lead_lag(
    result_df: pd.DataFrame,
    feature_name: str,
    significance_level: float = SIGNIFICANCE_LEVEL,
) -> None:
    """
    Plot the lead-lag correlation curve for one feature.
    """
    feature_df = get_feature_results(
        result_df=result_df,
        feature_name=feature_name,
    )

    best, is_significant = get_best_lag(
        result_df=result_df,
        feature_name=feature_name,
        significance_level=significance_level,
    )

    display_name = format_feature_name(feature_name)

    if is_significant:
        point_label = "Statistically Significant Best Lag"
        point_marker = "*"
        point_size = 240
    else:
        point_label = "Strongest Lag (Not Significant)"
        point_marker = "D"
        point_size = 100

    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.plot(
        feature_df["lag_months"],
        feature_df["correlation"],
        marker="o",
        linewidth=2,
        label="Pearson Correlation",
    )

    ax.scatter(
        best["lag_months"],
        best["correlation"],
        marker=point_marker,
        s=point_size,
        zorder=5,
        label=point_label,
    )

    ax.axhline(
        y=0,
        linestyle="--",
        linewidth=1,
    )

    ax.axvline(
        x=best["lag_months"],
        linestyle=":",
        linewidth=1,
        alpha=0.5,
    )

    annotation_text = (
        f"Lag {int(best['lag_months'])}\n"
        f"r = {best['correlation']:.3f}\n"
        f"p = {best['p_value']:.3f}"
    )

    # Use fixed annotation positions so labels remain inside the chart.
    if feature_name == "vix_level":
        annotation_position = (
            best["lag_months"] + 0.9,
            best["correlation"] + 0.055,
        )
    elif feature_name == "wti_return":
        annotation_position = (
            best["lag_months"] + 0.8,
            best["correlation"] - 0.075,
        )
    else:
        annotation_position = (
            best["lag_months"] + 0.8,
            best["correlation"] + 0.045,
        )

    ax.annotate(
        annotation_text,
        xy=(
            best["lag_months"],
            best["correlation"],
        ),
        xytext=annotation_position,
        arrowprops={
            "arrowstyle": "->",
            "linewidth": 1,
        },
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": "white",
            "edgecolor": "gray",
            "alpha": 0.95,
        },
        fontsize=10,
    )

    ax.set_title(
        f"Lead-Lag Correlation Between "
        f"{display_name} and Ship Return"
    )
    ax.set_xlabel("Feature Lead (Months)")
    ax.set_ylabel("Pearson Correlation")
    ax.set_xticks(
        range(int(feature_df["lag_months"].max()) + 1)
    )
    ax.set_ylim(-0.20, 0.20)
    ax.grid(alpha=0.3)
    ax.legend(loc="best")

    fig.tight_layout()
    plt.show()


def plot_combined_lead_lag(
    result_df: pd.DataFrame,
    feature_names: list[str],
    significance_level: float = SIGNIFICANCE_LEVEL,
) -> None:
    """
    Plot lead-lag correlations for multiple market indicators together.
    """
    fig, ax = plt.subplots(figsize=(11, 6.5))

    best_results = {}

    for feature_name in feature_names:
        feature_df = get_feature_results(
            result_df=result_df,
            feature_name=feature_name,
        )

        display_name = format_feature_name(feature_name)

        line = ax.plot(
            feature_df["lag_months"],
            feature_df["correlation"],
            marker="o",
            linewidth=2,
            label=display_name,
        )[0]

        best, is_significant = get_best_lag(
            result_df=result_df,
            feature_name=feature_name,
            significance_level=significance_level,
        )

        marker = "*" if is_significant else "D"
        marker_size = 240 if is_significant else 100

        ax.scatter(
            best["lag_months"],
            best["correlation"],
            marker=marker,
            s=marker_size,
            color=line.get_color(),
            edgecolor="black",
            linewidth=0.6,
            zorder=5,
        )

        best_results[feature_name] = {
            "result": best,
            "significant": is_significant,
            "color": line.get_color(),
        }

    ax.axhline(
        y=0,
        linestyle="--",
        linewidth=1,
    )

    # Add vertical reference lines at the selected lags.
    for feature_name, details in best_results.items():
        best = details["result"]

        ax.axvline(
            x=best["lag_months"],
            linestyle=":",
            linewidth=1,
            alpha=0.35,
            color=details["color"],
        )

    # Fixed label placement prevents overlap with the title and each other.
    if "vix_level" in best_results:
        vix_best = best_results["vix_level"]["result"]

        ax.annotate(
            (
                "VIX Level\n"
                f"Lag {int(vix_best['lag_months'])}, "
                f"r = {vix_best['correlation']:.3f}\n"
                f"p = {vix_best['p_value']:.3f} "
                "(not significant)"
            ),
            xy=(
                vix_best["lag_months"],
                vix_best["correlation"],
            ),
            xytext=(
                vix_best["lag_months"] + 0.8,
                vix_best["correlation"] + 0.055,
            ),
            arrowprops={
                "arrowstyle": "->",
                "linewidth": 1,
            },
            bbox={
                "boxstyle": "round,pad=0.4",
                "facecolor": "white",
                "edgecolor": "gray",
                "alpha": 0.95,
            },
            fontsize=10,
        )

    if "wti_return" in best_results:
        wti_best = best_results["wti_return"]["result"]

        ax.annotate(
            (
                "WTI Return\n"
                f"Lag {int(wti_best['lag_months'])}, "
                f"r = {wti_best['correlation']:.3f}\n"
                f"p = {wti_best['p_value']:.3f}*"
            ),
            xy=(
                wti_best["lag_months"],
                wti_best["correlation"],
            ),
            xytext=(
                wti_best["lag_months"] + 0.9,
                wti_best["correlation"] - 0.080,
            ),
            arrowprops={
                "arrowstyle": "->",
                "linewidth": 1,
            },
            bbox={
                "boxstyle": "round,pad=0.4",
                "facecolor": "white",
                "edgecolor": "gray",
                "alpha": 0.95,
            },
            fontsize=10,
        )

    max_lag = int(result_df["lag_months"].max())

    ax.set_title(
        "Lead-Lag Correlation Analysis\n"
        "Between Market Indicators and Ship Return"
    )
    ax.set_xlabel("Feature Lead (Months)")
    ax.set_ylabel("Pearson Correlation")
    ax.set_xticks(range(max_lag + 1))
    ax.set_ylim(-0.20, 0.20)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right")

    ax.text(
        0.01,
        0.02,
        "* p < 0.05",
        transform=ax.transAxes,
        fontsize=9,
    )

    fig.tight_layout()
    plt.show()


def print_best_lag_summary(
    result_df: pd.DataFrame,
    feature_names: list[str],
    significance_level: float = SIGNIFICANCE_LEVEL,
) -> None:
    """
    Print a concise summary of the selected lead-lag results.
    """
    print("\nBest-lag summary")

    for feature_name in feature_names:
        best, is_significant = get_best_lag(
            result_df=result_df,
            feature_name=feature_name,
            significance_level=significance_level,
        )

        status = (
            "statistically significant"
            if is_significant
            else "not statistically significant"
        )

        display_name = format_feature_name(feature_name)

        print(
            f"{display_name}: "
            f"lag={int(best['lag_months'])}, "
            f"r={best['correlation']:.3f}, "
            f"p={best['p_value']:.3f}, "
            f"n={int(best['observations'])}, "
            f"{status}"
        )


if __name__ == "__main__":
    lead_lag_results = build_lead_lag_table(
        max_lag=12
    )

    print(lead_lag_results.to_string(index=False))

    print_best_lag_summary(
        result_df=lead_lag_results,
        feature_names=[
            "vix_level",
            "vix_return",
            "wti_return",
        ],
    )

    plot_lead_lag(
        result_df=lead_lag_results,
        feature_name="vix_level",
    )

    plot_lead_lag(
        result_df=lead_lag_results,
        feature_name="wti_return",
    )

    plot_combined_lead_lag(
        result_df=lead_lag_results,
        feature_names=[
            "vix_level",
            "wti_return",
        ],
    )
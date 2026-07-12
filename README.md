# Shipping Asset Value Early Warning Analysis

## Overview

Every ship-finance loan starts with two questions.

- Can the borrower generate enough cash flow to repay the loan?
- If not, how much protection does the vessel itself provide?

Vessel value plays an equally important role in ship-finance lending. Since vessel-backed loans are typically granted at around a 55% loan-to-value (LTV) ratio, changes in vessel prices directly affect collateral coverage and credit risk.

Unlike financial markets, vessel values usually adjust more slowly. That raised a practical question during my work:

**Can publicly available market data provide an earlier signal before vessel values begin to move?**

To explore this, I combined proprietary vessel-value data from Clarksons Shipping Intelligence Network with public market data from Yahoo Finance. I then examined their relationships through exploratory analysis, lead-lag correlation analysis, and regression models.

The goal isn't to predict vessel prices directly. Instead, it's to identify market indicators that could provide earlier signals for collateral monitoring and support lending decisions.

## Key Findings

WTI shows the strongest leading relationship among all variables tested — monthly WTI returns lead vessel returns by approximately three months (correlation 0.156, p-value 0.032). This relationship remains statistically significant after controlling for VIX in the regression model.

VIX contains more limited predictive information. Higher market volatility is associated with weaker future vessel returns, but the relationship is relatively weak — VIX level reaches its strongest relationship at a two-month lead, but it's not statistically significant in the final regression model.

Overall, public market data can supplement collateral monitoring, but not replace it. The regression model explains only a small portion of monthly vessel-return variation (R² = 3.8%), so public market indicators should be treated as an additional monitoring signal rather than a substitute for formal vessel valuation.

## Why This Matters

In ship finance, lenders usually project a borrower's future cash flow over the life of the loan while also monitoring the value of the pledged vessel. Since collateral values directly affect LTV ratios, an earlier indication of declining vessel prices gives lenders more time to react — whether that's reviewing collateral coverage, updating internal vessel-value assumptions, running borrower stress tests, increasing monitoring frequency, or reassessing portfolio risk.

This project explores whether market information that's available every day can provide useful signals before vessel values adjust.

## Data

Two data sources are used throughout the project.

**Proprietary Data**
- Source: Clarksons Shipping Intelligence Network
- Dataset: Kamsarmax / Panamax 5-Year-Old Secondhand Prices
- Frequency: Monthly
- Period: March 2010 – March 2026
- Note: the original Clarksons dataset is proprietary and is therefore not included in this repository.

**Public Market Data**
- Source: Yahoo Finance
- Variables: VIX Index (`^VIX`), WTI Crude Oil Futures (`CL=F`)
- Daily observations are converted into month-end monthly data before analysis.

# Methodology

The workflow is fairly linear — each step feeds into the next:

```
Clarksons Vessel Values
            +
Yahoo Finance Market Data
            │
            ▼
     Data Preparation
            │
            ▼
 Monthly Analysis Dataset
            │
            ▼
Exploratory Data Analysis
            │
            ▼
 Lead-Lag Analysis
            │
            ▼
 Multiple Regression
            │
            ▼
Regression Diagnostics
            │
            ▼
Business Interpretation
```

Each stage serves a different purpose. Exploratory analysis comes first, mainly to get a feel for how vessel values and market variables have behaved over time and whether any relationships stand out. From there, lead-lag analysis checks whether a market indicator consistently moves ahead of vessel prices — not just correlated, but leading. Regression is the last step, used to test whether those leading relationships still hold once other variables are controlled for.

---

# Repository Structure

```
ShippingAssetValueAnalysis/
│
├── data/
├── notebooks/
├── reports/
├── src/
├── README.md
├── requirements.txt
└── pyproject.toml
```

- **data/** — raw and processed datasets
- **notebooks/** — the full analysis workflow, from data prep through regression
- **src/** — reusable Python scripts
- **reports/** — final project report

Structured so each stage of the analysis can be reproduced on its own.

---

# Notebook Guide

| Notebook | Purpose |
|----------|---------|
| 01_public_market_data.ipynb | Download and prepare market data |
| 02_vessel_value_pipeline.ipynb | Clean and prepare vessel-value data |
| 03_unified_dataset.ipynb | Merge all datasets into a monthly analysis table |
| 04_exploratory_data_analysis.ipynb | Explore trends, distributions, and correlations |
| 05_lead_lag_analysis.ipynb | Identify potential leading indicators |
| 06_regression_analysis.ipynb | Evaluate statistical relationships and model assumptions |

---

# Running the Project

Clone the repo:

```bash
git clone https://github.com/chengjiun-hub/ShippingAssetValueAnalysis.git
cd ShippingAssetValueAnalysis
```

Set up a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt

pip install -e .
```

The vessel-value dataset is proprietary, so you'll need to supply your own Clarksons source file under:

```
data/raw/clarksons/
```

Then run the notebooks in order:

1. Public market data
2. Vessel-value processing
3. Dataset construction
4. Exploratory analysis
5. Lead-lag analysis
6. Regression analysis

Once the required datasets exist, each notebook can also be run on its own.

# Limitations

This is an exploratory study, not a forecasting system, and it comes with a few real limitations.

For one, the analysis only looks at a single vessel benchmark (Kamsarmax/Panamax 5-year-old secondhand prices), so the results may not carry over to other vessel classes or age segments. It also only considers two market indicators — VIX and WTI — when vessel values are actually driven by a lot more than that, including freight rates, fleet supply, interest rates, and global trade activity. And the regression itself only explains a small slice of monthly vessel-return variation, which is a reminder that these public indicators are just one piece of a much bigger picture, not the whole story.

---

# Future Work

A few directions seem worth pursuing if this gets extended further.

The most obvious one is adding shipping-specific variables like freight rates or the Baltic Dry Index — these are probably more directly tied to vessel prices than broad financial-market indicators. It'd also be worth comparing across different vessel classes instead of relying on a single benchmark, just to see whether the relationship found here actually holds up elsewhere in the shipping market. On the modeling side, rolling-window regression or time-series models could help test whether these relationships stay stable over time rather than being a one-off pattern.

For now, the focus has been on understanding the relationship itself. Turning that into something with real predictive accuracy would be the next stage, not what this study set out to do.

---

# Full Report

A more detailed writeup of the methodology, statistical analysis, and business interpretation is here:

```
reports/final_report.md
```

---

# Acknowledgements

Public market data comes from Yahoo Finance. Vessel-value data comes from Clarksons Shipping Intelligence Network — the original Clarksons dataset is proprietary and isn't included in this repo.

---

# Disclaimer

This repository was built for educational and research purposes,
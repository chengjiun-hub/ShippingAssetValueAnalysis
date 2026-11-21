# Vessel Value Early Warning Analysis

## Executive Summary

This project explores whether VIX and WTI precede movements in vessel values using monthly data from March 2010 to March 2026.

The strongest observed WTI correlation occurs at a three-month lead (r = 0.156, unadjusted p = 0.032), but this is a weak association selected from 13 possible lags. A Bonferroni correction gives p ≈ 0.412. The combined OLS regression explains 3.8% of vessel-return variation. The findings are exploratory and do not establish a reliable early-warning indicator.

---

## 1. Business Motivation

Vessel values are a core part of collateral assessment in ship finance. A significant decline can push loan-to-value ratios up, weaken collateral coverage, raise covenant concerns, and increase expected loss on default — all of which usually mean closer monitoring or a call for additional collateral.

The problem is that formal vessel valuations tend to update more slowly than publicly traded financial and commodity markets do. This project checks whether VIX and WTI carry information that shows up before vessel values actually move.

---

## 2. Research Question

The core question: **do VIX and WTI provide useful early warning signals for future vessel-value movements?**

That breaks down into three parts — whether these indicators relate to vessel returns in the same month, whether lagged versions of them relate more strongly to future vessel returns, and whether any lagged relationship found still holds up in a multivariate regression rather than falling apart once other variables are controlled for.

---

## 3. Data

**Vessel-value data** comes from Clarksons Shipping Intelligence Network — the Kamsarmax/Panamax 5-year-old secondhand price series, monthly, in USD million, covering March 2010 to March 2026. This raw dataset is proprietary and isn't included in the public repo.

**Public market data** comes from Yahoo Finance: the VIX index (`^VIX`) and WTI crude oil futures (`CL=F`), both daily and converted to month-end values.

The final analysis dataset combines `ship_value`, `ship_return`, `vix_level`, `vix_return`, `wti_price`, and `wti_return`, with monthly returns calculated as percentage changes from the prior month.

---

## 4. Methodology

The project moves through eight stages: building the public market data pipeline, building the vessel-value pipeline, merging them into one monthly dataset, exploratory analysis, lead-lag correlation, regression, regression diagnostics, and finally business interpretation.

Monthly vessel return is the dependent variable throughout. The two candidates that came out of lead-lag analysis are WTI return lagged three months and VIX level lagged two months.

---

## 5. Exploratory Data Analysis

Vessel values move in pronounced cycles — a substantial decline between 2010 and 2016, followed by recovery in later years. The 12-month moving average confirms these are sustained cycles rather than short-term noise, which is exactly the kind of swing that makes collateral-value monitoring matter for lenders.

VIX stays fairly calm during normal periods but spikes sharply during stress events, most notably in 2020 — behaving more like an event-driven risk gauge than a persistent trend variable. WTI, by contrast, moves through longer commodity cycles, with clear structural shifts during the 2014–2016 oil-price decline, the 2020 pandemic shock, and the 2022 energy-price surge. These moves likely reflect broader shifts in economic activity, commodity demand, and shipping costs.

Monthly vessel returns cluster around zero — mean of roughly 0.1%, standard deviation around 4.6%, ranging from about -11.8% to +23.5% — with positive skew and heavy tails. In other words, calm in a typical month but capable of sharp, infrequent shocks.

Contemporaneous return correlations are weak: ship return versus VIX return sits around -0.01, and ship return versus WTI return around 0.08. Ship value and WTI price do show a moderate level correlation of about 0.46, but that gap between level and return correlations is a reminder not to mistake shared long-term trends for short-term predictive power.

---

## 6. Lead-Lag Analysis

Correlations were calculated at leads of 0–12 months for VIX level, VIX return, and WTI return, giving 39 comparisons. Reported p-values are unadjusted and lag selection was data-driven.

- WTI return: lag 3, r = 0.156, raw p = 0.032 (n = 190); Bonferroni-adjusted p ≈ 0.412 across its 13 lags.
- VIX level: lag 2, r = -0.128, raw p = 0.078.
- VIX return: lag 7, r = -0.093, raw p = 0.207.

These are exploratory associations, not validated predictions.

---

## 7. Regression Analysis

Three OLS models were estimated: WTI alone, VIX alone, and both together.

The **WTI-only model** finds WTI return (lag 3) significant, with a coefficient of 0.0624 (p = 0.032) and R² of 2.4% (adjusted 1.9%) — consistent with the lead-lag result.

The **VIX-only model** finds VIX level (lag 2) only marginally significant, coefficient roughly -0.0009 (p = 0.080), R² of 1.6% (adjusted 1.1%). The negative sign is directionally consistent with the idea that elevated fear precedes weaker vessel returns, but the statistical support is thin.

In the **combined model**, WTI return (lag 3) has coefficient 0.0589 (unadjusted p = 0.042) — while VIX level (lag 2) does not (coefficient roughly -0.0008, p = 0.108). The nominal model F-test p-value is 0.027, with R² of 3.8% (adjusted 2.7%). These p-values do not account for lag selection on the same sample or residual autocorrelation.

---

## 8. Regression Diagnostics

The residual-versus-fitted plot shows no obvious nonlinear pattern, so the linearity assumption looks reasonable. Residuals deviate somewhat from normality and show heavy tails, which is typical for financial return data and lines up with what the return distribution already showed.

The Breusch-Pagan test (LM p ≈ 0.667, F p ≈ 0.671) doesn't reject constant variance, so there's no evidence of heteroskedasticity. VIF values for both predictors sit around 1.006, meaning multicollinearity is negligible.

The Durbin-Watson statistic comes out around 1.40, pointing to mild positive autocorrelation in the residuals — worth flagging for future work, which could use Newey-West standard errors or a proper time-series model instead of plain OLS.

---

## 9. Key Findings

WTI has a weak positive association with vessel returns at the selected three-month lag (r = 0.156), but the raw p-value does not survive a conservative adjustment for the lag search. The combined regression gives WTI a coefficient of 0.059 (raw p = 0.042), with R² = 3.8%. The regression uses the same sample as the lag selection and has positive residual autocorrelation (Durbin–Watson ≈ 1.40), so these nominal p-values are not confirmatory evidence.

---

## 10. Business Interpretation

WTI changes appear to precede vessel-value movements by roughly three months, which makes it a reasonable candidate to fold into a broader collateral-monitoring framework — alongside vessel-market price indices, freight rates, charter-market data, borrower financials, LTV ratios, vessel age and condition, and macro/geopolitical indicators.

WTI shouldn't drive credit decisions on its own. A sharper reading is to treat a sharp WTI move as a trigger — for a more frequent vessel-value review, an updated LTV calculation, a borrower stress test, or a closer look at covenant headroom and sector conditions.

---

## 11. Limitations

This is a single-benchmark study — the Kamsarmax/Panamax 5-year-old secondhand series — so results may not carry over to other vessel types, ages, newbuilding or demolition prices, or individual vessel valuations.

The predictor set is also narrow: just VIX and WTI, leaving out freight rates, Baltic Dry Index components, orderbook and fleet-growth data, interest rates, steel prices, trade volumes, and scrapping activity — all of which plausibly matter more directly.

Explanatory power is modest (R² ≈ 3.8%), and the lag search and residual autocorrelation warrant caution in interpreting p-values. Residuals are non-normal with mild autocorrelation, which future work could address with Newey-West errors, autoregressive models, rolling-window regression, out-of-sample testing, or nonlinear approaches.

Finally, none of this establishes causality — WTI is more likely a proxy for broader global economic and commodity-market conditions than a direct driver of vessel prices.

---

## 12. Conclusion

The data suggest a weak association between WTI returns and vessel returns three months later, but the lead time was selected after testing multiple alternatives. Low explanatory power, residual autocorrelation, and the absence of out-of-sample validation prevent treating this as a dependable early-warning signal.

---

## Disclaimer

The Clarksons dataset used in this project is proprietary and isn't included in the public repository. This analysis is for educational and research purposes only and doesn't constitute investment, lending, or valuation advice.
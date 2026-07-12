# Vessel Value Early Warning Analysis

## Executive Summary

This project asks whether market fear (VIX) and oil-price movements (WTI returns) can serve as early warning signals for future vessel-value changes.

The analysis covers monthly data from March 2010 to March 2026, using the Clarksons Kamsarmax/Panamax 5-year-old secondhand price series as the vessel-value benchmark, alongside public VIX and WTI data from Yahoo Finance.

Same-month relationships between these market indicators and vessel returns are generally weak. But WTI returns lagged by three months show a statistically significant positive relationship with vessel returns, and that relationship holds up even after controlling for VIX level. The model's overall explanatory power is modest, so WTI is best treated as a supplementary early warning signal rather than a standalone forecasting tool.

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

Correlations are calculated across lags of zero to twelve months, where a lag of three means the indicator is observed three months before the corresponding vessel return.

**WTI return** reaches its strongest relationship at a three-month lead: correlation 0.156, p = 0.032 — statistically significant, and early evidence that oil-price moves might carry information about vessel values roughly a quarter ahead.

**VIX level**'s strongest (negative) relationship comes at a two-month lead: correlation -0.128, p = 0.078. That's not significant at the 5% level, only marginal at 10%, so it's carried forward as a candidate control variable rather than treated as confirmed.

**VIX return** doesn't show a significant relationship at any tested lag and is dropped from the regression.

---

## 7. Regression Analysis

Three OLS models were estimated: WTI alone, VIX alone, and both together.

The **WTI-only model** finds WTI return (lag 3) significant, with a coefficient of 0.0624 (p = 0.032) and R² of 2.4% (adjusted 1.9%) — consistent with the lead-lag result.

The **VIX-only model** finds VIX level (lag 2) only marginally significant, coefficient roughly -0.0009 (p = 0.080), R² of 1.6% (adjusted 1.1%). The negative sign is directionally consistent with the idea that elevated fear precedes weaker vessel returns, but the statistical support is thin.

In the **combined model**, WTI return (lag 3) stays significant — coefficient 0.0589, p = 0.042 — while VIX level (lag 2) does not (coefficient roughly -0.0008, p = 0.108). The model overall is significant (F-test p = 0.027), with R² of 3.8% (adjusted 2.7%). WTI holding up after VIX is added suggests it's contributing information beyond what VIX alone captures.

---

## 8. Regression Diagnostics

The residual-versus-fitted plot shows no obvious nonlinear pattern, so the linearity assumption looks reasonable. Residuals deviate somewhat from normality and show heavy tails, which is typical for financial return data and lines up with what the return distribution already showed.

The Breusch-Pagan test (LM p ≈ 0.667, F p ≈ 0.671) doesn't reject constant variance, so there's no evidence of heteroskedasticity. VIF values for both predictors sit around 1.006, meaning multicollinearity is negligible.

The Durbin-Watson statistic comes out around 1.40, pointing to mild positive autocorrelation in the residuals — worth flagging for future work, which could use Newey-West standard errors or a proper time-series model instead of plain OLS.

---

## 9. Key Findings

Vessel values move through substantial long-term cycles, which is itself a meaningful source of collateral risk for lenders. Same-month relationships between VIX, WTI, and vessel returns are weak, but WTI lagged three months shows a statistically significant positive relationship with vessel returns (r = 0.156, p = 0.032), and that relationship survives controlling for VIX (β = 0.059, p = 0.042).

VIX level lagged two months only offers marginal evidence on its own and doesn't hold up in the combined model. Overall the model's explanatory power stays modest (R² = 3.8%), which is why WTI reads as a supplementary monitoring signal rather than something to forecast off of directly.

---

## 10. Business Interpretation

WTI changes appear to precede vessel-value movements by roughly three months, which makes it a reasonable candidate to fold into a broader collateral-monitoring framework — alongside vessel-market price indices, freight rates, charter-market data, borrower financials, LTV ratios, vessel age and condition, and macro/geopolitical indicators.

WTI shouldn't drive credit decisions on its own. A sharper reading is to treat a sharp WTI move as a trigger — for a more frequent vessel-value review, an updated LTV calculation, a borrower stress test, or a closer look at covenant headroom and sector conditions.

---

## 11. Limitations

This is a single-benchmark study — the Kamsarmax/Panamax 5-year-old secondhand series — so results may not carry over to other vessel types, ages, newbuilding or demolition prices, or individual vessel valuations.

The predictor set is also narrow: just VIX and WTI, leaving out freight rates, Baltic Dry Index components, orderbook and fleet-growth data, interest rates, steel prices, trade volumes, and scrapping activity — all of which plausibly matter more directly.

Explanatory power is modest (R² ≈ 3.8%), enough to support a monitoring relationship but not a high-accuracy forecast. Residuals are non-normal with mild autocorrelation, which future work could address with Newey-West errors, autoregressive models, rolling-window regression, out-of-sample testing, or nonlinear approaches.

Finally, none of this establishes causality — WTI is more likely a proxy for broader global economic and commodity-market conditions than a direct driver of vessel prices.

---

## 12. Conclusion

This project set out to test whether VIX and WTI can provide early warning signals for vessel-value movements. Same-month relationships turn out to be weak, but WTI returns lagged three months show a statistically significant positive relationship with vessel returns that survives controlling for VIX — even if the model's overall explanatory power remains modest.

That's enough to support using lagged WTI returns as a supplementary early warning input within a broader ship-finance monitoring framework — not as a standalone forecasting model or a credit-decision rule on its own.

---

## Disclaimer

The Clarksons dataset used in this project is proprietary and isn't included in the public repository. This analysis is for educational and research purposes only and doesn't constitute investment, lending, or valuation advice.
import pandas as pd
import yfinance as yf


def download_yahoo_data(ticker, start_date="2010-02-01"):
    data = yf.download(ticker, start=start_date, auto_adjust=False)

    if data.empty:
        raise ValueError(f"No data downloaded for {ticker}")

    data = data[["Close"]].copy()
    data.columns = [ticker]

    return data


def convert_to_monthly(data):
    monthly_data = data.resample("ME").last()
    return monthly_data


def build_public_market_data(start_date="2010-02-01"):
    vix = download_yahoo_data("^VIX", start_date)
    wti = download_yahoo_data("CL=F", start_date)

    vix_monthly = convert_to_monthly(vix)
    wti_monthly = convert_to_monthly(wti)

    market_data = pd.concat([vix_monthly, wti_monthly], axis=1)
    market_data.columns = ["vix_level", "wti_price"]

    market_data["vix_return"] = market_data["vix_level"].pct_change()
    market_data["wti_return"] = market_data["wti_price"].pct_change()

    market_data = market_data.dropna()

    return market_data


if __name__ == "__main__":
    market_data = build_public_market_data()
    market_data.to_csv("data/processed/public/market_data_monthly.csv")
    print(market_data.head())
    print("Saved to data/processed/public/market_data_monthly.csv")
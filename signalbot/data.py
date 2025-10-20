import pandas as pd
import yfinance as yf


def get_btc_ohlc(interval: str = "4h", lookback_days: int = 365) -> pd.DataFrame:
    """
    Fetch BTC-USD OHLC data from Yahoo Finance.

    interval options (yfinance): 1m, 2m, 5m, 15m, 30m, 60m/1h, 90m, 1d, 5d, 1wk, 1mo, 3mo
    For our use: "1h", "4h", "1d" are typical.
    """
    # Map our intervals to yfinance period windows that give enough history.
    # (yfinance requires a 'period' argument compatible with the interval)
    period_map = {
        "1h":  "730d",
        "4h":  "730d",
        "1d":  f"{lookback_days}d",
    }
    yf_period = period_map.get(interval, f"{lookback_days}d")

    ticker = yf.Ticker("BTC-USD")
    df = ticker.history(period=yf_period, interval=interval)

    # Normalize column names, keep only what we use
    df = df.rename(columns=str.lower)
    df = df[["open", "high", "low", "close", "volume"]]
    df = df.dropna()
    return df


import pandas as pd

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Wilder's RSI. Input: price series (close). Returns RSI series.
    """
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Wilder's smoothing (RMA)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / (avg_loss.replace(0, 1e-10))
    rsi = 100 - (100 / (1 + rs))
    return rsi

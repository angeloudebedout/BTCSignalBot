import pandas as pd
from .indicators import rsi

def rsi_signal(
    df: pd.DataFrame,
    period: int = 14,
    oversold: int = 30,
    overbought: int = 70,
) -> pd.DataFrame:
    """
    Compute RSI and generate BUY/SELL/HOLD on the last candle.
    Also prints a small alert to terminal.
    """
    out = df.copy()
    out["rsi"] = rsi(out["close"], period=period)
    out["signal"] = "HOLD"

    if len(out) >= 2:
        prev, curr = out.iloc[-2], out.iloc[-1]
        if (prev["rsi"] < oversold) and (curr["rsi"] >= oversold):
            out.iloc[-1, out.columns.get_loc("signal")] = "BUY"
            print(f"\n🟢 BUY — ${curr['close']:.2f} | RSI {curr['rsi']:.2f} @ {curr.name}\n")
        elif (prev["rsi"] > overbought) and (curr["rsi"] <= overbought):
            out.iloc[-1, out.columns.get_loc("signal")] = "SELL"
            print(f"\n🔴 SELL — ${curr['close']:.2f} | RSI {curr['rsi']:.2f} @ {curr.name}\n")
        else:
            print(f"⚪ HOLD — ${curr['close']:.2f} | RSI {curr['rsi']:.2f}")
    return out






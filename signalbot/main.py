# signalbot/main.py
import argparse
from .data import get_btc_ohlc
from .strategy import rsi_signal
from .plotting import plot_price_rsi


def run(
    interval: str = "4h",
    period: int = 14,
    oversold: int = 30,
    overbought: int = 70,
    plot: bool = False,
    save: str | None = None,
):
    df = get_btc_ohlc(interval=interval)
    df = rsi_signal(df, period=period, oversold=oversold, overbought=overbought)
    last = df.iloc[-1]

    print(f"\n🕒 Interval: {interval}")
    print(f"🗓️  Time: {last.name}")
    print(f"💲 Close: {last['close']:.2f}")
    print(f"📈 RSI({period}): {last['rsi']:.2f}")
    print(f"📣 Signal: {last['signal']}\n")

    if plot or save:
        plot_price_rsi(df, interval=interval, save_path=(save or None))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="BTCSignalBot — RSI Trading Signal Generator")
    p.add_argument("--interval",  default="4h", help="1m,5m,15m,30m,1h,4h,1d")
    p.add_argument("--period",    type=int, default=14)
    p.add_argument("--oversold",  type=int, default=30)
    p.add_argument("--overbought", type=int, default=70)
    p.add_argument("--plot",      action="store_true", help="Show charts in a window")
    p.add_argument("--save",      default="", help="Save chart PNG to this path")
    args = p.parse_args()

    run(args.interval, args.period, args.oversold, args.overbought, args.plot, (args.save or None))


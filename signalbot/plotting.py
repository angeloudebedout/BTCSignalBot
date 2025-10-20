import os
import matplotlib.pyplot as plt

def plot_price_rsi(df, interval: str, save_path: str | None = None):
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), layout="constrained")

    # Price
    ax1.set_title(f"BTC-USD Close ({interval})", fontsize=14, weight="bold", color="#222")
    ax1.set_xlabel("Time"); ax1.set_ylabel("Price (USD)")
    ax1.grid(alpha=0.25)
    ax1.plot(df.index, df["close"].values, color="#1a1a1a", linewidth=1.2, alpha=0.85, label="BTC-USD Close")

    if "signal" in df.columns:
        buy = df[df["signal"] == "BUY"]
        sell = df[df["signal"] == "SELL"]
        # color the short segments at signal candles
        close_vals = df["close"].values
        for i in range(1, len(df)):
            sig = df["signal"].iloc[i]
            if sig == "BUY":
                ax1.plot(df.index[i-1:i+1], close_vals[i-1:i+1], color="#2ecc71", linewidth=2.3, alpha=0.95)
            elif sig == "SELL":
                ax1.plot(df.index[i-1:i+1], close_vals[i-1:i+1], color="#e74c3c", linewidth=2.3, alpha=0.95)
        ax1.scatter(buy.index, buy["close"], marker="^", color="#27ae60", s=85,
                    edgecolors="white", linewidths=0.8, label="BUY Signal", zorder=5)
        ax1.scatter(sell.index, sell["close"], marker="v", color="#c0392b", s=85,
                    edgecolors="white", linewidths=0.8, label="SELL Signal", zorder=5)
    ax1.legend(loc="upper left", fontsize=9)

    # RSI
    ax2.set_title("Relative Strength Index (RSI)", fontsize=13, weight="bold", color="#222")
    ax2.set_xlabel("Time"); ax2.set_ylabel("RSI"); ax2.grid(alpha=0.25)
    ax2.axhline(70, color="#e74c3c", linestyle="--", linewidth=1)
    ax2.axhline(30, color="#2ecc71", linestyle="--", linewidth=1)
    ax2.fill_between(df.index, 70, 100, color="#e74c3c", alpha=0.08)
    ax2.fill_between(df.index, 0, 30, color="#2ecc71", alpha=0.08)
    ax2.plot(df.index, df["rsi"].values, color="#000000", linewidth=1.3, label="RSI(14)")
    ax2.legend(loc="upper left", fontsize=9)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
        print(f"✅ Chart saved to {save_path}")
        plt.close(fig)
    else:
        plt.show()



"""Simulate 100 daily stock prices and save their price chart."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def simulate_prices(count=100, initial_price=100.0, seed=42):
    """Return positive prices using normally distributed daily log returns."""
    if count < 2:
        raise ValueError("count must be at least 2")
    if not np.isfinite(initial_price) or initial_price <= 0:
        raise ValueError("initial_price must be finite and positive")
    rng = np.random.default_rng(seed)
    increments = rng.normal(loc=0.0005, scale=0.02, size=count - 1)
    return initial_price * np.exp(np.concatenate(([0.0], np.cumsum(increments))))


def calculate_returns(prices):
    """Return simple and log returns for each adjacent pair (N-1 values)."""
    prices = np.asarray(prices, dtype=float)
    if prices.ndim != 1 or prices.size < 2:
        raise ValueError("prices must be a one-dimensional sequence of length >= 2")
    if not np.all(np.isfinite(prices)) or np.any(prices <= 0):
        raise ValueError("prices must be finite and positive")
    daily_returns = prices[1:] / prices[:-1] - 1
    log_returns = np.diff(np.log(prices))
    return daily_returns, log_returns


def plot_prices(prices, output):
    """Save a chart without requiring a graphical display."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(1, len(prices) + 1), prices)
    ax.set(title="Simulated Stock Prices", xlabel="Trading day", ylabel="Price")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    try:
        fig.savefig(output, dpi=150)
    finally:
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("stock_prices.png"))
    args = parser.parse_args()
    prices = simulate_prices(seed=args.seed)
    daily_returns, log_returns = calculate_returns(prices)
    plot_prices(prices, args.output)
    data_output = args.output.with_suffix(".csv")
    if data_output == args.output:
        data_output = args.output.with_name(args.output.stem + "_data.csv")
    # The first observation has no previous price, so its returns are undefined.
    np.savetxt(
        data_output,
        np.column_stack((np.arange(1, 101), prices,
                         np.r_[np.nan, daily_returns], np.r_[np.nan, log_returns])),
        delimiter=",", header="day,price,daily_return,log_return", comments="",
        fmt=["%d", "%.10f", "%.10f", "%.10f"],
    )
    print(f"Generated {len(prices)} prices and {len(daily_returns)} daily/log returns.")
    print(f"Chart: {args.output}; data: {data_output}")


if __name__ == "__main__":
    main()

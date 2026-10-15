# Stock price simulation

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
python -m unittest -v
```

`main.py` generates 100 positive simulated prices, starting at 100, using
daily log increments drawn from a normal distribution (mean 0.0005,
standard deviation 0.02). The default random seed is 42 for reproducibility.
These are synthetic observations, not market data or investment predictions.

Outputs are `stock_prices.png` and `stock_prices.csv`. The CSV includes the
price, simple daily return (`price[t] / price[t-1] - 1`), and log return
(`log(price[t]) - log(price[t-1])`). There are 99 returns for 100 prices;
the first row uses `nan` because it has no preceding observation.
Returns are fractions, so `0.01` means 1%.

Use `python main.py --seed 123 --output chart.png` to change the seed or
output path (the parent directory must exist). Charts use a headless backend.
On machines with a read-only home directory, set `MPLCONFIGDIR` and
`XDG_CACHE_HOME` to writable directories before running.

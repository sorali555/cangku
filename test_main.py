import tempfile
import unittest
from pathlib import Path

import numpy as np

from main import calculate_returns, plot_prices, simulate_prices


class StockSimulationTests(unittest.TestCase):
    def test_simulation_is_positive_and_reproducible(self):
        prices = simulate_prices()
        self.assertEqual(len(prices), 100)
        self.assertEqual(prices[0], 100.0)
        self.assertTrue(np.all(np.isfinite(prices) & (prices > 0)))
        np.testing.assert_array_equal(prices, simulate_prices())
        self.assertFalse(np.array_equal(prices, simulate_prices(seed=43)))

    def test_known_returns(self):
        daily, logarithmic = calculate_returns([100, 110, 99])
        np.testing.assert_allclose(daily, [0.1, -0.1])
        np.testing.assert_allclose(logarithmic, np.log([1.1, 0.9]))

    def test_return_count_and_compounding(self):
        prices = simulate_prices()
        daily, logarithmic = calculate_returns(prices)
        self.assertEqual(len(daily), 99)
        self.assertEqual(len(logarithmic), 99)
        self.assertAlmostEqual(np.prod(1 + daily), prices[-1] / prices[0])
        self.assertAlmostEqual(np.sum(logarithmic), np.log(prices[-1] / prices[0]))

    def test_invalid_prices(self):
        for prices in ([], [100], [[100, 110]], [0, 100], [-1, 100],
                       [100, np.nan], [100, np.inf]):
            with self.subTest(prices=prices), self.assertRaises(ValueError):
                calculate_returns(prices)

    def test_invalid_simulation_parameters(self):
        for kwargs in ({"count": 1}, {"initial_price": 0},
                       {"initial_price": float("nan")}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                simulate_prices(**kwargs)

    def test_plot_is_png(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "prices.png"
            plot_prices(simulate_prices(), output)
            self.assertTrue(output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
            self.assertGreater(output.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()

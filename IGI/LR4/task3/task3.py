"""
Lab 4 - Task 3, Variant 16
Version: 1.0
Developer: Ogienko D.D
Date: 22.04.2026
Description: Logic functions for Task 3

Functions for:
- computing Maclaurin series for sin(x)
- generating table values
- computing errors
- plotting graphs
- saving plots
"""

import matplotlib.pyplot as plt
from validating import safe_float, safe_int, safe_float_abs
import math
import statistics

class SeriesAnalyzer:
    """
    Class that:
    - computes Maclaurin series for sin(x)
    - stores table rows (x, n, F(x), math F(x), eps)
    - computes statistics (mean, median, mode, variance, std)
    """

    def __init__(self, x_start, x_end, step, n_terms):
        self.rows = []
        x = x_start
        while x <= x_end + 1e-9:
            self.add_value(x, n_terms)
            x += step

    @staticmethod
    def compute_series(x, n_terms):
        """Compute sin(x) using Maclaurin series (same as in LR3)."""
        s = 0
        for n in range(n_terms):
            s += ((-1)**n) * (x**(2*n + 1)) / math.factorial(2*n + 1)
        return s

    def add_value(self, x, n_terms):
        """Compute row and store it."""
        f_series = self.compute_series(x, n_terms)
        f_math = math.sin(x)
        eps = abs(f_series - f_math)

        self.rows.append({
            "x": x,
            "n": n_terms,
            "F_x": f_series,
            "math_F_x": f_math,
            "eps": eps
        })

    def mean(self):
        """Compute mean."""
        return statistics.mean(r["F_x"] for r in self.rows)

    def median(self):
        """Compute median."""
        return statistics.median(r["F_x"] for r in self.rows)

    def mode(self):
        """Compute mode."""
        try:
            return statistics.mode(r["F_x"] for r in self.rows)
        except statistics.StatisticsError:
            return None

    def variance(self):
        """Compute variance."""
        return statistics.pvariance(r["F_x"] for r in self.rows)

    def std(self):
        """Compute standard deviation."""
        return statistics.pstdev(r["F_x"] for r in self.rows)


    def _format_table(self) -> str:
        """
        Build formatted table of stored rows.
        """
        if not self.rows:
            return "No data."

        headers = ("x", "n", "F(x)", "Math F(x)", "eps")
        widths = (12, 6, 20, 20, 12)

        sep = "+" + "+".join("-" * w for w in widths) + "+"
        header = "|" + "|".join(h.center(w) for h, w in zip(headers, widths)) + "|"

        lines = [sep, header, sep]

        for r in self.rows:
            line = (
                    "|" +
                    f"{r['x']:<12.6g}" +
                    f"|{r['n']:<6d}" +
                    f"|{r['F_x']:<20.12g}" +
                    f"|{r['math_F_x']:<20.12g}" +
                    f"|{r['eps']:<12.6g}" +
                    "|"
            )
            lines.append(line)

        lines.append(sep)
        return "\n".join(lines)

    def visualize(self, eps_list, filename="plot.png"):
        """
        Plot series and math.sin on same axes.
        """
        plt.figure(figsize=(10, 6))

        # series graph
        plt.plot(self.x, self.series, "o--", color="blue", label="Series F(x)")
        # math.sin graph
        plt.plot(self.x, self.math, "-", color="red", label="math.sin(x)")

        plt.xlabel("x")
        plt.ylabel("F(x)")
        plt.title("Maclaurin Series vs math.sin(x)")
        plt.grid(True)
        plt.legend()

        max_eps = max(self.eps)
        idx = self.eps.index(max_eps)

        plt.annotate(
            f"max eps = {max_eps:.2e}",
            xy=(self.x[idx], self.series[idx]),
            xytext=(self.x[idx], self.series[idx] + 0.2),
            arrowprops=dict(arrowstyle="->", color="black")
        )

        plt.savefig(filename, dpi=300)
        plt.close()


    def __str__(self) -> str:
        return self._format_table()

    @property
    def x(self):
        return [r["x"] for r in self.rows]

    @property
    def series(self):
        return [r["F_x"] for r in self.rows]

    @property
    def math(self):
        return [r["math_F_x"] for r in self.rows]

    @property
    def eps(self):
        return [r["eps"] for r in self.rows]


def main():
    """Main function."""
    print("Task 3:")

    x_start = safe_float("Enter x start: ")
    x_end = safe_float("Enter x end: ")
    step = safe_float_abs("Enter step: ")
    while True:
        n_terms = safe_int("Enter number of terms in series: ")
        try:
            analyzer = SeriesAnalyzer(x_start, x_end, step, n_terms)
            print(analyzer)
        except OverflowError:
            print("The number of terms is too large. Enter again.")
            continue
        break
    print("\n--- Statistics ---")
    print("Mean:", analyzer.mean())
    print("Median:", analyzer.median())
    print("Mode:", analyzer.mode())
    print("Variance:", analyzer.variance())
    print("Std deviation:", analyzer.std())

    filename = "series_plot.png"
    analyzer.visualize(filename)
    print(f"\nPlot saved to {filename}")


if __name__ == "__main__":
    main()
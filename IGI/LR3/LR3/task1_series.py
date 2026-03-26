"""
Lab 3 - Task 1 (power series).
Variant 16: compute sin(x).
Purpose: compute function value via power series with epsilon and max iterations.
Author: Ogienko D.D.
Version: 1.2.
Date: 25.03.2026.
"""

import math
from decorators import repeatable

@repeatable
def series_sin(x: float = None, eps: float = None, max_iter: int = 500):
    """
    Compute sin(x) using power series:
    sin(x) = sum_{k=0..inf} (-1)^k * x^(2k+1) / (2k+1)!
    """
    while True:
        try:
            if x is None:
                x = float(input("Enter x (real number): ").strip())
            if eps is None:
                eps = float(input("Enter eps (e.g., 1e-8): ").strip())
            if eps <= 0:
                print("eps must be a positive number.")
                x = None
                eps = None
                continue
        except ValueError:
            print("Invalid numeric input.")
            x = None
            eps = None
            continue
        break

    try:
        term = x
        s = term
        k = 0

        while abs(term) >= eps and k < max_iter:
            k += 1
            term *= -1 * x * x / ((2 * k) * (2 * k + 1))
            s += term

        n_terms = k + 1
        math_val = math.sin(x)

        col_names = ("x", "n", "F(x)", "Math F(x)", "eps")
        widths = (12, 6, 20, 20, 12)
        sep = "+" + "+".join("-" * w for w in widths) + "+"
        header = "|" + "|".join(name.center(w) for name, w in zip(col_names, widths)) + "|"
        row = (
            "|" +
            f"{x:<12.6g}" + "|" +
            f"{n_terms:<6d}" + "|" +
            f"{s:<20.12g}" + "|" +
            f"{math_val:<20.12g}" + "|" +
            f"{eps:<12.6g}" + "|"
        )

        print(sep)
        print(header)
        print(sep)
        print(row)
        print(sep)

        return {"x": x, "n": n_terms, "F_x": s, "math_F_x": math_val, "eps": eps}

    except OverflowError:
        print("Overflow error during computation.")
    except ZeroDivisionError:
        print("Division by zero encountered during series computation.")
    except Exception as e:
        print(f"Unexpected error: {e}")

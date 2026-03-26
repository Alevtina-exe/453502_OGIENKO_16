"""
Lab 3 - Sequence initialization utilities.
Purpose: provide functions to initialize numeric sequences (generator and user input).
Author: Ogienko D.D.
Version: 1.1.
Date: 25.03.2026.
"""

import random
from typing import List

def gen_random_sequence(n: int, low: int = -10, high: int = 10):
    """
    Generate n random floats in [low, high] using a generator.
    """
    for _ in range(n):
        yield random.uniform(low, high)

def input_sequence(n: int) -> List[float]:
    """
    Read n numbers from user with validation.
    """
    seq = []
    for i in range(n):
        while True:
            try:
                val = float(input(f"Enter element {i+1}/{n}: ").strip())
                seq.append(val)
                break
            except ValueError:
                print("Invalid number, please enter a numeric value.")
    return seq

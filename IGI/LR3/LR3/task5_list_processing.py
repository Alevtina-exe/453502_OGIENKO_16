"""
Lab 3 - Task 5 (list processing).
Variant 16 tasks:
a) find index of element with maximum absolute value;
b) sum elements after first positive element.
Author: Ogienko D.D.
Version: 1.7.
Date: 25.03.2026.
"""

from typing import List, Optional, Callable
from decorators import repeatable
from init_seq import gen_random_sequence, input_sequence

def find_max_abs_index(seq: List[float]) -> int:
    """
    Return the index of the element with maximum absolute value.
    """
    if not seq:
        raise ValueError("Sequence is empty.")
    return max(range(len(seq)), key=lambda i: abs(seq[i]))

def sum_after_first_positive(seq: List[float]) -> float:
    """
    Return the sum of elements located after the first positive element in seq.
    """
    for i, v in enumerate(seq):
        if v > 0:
            return sum(seq[i+1:])
    return 0.0

def _compute_results(seq: List[float]) -> dict:
    """
    Compute and return results: index of max-by-abs and sum after first positive.
    """
    idx = find_max_abs_index(seq)
    s = sum_after_first_positive(seq)
    return {"max_abs_index": idx, "sum_after_first_positive": s}

def process_list_from_values(seq: List[float]) -> dict:
    """
    Process a user-provided sequence and print the results.
    """
    try:
        results = _compute_results(seq)
        print(f"Index of element with maximum absolute value: {results['max_abs_index']}")
        print(f"Sum of elements after first positive: {results['sum_after_first_positive']}")
        return results
    except Exception as e:
        print(f"Error: {e}")
        return {}


def process_list_from_generated(seq: List[float]) -> dict:
    """
    Process a generated sequence and print the results.
    """
    try:
        results = _compute_results(seq)
        print("Generated sequence:")
        print(seq)
        print(f"Index of element with maximum absolute value: {results['max_abs_index']}")
        print(f"Sum of elements after first positive: {results['sum_after_first_positive']}")
        return results
    except Exception as e:
        print(f"Error: {e}")
        return {}

@repeatable("Do you want to repeat Task 5? (y/n): ")
def run_task5(gen_func: Optional[Callable[[int, float, float], List[float]]] = None):
    """
    Runner for Task 5.
    Asks for number of elements, then whether to input data or generate it,
    then calls the appropriate processing function.
    """
    while True:
        try:
            n = int(input("Enter number of elements (positive integer): ").strip())
            if n <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid integer, try again.")

    while True:
        choice = input("Enter data manually or generate? (m/g): ").strip().lower()

        if choice in ("m", "manual", "i", "input"):
            try:
                seq = input_sequence(n)
                return process_list_from_values(seq)
            except Exception as e:
                print(f"Error processing input sequence: {e}")
                return {}

        if choice in ("g", "gen", "generate"):
            low = None
            high = None

            while low is None or high is None:
                if low is None:
                    try:
                        low_str = input("Enter lower bound (default -10): ").strip()
                        low = float(low_str) if low_str else -10.0
                    except ValueError:
                        print("Invalid lower bound, try again.")
                        low = None
                        continue

                if high is None:
                    try:
                        high_str = input("Enter upper bound (default 10): ").strip()
                        high = float(high_str) if high_str else 10.0
                    except ValueError:
                        print("Invalid upper bound, try again.")
                        high = None
                        continue

                if  low > high:
                    print("Lower bound must be <= upper bound.")
                    low = None
                    high = None

            try:
                generator = gen_func if gen_func is not None else gen_random_sequence
                seq = generator(n, low, high)
                return process_list_from_generated(seq)
            except Exception as e:
                print(f"Error generating sequence: {e}")
                return {}

        print("Please answer 'm' for manual input or 'g' for generation.")

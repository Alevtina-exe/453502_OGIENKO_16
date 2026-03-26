"""
Lab 3 - Task 5 (list processing).
Variant 16 tasks.
Author: Ogienko D.D.
Version: 1.5.
Date: 2026-03-26.
"""

from typing import List, Optional, Callable
from decorators import repeatable
from init_seq import gen_random_sequence


def input_float_list_interactive(n: int) -> List[float]:
    """
    Read exactly n float elements from the user with validation and return the list.
    Raises ValueError if n is not positive.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer.")
    seq: List[float] = []
    for i in range(n):
        while True:
            try:
                val = float(input(f"Element {i+1}: ").strip())
                seq.append(val)
                break
            except ValueError:
                print("Invalid number, try again.")
    return seq


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
    if not seq:
        raise ValueError("Sequence is empty.")
    idx = find_max_abs_index(seq)
    s = sum_after_first_positive(seq)
    return {"max_abs_index": idx, "sum_after_first_positive": s}


def process_list_from_values(seq: List[float]) -> dict:
    """
    Process a user-provided sequence and print the results.
    Returns a dictionary with computed values.
    """
    try:
        results = _compute_results(seq)
        print(f"Index of element with maximum absolute value: {results['max_abs_index']}")
        print(f"Sum of elements after first positive: {results['sum_after_first_positive']}")
        return results
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}


def process_list_from_generated(seq: List[float]) -> dict:
    """
    Process a generated sequence and print the results.
    Returns a dictionary with computed values.
    """
    try:
        results = _compute_results(seq)
        print("Generated sequence:")
        print(seq)
        print(f"Index of element with maximum absolute value: {results['max_abs_index']}")
        print(f"Sum of elements after first positive: {results['sum_after_first_positive']}")
        return results
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}


@repeatable("Do you want to repeat Task 5? (y/n): ")
def run_task5(gen_func: Optional[Callable[[int, float, float], List[float]]] = None):
    """
    Interactive runner for Task 5.
    Asks for number of elements, then whether to input data or generate it,
    then calls the appropriate processing function. Uses gen_random_sequence if no gen_func provided.
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
                seq = input_float_list_interactive(n)
                return process_list_from_values(seq)
            except Exception as e:
                print(f"Error processing input sequence: {e}")
                return {}
        if choice in ("g", "gen", "generate"):
            while True:
                try:
                    low_s = input("Enter lower bound for generation (default -10): ").strip()
                    high_s = input("Enter upper bound for generation (default 10): ").strip()
                    low = float(low_s) if low_s else -10.0
                    high = float(high_s) if high_s else 10.0
                    if low > high:
                        print("Lower bound must be <= upper bound.")
                        continue
                    break
                except ValueError:
                    print("Invalid bound, try again.")
            try:
                generator = gen_func if gen_func is not None else gen_random_sequence
                seq = generator(n, low, high)
                if not isinstance(seq, list):
                    raise TypeError("Generator did not return a list.")
                return process_list_from_generated(seq)
            except Exception as e:
                print(f"Error generating or processing sequence: {e}")
                return {}
        print("Please answer 'm' for manual input or 'g' for generation.")

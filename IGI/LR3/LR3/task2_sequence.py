"""
Lab 3 - Task 2 (sequence sums / counts).
Variant 16: Count odd natural numbers; termination input is 0.
Author: Ogienko D.D.
Version: 1.1.
Date: 25.03.2026.
"""

from decorators import repeatable

def is_natural(n: int) -> bool:
    return n > 0 and float(n).is_integer()

@repeatable
def count_odd_naturals():
    """
    Reads integers until 0 is entered. Counts odd natural numbers.
    """
    count = 0
    print("Enter integers one by one. Enter 0 to finish.")

    while True:
        s = input("Enter integer: ").strip()
        try:
            val = int(s)
        except ValueError:
            print("Invalid integer, try again.")
            continue

        if val == 0:
            break

        if is_natural(val) and val % 2 != 0:
            count += 1

    print(f"Count of odd natural numbers entered: {count}")

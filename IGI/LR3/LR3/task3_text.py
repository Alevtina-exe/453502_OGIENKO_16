"""
Lab 3 - Task 3 (text analysis).
Variant 16: count punctuation characters.
Author: Ogienko D.D.
Version: 1.1.
Date: 25.03.2026.
"""

from decorators import repeatable
import string

@repeatable
def count_punctuation():
    """
    Reads a line and counts punctuation characters.
    """
    s = input("Enter a line of text: ")

    try:
        punct = set(string.punctuation)
        cnt = sum(1 for ch in s if ch in punct)
        print(f"Punctuation characters count: {cnt}")
    except Exception as e:
        print(f"Unexpected error: {e}")

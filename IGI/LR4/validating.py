"""
Lab 4 - Validating functions.
Purpose: functions for safe input.
Author: Ogienko D.D.
Version: 1.0
Date: 23.04.2026
"""

from matplotlib.colors import to_rgba

def safe_float(prompt: str):
    """Get float from user."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid float number.")

def safe_float_abs(prompt: str):
    """Get positive float from user."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Value must be positive.")
                continue
            return value
        except ValueError:
            print("Invalid float number.")

def safe_color(prompt: str):
    """Get non-empty color string."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Color cannot be empty.")
            continue
        try:
            to_rgba(value)
        except ValueError:
            print("Invalid color.")
            continue
        return value

def safe_text(prompt: str):
    """Get non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Text cannot be empty.")

def safe_input(prompt: str) -> str:
    """Return non-empty user input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def safe_int(prompt):
    while True:
        try:
            v = int(input(prompt))
            if v <= 0:
                print("Value must be positive.")
                continue
            return v
        except ValueError:
            print("Invalid integer.")
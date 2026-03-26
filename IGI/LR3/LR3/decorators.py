"""
Lab 3 - Decorators module.
Purpose: provide utility decorators used in lab tasks.
Author: Ogienko D.D.
Version: 1.2.
Date: 25.03.2026.
"""

def repeatable(func):
    """
    Decorator factory to allow repeating an interactive function until user declines.
    """
    def wrapper(*args, **kwargs):
        while True:
            result = func(*args, **kwargs)
            ans = input("Do you want to repeat the Task? (y/n)").strip().lower()
            if ans not in ('y', 'yes'):
                return result
    return wrapper



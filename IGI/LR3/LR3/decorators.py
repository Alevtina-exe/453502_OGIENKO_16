"""
Lab 3 - Decorators module.
Purpose: provide utility decorators used in lab tasks.
Author: Ogienko D.D.
Version: 1.2.
Date: 25.03.2026.
"""

def repeatable(prompt_message="Run again? (y/n): "):
    """
    Decorator factory to allow repeating an interactive function until user declines.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                result = func(*args, **kwargs)
                ans = input(prompt_message).strip().lower()
                if ans not in ('y', 'yes'):
                    return result

        return wrapper

    return decorator


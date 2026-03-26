"""
Lab 3 - Main program.
Purpose: interactive menu to run tasks.
Author: Ogienko D.D.
Version: 1.1.
Date: 25.03.2026.
"""

from task1_series import series_sin
from task2_sequence import count_odd_naturals
from task3_text import count_punctuation
from task4_string_analyzer import analyze_string
from task5_list_processing import run_task5

def print_menu():
    """
    Print the interactive menu for main program.
    """
    print("\nSelect a task:")
    print("1. Task 1: Compute sin(x) by power series")
    print("2. Task 2: Count odd natural numbers (input until 0)")
    print("3. Task 3: Count punctuation in input string")
    print("4. Task 4: Analyze fixed sentence (variant tasks)")
    print("5. Task 5: List processing (max-by-abs index and sum after first positive)")
    print("0. Exit")

def main():
    """
    Main program.
    """
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == '0':
            break

        elif choice == '1':
            series_sin()

        elif choice == '2':
            count_odd_naturals()

        elif choice == '3':
            count_punctuation()

        elif choice == '4':
            analyze_string()

        elif choice == '5':
            run_task5()

        else:
            print("Unknown option. Please choose 0-5.")


if __name__ == "__main__":
    main()

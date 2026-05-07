"""
Lab 4 - Main program.
Purpose: interactive menu to run all tasks of the lab.
Author: Ogienko D.D.
Version: 1.0
Date: 23.04.2026
"""

from task1.task1 import main as task1_main
from task2.task2 import main as task2_main
from task3.task3 import main as task3_main
from task4.task4 import main as task4_main
from task5.task5 import main as task5_main
from task6.task6 import main as task6_main


def print_menu():
    """
    Print the interactive menu for the main program.
    """
    print("\nSelect a task from Lab 4:")
    print("1. Task 1: Serialization, classes, CSV & pickle")
    print("2. Task 2: Text analysis with regex, archiving")
    print("3. Task 3: Maclaurin series, statistics, matplotlib")
    print("4. Task 4: OOP geometry, abstract classes, drawing")
    print("5. Task 5: NumPy arrays, math & statistics")
    print("6. Task 6: Pandas Series/DataFrame, UFO dataset analysis")
    print("0. Exit")


def main():
    """
    Main program loop.
    """
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == '0':
            print("Exiting program.")
            break

        elif choice == '1':
            task1_main()

        elif choice == '2':
            task2_main()

        elif choice == '3':
            task3_main()

        elif choice == '4':
            task4_main()

        elif choice == '5':
            task5_main()

        elif choice == '6':
            task6_main()

        else:
            print("Unknown option. Please choose 0–6.")


if __name__ == "__main__":
    main()

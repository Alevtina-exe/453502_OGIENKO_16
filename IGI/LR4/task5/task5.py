"""
Lab 4 - Task 5, Variant 16
Version: 1.0
Developer: Ogienko D.D
Date: 22.04.2026
Description: Logic functions for Task 5

Functions for:
- generating random matrix
- demonstrating NumPy operations
- finding column with minimal sum
- computing median in two ways
"""

import numpy as np
from validating import safe_int


class MatrixAnalyzer:
    """Class for analyzing integer NumPy matrices."""

    def __init__(self, matrix: np.ndarray):
        """
        Initialize analyzer with a NumPy matrix.
        """
        if not isinstance(matrix, np.ndarray):
            raise TypeError("Matrix must be a NumPy array.")
        self.matrix = matrix
        self.min_col = self.column(self.min_sum_column_index())


    def __str__(self):
        """String representation."""
        return f"MatrixAnalyzer(shape={self.matrix.shape})"


    def column_sums(self):
        """
        Compute sum of each column.
        """
        return np.sum(self.matrix, axis=0)

    def min_sum_column_index(self):
        """
        Find index of column with minimal sum.
        """
        return np.argmin(self.column_sums())

    def column(self, index: int):
        """
        Extract a column by index.
        """
        return self.matrix[:, index]

    def col_median_numpy(self):
        """
        Compute median using NumPy.
        """
        return np.median(self.min_col)

    def col_median_manual(self):
        """
        Compute median manually (without NumPy).
        """
        arr_sorted = sorted(self.min_col)
        n = len(arr_sorted)
        mid = n // 2

        if n % 2 == 1:
            return arr_sorted[mid]
        else:
            return (arr_sorted[mid - 1] + arr_sorted[mid]) / 2


    @staticmethod
    def generate_matrix(n, m, low=0, high=50):
        """
        Generate random integer matrix A[n, m].
        """
        matrix = np.random.randint(low, high, size=(n, m))
        return MatrixAnalyzer(matrix)


def main():
    """
    Main function.
    """
    print("Task 5:")

    n = safe_int("Enter number of rows n: ")
    m = safe_int("Enter number of columns m: ")

    analyzer = MatrixAnalyzer.generate_matrix(n, m)

    print("\nGenerated matrix A:")
    print(analyzer.matrix)

    col_index = analyzer.min_sum_column_index()
    col = analyzer.column(col_index)
    median_np = analyzer.col_median_numpy()
    median_manual = analyzer.col_median_manual()

    print("\nColumn analysis:")
    print(f"Column with minimal sum: index {col_index}")
    print("Column values:", col)
    print("Median (NumPy):", median_np)
    print("Median (manual):", median_manual)


if __name__ == "__main__":
    main()
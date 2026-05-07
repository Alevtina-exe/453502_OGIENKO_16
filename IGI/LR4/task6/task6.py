"""
Lab 4 - Task 6, Variant 16
Version: 1.0
Developer: Ogienko D.D
Date: 22.04.2026
Description:
Pandas analysis of UFO dataset.
Contains:
- DataFrame wrapper
- Analyzer class with Subtask A and B logic
- Single main() entry point
"""

import pandas as pd


class DataFrameWrapper:
    """Stores DataFrame."""
    def __init__(self, df):
        self.df = df


class UFOAnalyzer:
    """Performs Subtask A and Subtask B analysis."""

    def __init__(self, dfw: DataFrameWrapper):
        self.dfw = dfw

    def subtask_A(self):
        df = self.dfw.df
        return df["State"].str[:1].str.upper()

    def subtask_B(self):
        df = self.dfw.df

        df.columns = df.columns.str.strip()

        df["Duration"] = pd.to_timedelta(df["Duration"], errors="coerce").dt.total_seconds()
        df["Shape"] = df["Shape"].astype(str).str.strip()

        df = df.dropna(subset=["Duration"])
        df = df[df["Shape"] != ""]
        df = df[df["Shape"].str.lower() != "nan"]

        shape_counts = df["Shape"].value_counts()

        most_freq = shape_counts.index[0]
        rarest = shape_counts.index[-1]

        mean_most = df[df["Shape"] == most_freq]["Duration"].mean()
        mean_rare = df[df["Shape"] == rarest]["Duration"].mean()
        ratio = mean_most / mean_rare if mean_rare != 0 else None

        mean_ca = df[df["State"] == "AL"]["Duration"].mean()

        return most_freq, rarest, mean_most, mean_rare, ratio, mean_ca


def load_ufo_dataset(path="ufo.csv"):
    df = pd.read_csv(path)
    return DataFrameWrapper(df)


def main():
    print("Task 6:")

    print("\nSubtask A:\nNo.\tState Codes(1st letter)")
    dfw = load_ufo_dataset()
    analyzer = UFOAnalyzer(dfw)

    print(analyzer.subtask_A())

    most, rare, m_most, m_rare, ratio, ca = analyzer.subtask_B()

    print("\nSubtask B:")
    print(f"Most frequent shape: {most}")
    print(f"Rarest shape: {rare}")
    print(f"Mean duration (most frequent): {m_most:.2f}")
    print(f"Mean duration (rarest): {m_rare:.2f}")
    print(f"Ratio: {ratio:.2f}")
    print(f"Mean duration in California: {ca:.2f}")


if __name__ == "__main__":
    main()

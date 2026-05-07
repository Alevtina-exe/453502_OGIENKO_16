"""
Lab 4 - Task 1, Variant 16
Version: 1.0
Developer: Ogienko D.D
Date: 22.04.2026
Description:
This module contains classes
for representing applicants
of the Music-Pedagogical Faculty
including methods for:
- searching applicants
- grouping by instrument
- CSV and pickle serialization
"""


import csv
import pickle
import os
from validating import safe_input


class SerializationMixin:
    """Checks if file exists."""
    @staticmethod
    def check_file(filename):
        return os.path.exists(filename)


class CsvMixin(SerializationMixin):
    """Saves and loads objects in CSV."""
    def save_to_csv(self, objects, filename):
        """Saves objects in CSV file."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["last_name", "instrument", "exam_score"])
            writer.writeheader()
            for obj in objects:
                writer.writerow({
                    "last_name": obj.last_name,
                    "instrument": obj.instrument,
                    "exam_score": obj.exam_score if obj.exam_score is not None else ""
                })

    def load_from_csv(self, filename):
        """Loads data from CSV file."""
        result = []
        if not self.check_file(filename):
            return result
        with open(filename, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                score = float(row["exam_score"]) if row["exam_score"] else None
                result.append(ApplicantWithExam(row["last_name"], row["instrument"], score))
        return result


class PickleMixin(SerializationMixin):
    """Saves and loads objects in pickle."""
    def save_to_pickle(self, objects, filename):
        """Saves objects in pickle file."""
        with open(filename, "wb") as f:
            pickle.dump(objects, f)

    def load_from_pickle(self, filename):
        """Loads objects from pickle file."""
        if not self.check_file(filename):
            return []
        with open(filename, "rb") as f:
            return pickle.load(f)


class Applicant:
    """Represents an applicant."""

    faculty_name = "Music-Pedagogical Faculty"

    def __init__(self, last_name, instrument):
        self.last_name = last_name
        self.instrument = instrument

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value.strip():
            raise ValueError("Last name cannot be empty.")
        self._last_name = value.title()

    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        if not value.strip():
            raise ValueError("Instrument cannot be empty.")
        self._instrument = value.title()

    def __str__(self):
        return f"{self.last_name} ({self.instrument})"

    def __lt__(self, other):
        return (self.instrument, self.last_name) < (other.instrument, other.last_name)


class ApplicantWithExam(Applicant):
    """Represents an applicant with exam score."""

    def __init__(self, last_name, instrument, exam_score=None):
        super().__init__(last_name, instrument)
        self.exam_score = exam_score

    @property
    def exam_score(self):
        return self._exam_score

    @exam_score.setter
    def exam_score(self, value):
        if value is not None and not (0 <= value <= 100):
            raise ValueError("Exam score must be between 0 and 100.")
        self._exam_score = value

    def __str__(self):
        base = super().__str__()
        return f"{base} — score: {self.exam_score}" if self.exam_score is not None else f"{base} — exam not taken"


class ApplicantManager(CsvMixin, PickleMixin):
    """Manages applicants and file operations."""

    def __init__(self, csv_file, pkl_file):
        self.csv_file = csv_file
        self.pkl_file = pkl_file
        self.applicants = []

    def load_initial_data(self, data):
        """Loads data for initialisation."""
        for item in data:
            self.applicants.append(
                ApplicantWithExam(item["last_name"], item["instrument"], item["exam_score"])
            )
        self.applicants.sort()

    def group_by_instrument(self):
        """Groups applicants by instrument."""
        groups = {}
        for a in self.applicants:
            groups.setdefault(a.instrument, []).append(a)
        return groups

    def find_by_last_name(self, name):
        """Finds applicants by last name."""
        name = name.title()
        return [a for a in self.applicants if a.last_name == name]


APPLICANTS = [
    {"last_name": "Ivanov", "instrument": "Piano", "exam_score": None},
    {"last_name": "Petrova", "instrument": "Violin", "exam_score": 88},
    {"last_name": "Sidorov", "instrument": "Piano", "exam_score": 73},
    {"last_name": "Smirnova", "instrument": "Guitar", "exam_score": None},
]


def main():
    manager = ApplicantManager("applicants.csv", "applicants.pkl")
    manager.load_initial_data(APPLICANTS)

    while True:
        print("\nTask 1:")
        print("1. Save to CSV and pickle")
        print("2. Load from CSV")
        print("3. Load from pickle")
        print("4. Show exam lists by instrument")
        print("5. Find applicant by last name")
        print("0. Exit")

        cmd = safe_input("Choose option: ")

        if cmd == "1":
            manager.save_to_csv(manager.applicants, manager.csv_file)
            manager.save_to_pickle(manager.applicants, manager.pkl_file)
            print("Saved.")

        elif cmd == "2":
            manager.applicants = manager.load_from_csv(manager.csv_file)
            print("Loaded from CSV.")

        elif cmd == "3":
            manager.applicants = manager.load_from_pickle(manager.pkl_file)
            print("Loaded from pickle.")

        elif cmd == "4":
            groups = manager.group_by_instrument()
            for instr, group in sorted(groups.items()):
                print(f"\nInstrument: {instr}")
                for a in sorted(group):
                    print("  -", a)

        elif cmd == "5":
            name = safe_input("Enter last name: ")
            found = manager.find_by_last_name(name)
            if found:
                for a in found:
                    print("  -", a)
            else:
                print("Not found.")

        elif cmd == "0":
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

"""
Lab 4 - Task 2, Variant 16
Version: 1.0
Developer: Ogienko D.D
Date: 22.04.2026
Description: Classes & functions for Task 2:
- regex-based text analysis
- counting sentences
- counting smileys
- replacing characters in words
"""


import re
import zipfile
from validating import safe_int

class PrintableMixin:
    """Returns string representation."""
    def pretty(self):
        return str(self)


class BaseText:
    """Stores raw text."""
    def __init__(self, text):
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError("Text must be a string.")
        self._text = value

    def __len__(self):
        return len(self.text)


class TextAnalyzer(BaseText, PrintableMixin):
    """Performs regex-based text analysis."""

    def count_sentences(self):
        """Counts sentences in text."""
        return len(re.findall(r"[.!?]+", self.text))

    def count_sentence_types(self):
        """Counts sentences by types in text."""
        declarative = len(re.findall(r"\.", self.text))
        interrogative = len(re.findall(r"\?", self.text))
        exclamatory = len(re.findall(r"!", self.text))
        return declarative, interrogative, exclamatory

    def average_sentence_length(self):
        """Counts average sentence length in text."""
        sentences = re.split(r"[.!?]+", self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0
        lengths = [len(re.sub(r"[^A-Za-zА-Яа-я]", "", s)) for s in sentences]
        return sum(lengths) / len(lengths)

    def average_word_length(self):
        """Counts average word length in text."""
        words = re.findall(r"[A-Za-zА-Яа-я]+", self.text)
        if not words:
            return 0
        return sum(len(w) for w in words) / len(words)

    def count_smileys(self):
        """Count smileys in text."""
        pattern = r"[:;]-*([\(\)\[\]])\1+"
        return len(re.findall(pattern, self.text))

    def replace_last_three(self, length):
        """Replaces last three characters in words with given length."""
        def repl(match):
            w = match.group()
            return w[:-3] + "$$$"
        pattern = rf"\b[A-Za-zА-Яа-я]{{{length}}}\b"
        return re.sub(pattern, repl, self.text)

    def find_times(self):
        """Finds time stamps in text."""
        return re.findall(r"\b[0-2]\d:[0-5]\d\b", self.text)

    def count_max_length_words(self):
        """Counts max length words in text."""
        words = re.findall(r"[A-Za-zА-Яа-я]+", self.text)
        if not words:
            return 0
        max_len = max(len(w) for w in words)
        return sum(1 for w in words if len(w) == max_len)

    def words_before_punctuation(self):
        """Finds words before punctuation symbols."""
        return re.findall(r"\b([A-Za-zА-Яа-я]+)(?=[,.])", self.text)

    def longest_word_ending_e(self):
        """Finds the longest word ending with the letter e"""
        words = re.findall(r"[A-Za-zА-Яа-я]+е(?![A-Za-zА-Яа-я])", self.text, flags=re.IGNORECASE)
        if not words:
            return None
        return max(words, key=len)

    def __str__(self):
        return f"TextAnalyzer(len={len(self.text)})"


def archive_file(source, archive_name):
    """Archives file into zip archive."""
    with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(source)
        info = z.getinfo(source)
    return info


def main():
    """Main function."""
    print("Task 2:")

    input_file = "input.txt"
    output_file = "result.txt"
    archive_name = "result.zip"

    try:
        with open(input_file , "r", encoding="utf-8") as f:
            analyzer = TextAnalyzer(f.read())
        total_sent = analyzer.count_sentences()
        dec, inter, excl = analyzer.count_sentence_types()
        avg_sent = analyzer.average_sentence_length()
        avg_word = analyzer.average_word_length()
        smileys = analyzer.count_smileys()
        times = analyzer.find_times()
        max_words = analyzer.count_max_length_words()
        punct_words = analyzer.words_before_punctuation()
        longest_e = analyzer.longest_word_ending_e()

        length = safe_int("Enter word length to replace last 3 chars: ")
        replaced_text = analyzer.replace_last_three(length)

        result = (
            f"Total sentences: {total_sent}\n"
            f"Declarative: {dec}\n"
            f"Interrogative: {inter}\n"
            f"Exclamatory: {excl}\n"
            f"Average sentence length: {avg_sent:.2f}\n"
            f"Average word length: {avg_word:.2f}\n"
            f"Smileys found: {smileys}\n"
            f"Times found: {times}\n"
            f"Words with max length: {max_words}\n"
            f"Words before punctuation: {punct_words}\n"
            f"Longest word ending with 'e': {longest_e}\n\n"
            f"Text with replacements:\n{replaced_text}\n"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print("Analysis saved to result.txt")

        info = archive_file(output_file, archive_name)
        print("Archived:", info.filename, "size:", info.file_size)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()

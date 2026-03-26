"""
Lab 3 - Task 4 (fixed string analysis).
Variant 16 tasks
 a) count words ending with a consonant;
 b) compute average word length (rounded) and list words of that length or message;
 c) print every 7th word.
Author: Ogienko D.D.
Version: 1.1.
Date: 25.03.2026.
"""

TEXT = ("So she was considering in her own mind, as well as she could, "
        "for the hot day made her feel very sleepy and stupid, "
        "whether the pleasure of making a daisy-chain would be "
        "worth the trouble of getting up and picking the daisies, "
        "when suddenly a White Rabbit with pink eyes ran close by her.")

def split_words(text: str):
    cleaned = text.replace(",", " ").replace(".", " ")
    return [w.strip() for w in cleaned.split() if w.strip()]

def is_consonant(ch: str) -> bool:
    vowels = set("aeiou")
    return ch.isalpha() and ch.lower() not in vowels

def count_words_ending_with_consonant(words):
    return sum(1 for w in words if is_consonant(w[-1]))

def words_with_average_length(words):
    lengths = [len(w) for w in words]
    avg_len = round(sum(lengths) / len(lengths))
    return avg_len, [w for w in words if len(w) == avg_len]

def every_seventh_word(words):
    return [words[i] for i in range(6, len(words), 7)]

def analyze_string():
    """
    Run all three subtasks and print results.
    """
    words = split_words(TEXT)

    consonant_count = count_words_ending_with_consonant(words)
    avg_len, avg_words = words_with_average_length(words)
    seventh = every_seventh_word(words)

    print(f"Total words: {len(words)}")
    print(f"Words ending with consonant: {consonant_count}")
    print(f"Average length (rounded): {avg_len}")
    print(f"Words with this length: {avg_words if avg_words else 'None'}")
    print(f"Every 7th word: {seventh}")



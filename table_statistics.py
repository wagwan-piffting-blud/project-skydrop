import re
import pandas as pd
from fuzzywuzzy import fuzz
from operator import itemgetter

CODE_BOOK = "scroll.htm" # Or bounty.htm for Bounty/Final Puzzle

def load_codebook():
    codebook_df = pd.read_html(CODE_BOOK, header=0)[1]
    codebook = codebook_df.drop_duplicates('Word').set_index('Word').T.to_dict('list')
    return codebook

def load_codebook2():
    codebook_df = pd.read_html(CODE_BOOK, header=0)[2]
    codebook = codebook_df.drop_duplicates('Word').set_index('Word').T.to_dict('list')
    return codebook

codebook = load_codebook()
codebook2 = load_codebook2()

def count_number_occurrences(codebook):
  number_counts = {}
  for word, numbers in codebook.items():
    for number in numbers:
      number_counts[number] = number_counts.get(number, 0) + 1

  sorted_number_counts = dict(sorted(number_counts.items()))

  return sorted_number_counts

number_counts = count_number_occurrences(codebook)
total = 0

print("Mountain Table:")

for number, count in number_counts.items():
    print(f"Number {number}: {count} occurrences")
    total += count

print(f"Total items in Mountain Table: {total}")

print("-" * 120)

print("Secret Words Table:")

number_counts = count_number_occurrences(codebook2)
total = 0

for number, count in number_counts.items():
    print(f"Number {number}: {count} occurrences")
    total += count

print(f"Total items in Secret Words Table: {total}")
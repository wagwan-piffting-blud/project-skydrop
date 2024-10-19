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

names = ["Tobin", "China"] # M1 SPIRIT GUIDE COUNTRY NAME M2
names2 = ["43", "70"]

codebook = load_codebook()
codebook2 = load_codebook2()

def find_fuzzy_matches(names, codebook, threshold=100):
    matches = {}
    for name in names:
        processed_name = re.sub(r'\b(Mount|Mountain|Peak|Dome)\b', '', name, flags=re.IGNORECASE).strip()
        for codebook_name, entry in codebook.items():
            processed_codebook_name = re.sub(r'\b(Mount|Mountain|Peak|Dome)\b', '', codebook_name, flags=re.IGNORECASE).strip()
            score = fuzz.ratio(processed_name.lower(), processed_codebook_name.lower())
            if score >= threshold:
                matches[processed_codebook_name] = entry
    return matches

def find_fuzzy_matches2(names, codebook):
    matches = {}
    for name in names:
        for codebook_name, entry in codebook.items():
            if name == ''.join(map(str, entry)) or name == codebook_name:
                matches[codebook_name] = entry
    return matches

matches = find_fuzzy_matches(names, codebook)
matches = list(matches.items())

for idx, namecoord in enumerate(matches):
    print(f"Index #{idx}: {namecoord[0]} ({namecoord[1][0]})")

print("-" * 120)

matches2 = find_fuzzy_matches2(names2, codebook2)
matches2 = list(matches2.items())
natch = {}

for idx, namecoord in enumerate(matches2):
    print(f"Index #{idx}: {namecoord[0]} ({namecoord[1][0]})")
    if(names2[0] == ''.join(map(str, namecoord[1]))):
        natch[1] = namecoord[1][0]
    elif(names2[1] == ''.join(map(str, namecoord[1]))):
        natch[0] = namecoord[1][0]

try:
    print(f"\nLat: {int(natch[0])}.{int(''.join(map(str, matches[0][1])))}{int(''.join(map(str, matches[0][2])))}, Lon: -{int(natch[1])}.{int(''.join(map(str, matches[1][1])))}{int(''.join(map(str, matches[1][2])))}")
except Exception:
    print(f"\nLat: {int(natch[0])}.{int(''.join(map(str, matches[0][1])))}, Lon: -{int(natch[1])}.{int(''.join(map(str, matches[1][1])))}")
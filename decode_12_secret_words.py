import sys
import nltk
import asyncio
import threading
import itertools
import pandas as pd
from tqdm import tqdm
from math import factorial
from nltk.corpus import words as NLTKWords
from multiprocessing import Process, freeze_support
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = 1
WORD_LIST = "scroll_12_words.txt" # Or "bounty_12_words.txt" for Bounty/Final Puzzle
CODE_BOOK = "scroll.htm" # Or bounty.htm for Bounty/Final Puzzle

try:
    nltk.download('words')
except Exception as e:
    print(e)

english_words = set(NLTKWords.words())

with open("__WORDLISTFOUND2__.txt", 'w') as my_file:
    my_file.write("Start!\n\n\n")
    
def save_state(chunk_index, perm_index):
    with open("state2.txt", "w") as f:
        f.write(f"{chunk_index},{perm_index}")

def load_state():
    try:
        with open("state2.txt", "r") as f:
            chunk_index, perm_index = map(int, f.read().split(","))
        return chunk_index, perm_index
    except FileNotFoundError:
        return 0, 0

def load_codebook():
    codebook_df = pd.read_html(CODE_BOOK, header=0)[0]
    codebook = codebook_df.set_index('Word').T.to_dict('list')
    return codebook

def decode_words_pandas(words, codebook):
    decoded_values = []
    for i, word in enumerate(words):
        if word.lower() in codebook:
            decoded_values.append(codebook[word.lower()])
        else:
            decoded_values.append(f": Word '{word}' not found in codebook")

    return decoded_values

def runner(combined_msg):
    found_words = []
    
    for i in range(len(combined_msg)):
        for j in range(i + 4, len(combined_msg) + 1):
            word = combined_msg[i:j].lower()
            if word in english_words and len(word) > 4:
                found_words.append(word)
    return found_words

def find_english_words(decoded_values):
    num_columns = 21
    combined_msg = ""
    
    for col in range(0, num_columns):
        for row in range(0, num_columns):
            try:
                combined_msg += ''.join([values[row][col] for values in decoded_values])
            except IndexError:
                break
    found_words = runner(combined_msg)
    return found_words

def process_permutation(words, codebook, my_file):
    decoded_values = decode_words_pandas(words, codebook)
    found_words = find_english_words(decoded_values)
    
    num_columns = 21
    combined_msg = ""
    
    for col in range(0, num_columns):
        for row in range(0, num_columns):
          try:
            combined_msg += decoded_values[row][col] 
            if combined_msg.startswith('***'):
              full_strings.append(combined_msg)
              break
          except IndexError:
            break
    
    output = ""
    output += "Words: " + str(words) + "\n\n"
    output += "Decoded Values: " + str(decoded_values) + "\n\n"
    output += "As fully-formed string: " + combined_msg + "\n\n"
    output += "Found English Words: " + str(found_words) + "\n\n" + ("-" * 90)
    
    if(len(found_words) > 2):
        with open("__WORDLISTFOUND2__.txt", 'w') as my_file:
            my_file.write(str(found_words) + str(words))
            my_file.close()
    
    tqdm.write(output)
    asyncio.get_running_loop().stop()
    
    return output;

with open(WORD_LIST, 'r') as f:
    all_words = [line.strip() for line in f]

def process_wordlist(wordlist, chunk_size=12):
    for i in range(0, len(wordlist), chunk_size):
        yield wordlist[i:i + chunk_size]

codebook = load_codebook()

async def async_process_permutation(executor, perm):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, process_permutation, perm, codebook, my_file)

total_permutations_len = factorial(len(all_words)) // factorial(len(all_words) - 12)

async def main():
    chunk_index, perm_index = load_state()

    for i, chunk in enumerate(process_wordlist(all_words)):
        if i < chunk_index:
            continue

        all_permutes = itertools.permutations(chunk, 12)
        perm_count = factorial(12)

        for j in range(0, perm_count, MAX_WORKERS):
            if i == chunk_index and j < perm_index:
                continue

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                with tqdm(desc="Processing permutations", position=0, total=total_permutations_len) as pbar:
                    tasks = []
                    for perm in itertools.islice(all_permutes, MAX_WORKERS):
                        task = asyncio.ensure_future(async_process_permutation(executor, perm))
                        tasks.append(task)
                        pbar.update(perm_index)

                    results = await asyncio.gather(*tasks)
                    for result in results:
                        print(result)

            perm_index = j + MAX_WORKERS
            save_state(i, perm_index)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        sys.exit()
    except Exception as e2:
        tqdm.write(e2)
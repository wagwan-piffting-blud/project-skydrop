#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import ast
import csv
import sys
import time
import nltk
import random
import asyncio
import argparse
import mnemonic
import requests
import itertools
import threading
import bip32utils
import pandas as pd
from tqdm import tqdm
from io import StringIO
from math import factorial
from fuzzywuzzy import fuzz
from operator import itemgetter
from nltk.corpus import words as NLTKWords
from multiprocessing import Process, freeze_support
from concurrent.futures import ThreadPoolExecutor, as_completed

parser = argparse.ArgumentParser(description="Project Skydrop Scripts by Wags", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--version', action='version', version='1.0.2')
args = parser.parse_args()
config = vars(args)

def decode_12_secret_words(file):
    MAX_WORKERS = 1
    WORD_LIST = f"{file}.txt"
    CODE_BOOK = f"{file}.htm"

    try:
        nltk.download('words', quiet=True)
    except Exception as e:
        print(e)

    english_words = set(NLTKWords.words())

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

    def process_permutation(words, codebook):
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
        
        print(output)

    with open(WORD_LIST, 'r') as f:
        all_words = [line.strip() for line in f]

    def process_wordlist(wordlist, chunk_size=12):
        for i in range(0, len(wordlist), chunk_size):
            yield wordlist[i:i + chunk_size]

    codebook = load_codebook()
    
    def main():
        process_permutation(all_words, codebook)
    
    try:
        main()
    except KeyboardInterrupt:
        raise KeyboardInterrupt

def decode_base_3():
    def decode_base3_to_ascii_long(base3_string):
      if "?" not in base3_string:
        decimal_value = int(base3_string, 3)
        print("\nDEC: " + str(decimal_value))
        hex_string = hex(decimal_value)[2:]
        print("\nHEX: " + str(hex_string))

        decoded_string = ""
        for i in range(0, len(hex_string), 2):
          hex_pair = hex_string[i:i+2]
          try:
            decoded_string += chr(int(hex_pair, 16))
          except ValueError:
            decoded_string += "?"
        return [decoded_string]

      else:
            decoded_strings = []
            for digit in "012":
                temp_string = base3_string.replace("?", digit)

                decimal_value = int(temp_string, 3)
                print(f"\nDEC (PERMUTE #{str(int(digit) + 1)}): " + str(decimal_value))
                hex_string = hex(decimal_value)[2:]
                print(f"\nHEX (PERMUTE #{str(int(digit) + 1)}): " + str(hex_string))

                decoded_string = ""
                for i in range(0, len(hex_string), 2):
                    hex_pair = hex_string[i:i + 2]
                    try:
                        decoded_string += chr(int(hex_pair, 16))
                    except ValueError:
                        decoded_string += "?"
                print(f"\nFINAL (PERMUTE #{str(int(digit) + 1)}): " + decoded_string)
                decoded_strings.append(decoded_string)
            return decoded_strings

    while True:
        SEQU = input("Paste your base-3 here, or type \"exit\" to exit back to the main menu: ")
        if SEQU == "exit":
            raise KeyboardInterrupt
        print("STRING: " + str(SEQU))
        final = decode_base3_to_ascii_long(SEQU)

        if isinstance(final, list) and len(final) > 1:
            pass
        else:
            print("\nFINAL: " + final[0])
        print("\n" + "-" * 80 + "\n")

def decode_linear_a():
    def linear_a_to_plaintext(text):
        linear_a_dict = {
            "𐚐": "A",
            "𐘉": "B",
            "𐚶": "C",
            "𐛘": "D",
            "𐘪": "E",
            "𐜩": "F",
            "𐙧": "G",
            "𐝅": "H",
            "𐚜": "I",
            "𐙵": "J",
            "𐙃": "K",
            "𐙰": "L",
            "𐙱": "M",
            "𐚙": "N",
            "𐘋": "O",
            "𐚌": "P",
            "𐘚": "Q",
            "𐙀": "R",
            "𐘫": "S",
            "𐙛": "T",
            "𐚃": "U",
            "𐛃": "V",
            "𐙡": "W",
            "𐘴": "X",
            "𐘦": "Y",
            "𐛉": "Z"
        }

        translated_text = "".join([linear_a_dict.get(char, char) for char in text])
        return translated_text

    def decrypt(ciphertext):
        plaintext = ""
        order = [0, 3, 6, 8, 7, 1, 4, 5, 2]
        indices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '$', '!', '@']

        num_cycles = len(ciphertext) // 108

        cipher2 = ""
        
        for myind in indices:
            for idx, letter in enumerate(ciphertext):
                wrapped_index = (ciphertext.index(myind) + idx * 12) % len(ciphertext)
                cipher2 += ciphertext[wrapped_index]
            heartbeat = ''
        
            for idx1 in order:
                heartbeat += cipher2[idx1]
            idx1 = 0
            
            print(''.join(heartbeat).replace('$', '10').replace('!', '11').replace('@', '12'))
            
            cipher2 = ""

    original = "8𐙛𐙀𐚜__𐙛__𐘪𐛘__7𐚐𐙀𐘋__𐚶𐚙_𐙧𐙧_𐜩6𐘉𐚙𐚐_𐙀𐘋𐘪_𐚐𐘫𐙛_5𐙀𐙃𐝅𐘦𐙰𐚃𐚐𐙰_𐚐_𐚐4𐘫𐘋𐘪@𐛘𐚜𐘪_𐚐𐙰__3𐙀𐙛𐚶!𐙀𐘪𐘪𐚶_𐙰__2𐚙_𐚶$𐚙𐙛𐙀_𐙀𐚶_𐙡1𐚃_𐚙9𐚐𐘪𐚜𐘦_𐙛_𐚃𐙃𐙀_𐙀"
    print(f"ORIGINAL: {original}")

    ciphertext = linear_a_to_plaintext(original)
    print(f"\nLINEAR-A DECODE: {ciphertext}\n")

    print("12 SECRET WORDS IN ORDER AFTER USING X58167243 ALGO:")
    decrypt(ciphertext)

def locate_coords(file, names, names2):
    CODE_BOOK = f"{file}.htm"

    def load_codebook():
        codebook_df = pd.read_html(CODE_BOOK, header=0)[1]
        codebook = codebook_df.drop_duplicates('Word').set_index('Word').T.to_dict('list')
        return codebook

    def load_codebook2():
        codebook_df = pd.read_html(CODE_BOOK, header=0)[2]
        codebook = codebook_df.drop_duplicates('Word').set_index('Word').T.to_dict('list')
        return codebook

    def csv_string_to_list(csv_string):
        f = StringIO(csv_string)
        reader = csv.reader(f, delimiter=',')
        return list(reader)[0]

    codebook = load_codebook()
    codebook2 = load_codebook2()
    
    names = csv_string_to_list(names)
    names2 = csv_string_to_list(names2)
    
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
            natch[0] = namecoord[1][0]
        elif(names2[1] == ''.join(map(str, namecoord[1]))):
            natch[1] = namecoord[1][0]

    try:
        print(f"\nLat: {int(natch[0])}.{int(''.join(map(str, matches[0][1])))}{int(''.join(map(str, matches[0][2])))}, Lon: -{int(natch[1])}.{int(''.join(map(str, matches[1][1])))}{int(''.join(map(str, matches[1][2])))}")
    except Exception:
        print(f"\nLat: {int(natch[0])}.{int(''.join(map(str, matches[0][1])))}, Lon: -{int(natch[1])}.{int(''.join(map(str, matches[1][1])))}")

def recover_wallet(file):
    N_TX = 1
    MAX_WORKERS = 8

    async def asyncio_sleep(delay):
        await asyncio.sleep(delay)

    def generate_mnemonic():
        mnemo = mnemonic.Mnemonic("english")
        return mnemo.generate(strength=128)

    def recover_wallet_from_mnemonic(mnemonic_phrase):
        seed = mnemonic.Mnemonic.to_seed(mnemonic_phrase)
        root_key = bip32utils.BIP32Key.fromEntropy(seed)
        child_key = root_key.ChildKey(44 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)  

        address = child_key.Address()  

        balance, ntx = check_BTC_balance(address)
        return mnemonic_phrase, balance, address, ntx

    def check_BTC_balance(address, retries=3, delay=5):
        for attempt in range(retries):
            try:
                response = requests.get(f"https://blockchain.info/balance?active={address}", timeout=10)
                response.raise_for_status()
                data = response.json()
                balance = data[address]["final_balance"]
                ntx = data[address]["n_tx"]
                return balance / 100000000, ntx
            except requests.RequestException as e:
                if attempt < retries - 1:
                    print(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                    asyncio.run(asyncio_sleep(delay))
                else:
                    print("Error checking balance: %s", str(e))
        return 0, 0

    def is_str_a_list(s):
        if s.startswith('[') and s.endswith(']'):
            s = re.sub(r'(?<=\[|,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=,|\])', r'"\1"', s)
            try:
                parsed = ast.literal_eval(s)
                return isinstance(parsed, list)
            except (ValueError, SyntaxError):
                return False
        return False

    def check_mnemonic(full_mnemonic):
        asyncio.run(asyncio_sleep(random.random()))
        mnemonic_phrase, balance, address, ntx = recover_wallet_from_mnemonic(full_mnemonic)
        print(f"Trying mnemonic phrase: {full_mnemonic}")
        print(f"Wallet Address: {address}, Balance: {balance} BTC, Number of Transactions: {ntx}")
        if balance > 0 or ntx > N_TX:
            print(f"Found wallet with non-zero balance or more than {N_TX} transactions: {balance} BTC")
            with open("wallet.txt", "a") as f:
                f.write(f"Mnemonic Phrase: {mnemonic_phrase}\n")
                f.write(f"Wallet Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n\n")
                f.write(f"Number of Transactions: {ntx}\n\n")
        return mnemonic_phrase, balance, address, ntx

    def recover_wallet_from_partial_mnemonic(partial_mnemonic):
        partial_mnemonic_words = re.findall(r'\[.*?\]|\S+', partial_mnemonic)
        
        wordlist = mnemonic.Mnemonic("english").wordlist

        known_words = {}
        missing_positions = []
        i = 0
        while i < len(partial_mnemonic_words):
            word = partial_mnemonic_words[i]
            try:
                position = int(word)
                if 0 < position <= 12:
                    next_word = partial_mnemonic_words[i + 1]
                    if next_word.startswith("[") and next_word.endswith("]"):
                        try:
                            known_words[position - 1] = eval(next_word)
                            i += 2
                        except:
                            known_words[position - 1] = next_word
                            i += 2
                    else:
                        known_words[position - 1] = next_word
                        i += 2
                else:
                    known_words[i] = word
                    i += 1
            except ValueError:
                known_words[i] = word
                i += 1
        for i in range(12):
            if i not in known_words:
                missing_positions.append(i)
        
        provided_words = len(known_words)
        missing_words = len(missing_positions)
        print(f"\nAttempting to recover wallet from {provided_words} words. Missing {missing_words} words.")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []

            for guess_tuple in itertools.product(
                *(
                    known_words.get(pos, wordlist)
                    if isinstance(known_words.get(pos), list)
                    else [known_words.get(pos)]
                    if pos in known_words
                    else wordlist
                    for pos in range(12)
                )
            ):
                flattened_guess = []
                idx = -1
                for idx, item in enumerate(guess_tuple):
                    idx += 1
                    if(is_str_a_list(item)):
                        for item2 in eval(re.sub(r'(?<=\[|,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=,|\])', r'"\1"', item)):
                            flattened_guess.append(item2)
                            
                    else:
                        flattened_guess.append(item)
                full_mnemonic = " ".join(flattened_guess)
                
                future = executor.submit(check_mnemonic, full_mnemonic)
                futures.append(future)

            for future in as_completed(futures):
                mnemonic_phrase, balance, address, ntx = future.result()
                if balance > 0 or ntx > N_TX:
                    return mnemonic_phrase, balance, address, ntx 
        return None, 0, None

    def main(file):
        partial_mnemonic = file
        recover_wallet_from_partial_mnemonic(partial_mnemonic)
    
    try:
        main(file)
    except KeyboardInterrupt:
        raise KeyboardInterrupt

def main(runopt, file):
    match int(runopt):
        case 1:
            decode_12_secret_words(file)
        case 2:
            decode_base_3()
        case 3:
            decode_linear_a()
        case 4:
            names = input("What NAMES do you wish to find in the Secret Words table (in CSV format with NO SPACES, ex. `Tobin,China`)? ")
            names2 = input("What NUMBERS do you wish to find in the Secret Words table (in CSV format with NO SPACES, ex. `43,70`)? ")
            locate_coords(file, names, names2)
        case 5:
            with open(file + ".txt", 'r') as f:
                words = [line.strip() for line in f]
            indexed_words = [f"{i} {word}" for i, word in enumerate(words, 1)]
            file = " ".join(indexed_words)
            recover_wallet(file)

if __name__ == '__main__':
    print("""
  _____           _           _      _____ _              _                    _____           _       _       
 |  __ \\         (_)         | |    / ____| |            | |                  / ____|         (_)     | |      
 | |__) _ __ ___  _  ___  ___| |_  | (___ | | ___   _  __| |_ __ ___  _ __   | (___   ___ _ __ _ _ __ | |_ ___ 
 |  ___| '__/ _ \\| |/ _ \\/ __| __|  \\___ \\| |/ | | | |/ _` | '__/ _ \\| '_ \\   \\___ \\ / __| '__| | '_ \\| __/ __|
 | |   | | | (_) | |  __| (__| |_   ____) |   <| |_| | (_| | | | (_) | |_) |  ____) | (__| |  | | |_) | |_\\__ \\
 |_|   |_|  \\___/| |\\___|\\___|\\__| |_____/|_|\\_\\\\__, |\\__,_|_|  \\___/| .__/  |_____/ \\___|_|  |_| .__/ \\__|___/
                _/ |                             __/ |               | |                        | |            
               |__/                             |___/                |_|                        |_|            

Welcome to the Project Skydrop Scripts runner by Wags. This contains all of the scripts in the GitHub repository in one centralized file for ease of use and access.

Directory of Scripts:

1. Decode 12 Secret Words
2. Decode Base 3
3. Decode Linear A
4. Locate Coords
5. Recover Bitcoin Wallet

You can pick which codebook you wish to run against as well (either 'bounty', AKA Final Puzzle, or 'scroll', AKA Final Final Puzzle).

So, with that all being said...
""")
    
    while True:
        try:
            runopt = input("\n\n\nWhich script do you wish to run? (1-5, or \"exit\" to exit) ")
            if runopt == "exit":
                raise ValueError
            elif(int(runopt) == 1 or int(runopt) == 4 or int(runopt) == 5):
                file = input("Which file do you wish to run against? (bounty/scroll) ")
            else:
                file = ""
            main(runopt, file)
        except KeyboardInterrupt:
            runopt = input("\n\n\nWhich script do you wish to run? (1-5, or \"exit\" to exit) ")
            if runopt == "exit":
                raise ValueError
            elif(int(runopt) == 1 or int(runopt) == 4 or int(runopt) == 5):
                file = input("Which file do you wish to run against? (bounty/scroll) ")
            else:
                file = ""
            main(runopt, file)
        except ValueError:
            sys.exit()
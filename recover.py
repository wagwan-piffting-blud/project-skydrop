# Script originally from https://github.com/MinightDev/BTC-Wallet-Recover with some modifications for our purposes

import re
import os
import sys
import ast
import time
import random
import logging
import asyncio
import mnemonic
import requests
import itertools
import bip32utils
from concurrent.futures import ThreadPoolExecutor, as_completed

N_TX = 1
MAX_WORKERS = 8
CHECKPOINT_FILE = "checkpoint.txt"

async def asyncio_sleep(delay):
    await asyncio.sleep(delay)

def save_checkpoint(last_guess):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(last_guess)

def load_checkpoint():
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return f.readline().strip()
    except FileNotFoundError:
        return None

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
                logging.error(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                asyncio.run(asyncio_sleep(delay))
            else:
                logging.error("Error checking balance: %s", str(e))
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
    logging.info(f"Trying mnemonic phrase: {full_mnemonic}")
    logging.info(f"Wallet Address: {address}, Balance: {balance} BTC, Number of Transactions: {ntx}")
    if balance > 0 or ntx > N_TX:
        logging.info(f"Found wallet with non-zero balance or more than {N_TX} transactions: {balance} BTC")
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
    logging.info(f"Attempting to recover wallet from {provided_words} words. Missing {missing_words} words.")
    
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
            
            save_checkpoint(" ".join(flattened_guess))

        for future in as_completed(futures):
            mnemonic_phrase, balance, address, ntx = future.result()
            if balance > 0 or ntx > N_TX:
                return mnemonic_phrase, balance, address, ntx 

    logging.info("No wallet found with the provided partial mnemonic phrase.")
    return None, 0, None

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # partial_mnemonic = "1 century 2 throw 3 task 4 corn 5 library 6 liar 7 artefact 8 seat 9 general 10 daring 11 reduce 12 unlock" # Bounty words
    partial_mnemonic = "1 half 2 acquire 3 annual 4 label 5 sniff 6 velvet 7 zero 8 estate 9 wasp 10 acoustic 11 rose 12 click" # Scroll words
    recover_wallet_from_partial_mnemonic(partial_mnemonic)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
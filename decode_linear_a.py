import sys

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

sys.exit()
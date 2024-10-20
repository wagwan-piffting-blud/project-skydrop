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

"""
Some example strings to try:

0100202220121212 - Coin

2011102202012022211110222010221010002222121111002200222220222011122001010001011100022221010211220202 - Trophy 2nd Big Ring, Row/Message 1

2011201120212210000101111111010110010101002020202100110122221112211120210001210011111212021212000200 - Trophy 2nd Big Ring, Row/Message 2

1201211022111001002102010212102222010102001000220022200100210021220102210220012002021121002112020112 - Trophy 2nd Big Ring, Row/Message 3

"""

while True:
    SEQU = input("Paste your base-3 here: ")
    print("STRING: " + str(SEQU))
    final = decode_base3_to_ascii_long(SEQU)

    if isinstance(final, list) and len(final) > 1:
        pass
    else:
        print("\nFINAL: " + final[0])
    print("\n" + "-" * 80 + "\n")
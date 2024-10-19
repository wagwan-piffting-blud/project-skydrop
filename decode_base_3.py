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

SEQU = input("Paste your base-3 here: ")
triplet = SEQU
print("STRING: " + str(triplet))
final = decode_base3_to_ascii_long(triplet)

if isinstance(final, list) and len(final) > 1:
    pass
else:
    print("\nFINAL: " + final[0])
print("\n" + "-" * 80 + "\n")
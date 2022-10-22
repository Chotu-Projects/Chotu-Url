import hashlib
from os import getenv
from dotenv import load_dotenv


load_dotenv()

base58_symbol_chart = [
    '1', '2', '3', '4', '5',
    '6', '7', '8', '9', 'A',
    'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'J', 'K', 'L',
    'M', 'N', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z', 'a', 'b',
    'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'm',
    'n', 'o', 'p', 'q', 'r',
    's', 't', 'u', 'v', 'w',
    'x', 'y', 'z']

SALT = getenv("SALT")

hashes = []
duplicates = {}

for i in range(58):
    print(f"i : {i}")
    for j in range(58):
        for k in range(58):
            c1 = base58_symbol_chart[i]
            c2 = base58_symbol_chart[j]
            c3 = base58_symbol_chart[k]

            string = c1 + c2 + c3 + SALT
            hash_string = int.from_bytes(hashlib.sha512(string.encode('utf-8')).digest()[:4], byteorder='little')

            if hash_string in hashes:
                if hash_string in duplicates.keys():
                    duplicates[hash_string] += 1
                else:
                    duplicates[hash_string] = 1
            else:
                hashes.append(hash_string)

print("DONE")
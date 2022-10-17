import random
import cryptocode

def base58(salt:str) -> str:
    """
    Generates a random 3 bytes long
    BASE58 string
    """
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
    
    url_str = "".join(random.sample(base58_symbol_chart, k=3))

    hashed_str = hash_chotu(url_str, salt)

    return url_str, hashed_str


def hash_chotu(url_str:str, salt:str) -> int:
    print(salt + url_str)
    return hash(salt + url_str) % (10 ** 9)


def encrypt(chotu:str, salt:str, original_url:str) -> str:
    encrypted_url = cryptocode.encrypt(original_url, chotu + salt)
    return encrypted_url


def decrypt(chotu:str, salt:str, encrypted_url:str) -> str:
    original_url = cryptocode.decrypt(encrypted_url, chotu + salt)
    return original_url

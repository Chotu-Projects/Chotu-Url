import random

def base58():
    base58_symbol_chart = {
        0: '1',
        1: '2',
        2: '3',
        3: '4',
        4: '5',
        5: '6',
        6: '7',
        7: '8',
        8: '9',
        9: 'A',
        10: 'B',
        11: 'C',
        12: 'D',
        13: 'E',
        14: 'F',
        15: 'G',
        16: 'H',
        17: 'J',
        18: 'K',
        19: 'L',
        20: 'M',
        21: 'N',
        22: 'P',
        23: 'Q',
        24: 'R',
        25: 'S',
        26: 'T',
        27: 'U',
        28: 'V',
        29: 'W',
        30: 'X',
        31: 'Y',
        32: 'Z',
        33: 'a',
        34: 'b',
        35: 'c',
        36: 'd',
        37: 'e',
        38: 'f',
        39: 'g',
        40: 'h',
        41: 'i',
        42: 'j',
        43: 'k',
        44: 'm',
        45: 'n',
        46: 'o',
        47: 'p',
        48: 'q',
        49: 'r',
        50: 's',
        51: 't',
        52: 'u',
        53: 'v',
        54: 'w',
        55: 'x',
        56: 'y',
        57: 'z'
    }

    url_str = ""
    A, B, C = random.sample(range(0, 58), k=3)
    url_str += base58_symbol_chart[A]
    url_str += base58_symbol_chart[B]
    url_str += base58_symbol_chart[C]

    return url_str


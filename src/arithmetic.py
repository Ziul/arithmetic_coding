import ipdb
from math import e, log2, ceil
from multiprocessing.pool import ThreadPool
from scipy.integrate import quad
from decimal import *
import numpy as np
from collections import Counter
from sys import argv, stdout
from arithmeticargs import _parser
from pprint import pformat, pprint

_MAX_THREADS = 10
_PRECISION = 3
_ATOL = 1 / 10**_PRECISION
_pool = ThreadPool(processes=_MAX_THREADS)


class Float(float):
    """docstring for Float"""

    def __init__(self, arg):
        super(Float, self).__init__()
        self.decimal = self.real % 1


def laplacian(x, b=1.0):
    try:
        return 1 / (2 * b) * e**(-(abs(x) / b))
    except ZeroDivisionError:
        # lim(x->0) 0.5 * b * e**(-(abs(x) / b)) = 0.5*b (not fails)
        # lim(b->0) 0.5 * b * e**(-(abs(x) / b)) = do not have, comes to 0 from
        # the positive side. -Inf from negative side.
        raise


def integrate(b=1):
    # return the integral from laplacian with especifc `b`
    return quad(laplacian, -np.inf, np.inf, args=(b))


def encode(word, symbols):
    """
    Symbols shold come as dictionarry of list od two  elements, like:
    dict[symbol] = [low, hight]

    Word is the text to be encoded.

    low and high means the values of each symbol in the probability.
    """

    low = 0.0
    high = 1.0
    word = list(word)
    word.reverse()

    while(len(word)):
        symbol = word.pop()
        code_range = high - low
        high = low + code_range * symbols[symbol][1]
        low = low + code_range * symbols[symbol][0]

    return low


def decode(number, symbols):
    word = ''
    snumber = str(number)
    while not np.isclose(number, 0, atol=_ATOL):
        for key in symbols:
            if symbols[key][0] <= number < symbols[key][1]:
                # output the symbol
                if type(key) == int:
                    word += chr(key)
                else:
                    word += key
                _range = symbols[key][1] - symbols[key][0]
                # subtract symbol from encoded
                number -= symbols[key][0]
                # number = number % 1
                # divide encoded by range
                number /= _range
                snumber = snumber[1:]
                break
        if not len(word):
            raise Exception('Range not found')
    return word


def get_range(p_x, range_min_precessor=0):
    return [round(range_min_precessor, _PRECISION),
            round(range_min_precessor + p_x, _PRECISION)]
    # return [range_min_precessor, range_min_precessor + p_x]


def set_range(symbols):
    keys = list(symbols.keys())
    keys.sort()
    sym = {}
    sym[keys[0]] = [0.0, symbols[keys[0]]]

    for key in keys[1:]:
        sym[key] = get_range(symbols[key], sym[
                             keys[keys.index(key) - 1]][1])

    return sym


def set_probability(text):
    symb2freq = Counter(text)
    for key in symb2freq:
        symb2freq[key] = symb2freq[key] / len(text)
    return symb2freq


def main():
    (_options, _args) = _parser.parse_args()

    def print(data, end='\n'):
        # overwrite print
        if _options.verbose:
            stdout.write(str(data) + end)

    if not _options.filename:
        if len(argv) > 1:
            if _options.text:
                txt = _options.text
            else:
                # _options.filename = _args[0]
                txt = open(_args[0], "rb",).read()
        else:
            _parser.print_help()
            return

    sym = set_probability(txt)
    # print(1.0 - sum(sym.values()))
    sym = set_range(sym)
    if _options.verbose:
        pprint(sym, indent=4)
    result = encode(txt, sym)
    print("%1.95f" % result)
    print(decode(result, sym))

if __name__ == '__main__':
    main()

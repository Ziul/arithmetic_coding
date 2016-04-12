import ipdb
from math import e
from multiprocessing.pool import ThreadPool
from scipy.integrate import quad
import numpy as np
from collections import Counter
from sys import argv
from arithmeticargs import _parser

_MAX_THREADS = 10
_PRECISION = 2
_pool = ThreadPool(processes=_MAX_THREADS)


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


def get_range(p_x, range_min_precessor=0):
    # return [round(range_min_precessor, _PRECISION),
    # round(range_min_precessor + p_x, _PRECISION)]
    return [range_min_precessor, range_min_precessor + p_x]


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
    txt = ' '.join(_args)
    sym = set_probability(txt)
    # print(1.0 - sum(sym.values()))
    sym = set_range(sym)
    if _options.verbose:
        print(sym)
    result = encode(txt, sym)
    print("%1.95f" % result)
    # print(result)

if __name__ == '__main__':
    main()

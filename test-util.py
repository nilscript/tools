#!/usr/bin/env python

"""
Usage:
    test-util spread <n>
"""

import sys
from math import ceil
from docopt import docopt
from tabulate import tabulate

def spread(n):
    """
    Yields all numbers up to n not including n, by dividing n. 
    Generator is usefull for testing performance on applications which can take 
    integers continiously. The sequence of numbers will go from rough jumps to 
    finer and finer sequences so a test can be aborted but the result of the 
    test has balanced amount of data over the test range.
    """

    def __spread(n, yielded=[]):
        if n == 1:
            yield n
            return n
        else:
            yield n

        # Used to safeguard so no number gets printed more than once.
        # (This generator is not optimized to avoid these)
        yielded.append(n)
        for a in __spread(ceil(n / 2), yielded):

            if a not in yielded:
                yield a

            b = 2 * n - a
            if b < yielded[0] and b not in yielded:
                yield b

    return map(lambda n: n - 1, __spread(n))


if __name__ == '__main__':
 
 
    args = docopt(__doc__ + "\n" + 
        tabulate([["spread <n>", spread.__doc__]], tablefmt="plain"))

    if args["spread"]:
        for n in spread(int(args["<n>"])):
            print(n)

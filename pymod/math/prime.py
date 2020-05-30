#!/usr/bin/env python

"""
Usage: 
    prime floor         <n>
    prime ceil          <n>
    prime nth           <n> [--all]
    prime up-to         <n> [--all]
    prime is            <n>
    prime probable      <n> [<k>]
"""

import secrets
from random import randrange

import numpy as np
from docopt import docopt
from tabulate import tabulate
from textwrap import indent

def floor(n):
    """
    Returns the approximate lower limit of how big the nth prime could be.
    """
    return "TODO"  # TODO


def ceil(n):
    """
    Returns the approximate upper limit of how big the nth prime could be.
    Source: https://math.stackexchange.com/a/1259
    """
    if n <= 0:
        return 0
    elif n < 4:
        return [2, 3, 5][n-1]
    else:
        return np.ceil(n * np.log(n) + n * np.log(np.log(n)))


def nth(n):
    """
    Returns an array of primes where the nth prime can be indexed by n - 1.
    """

    return up_to(ceil(n) + 1)


def up_to(n):
    """
    Input n > 0, 
    Returns an array of primes between 2 (inclusive) and n (exclusive)
    Source: https://stackoverflow.com/a/3035188/10023360
    """

    if n <= 2:
        return []
    elif n == 3:
        return [2]
    else:
        sieve = np.ones(int(n//3 + (n % 6 == 2)), dtype=np.bool)
        for i in range(1, int(n**0.5)//3+1):
            if sieve[i]:
                k = 3*i+1 | 1
                sieve[k*k//3::2*k] = False
                sieve[k*(k-2*(i & 1)+4)//3::2*k] = False
        return list(np.r_[2, 3, ((3*np.nonzero(sieve)[0][1:]+1) | 1)])


def probable(n, k=10):
    """
    Returns true if n has not been proven to be a composit number and
    could be a prime.
    Returns false if n is proven to be a composit number.
    k is the number of rounds that n is tested
    Miller Rabin Test is non deterministic.
    Source: https://gist.github.com/bnlucas/5857478
    """
    # All negative integers (+ 0, 1) can't be a prime number (depending on who you ask)
    if n <= 1:
        return False

    # Edge cases
    elif n in [2, 3]:
        return True

    # All even numbers are composit to 2
    elif not n & 1:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for _ in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for _ in range(k):
        a = randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


if __name__ == '__main__':

    helper = tabulate([
        ["floor <n>", floor.__doc__],
        ["ceil <n>", ceil.__doc__],
        ["nth <n>", "Returns the nth prime. If option [--all] is present, also return all primes up to nth prime."],
        ["up-to <n> [--all]", "Returns the last prime before n (exclusive). If option[--all] is present, return all primes up to n."],
        ["is <n>", "Returns a boolean whether n is a prime or not."],
        ["probable", probable.__doc__]
    ], tablefmt="plain") + "\n\nBoolean options also exits with code (0 | 1)"
    
    args = docopt(__doc__ + "\nDescription:\n" + indent(helper, "    "))
    n = int(args["<n>"])

    if args["floor"]:
        print(floor(n))
    elif args["ceil"]:
        print(ceil(n))
    elif args["nth"]:
        if args["--all"]:
            print(nth(n)[:n])
        else:
            print(nth(n)[n-1])
    elif args["up-to"]:
        if args["--all"]:
            print(up_to(n))
        else:
            print(up_to(n)[-1])
    elif args["is"]:
        if n in up_to(n+1):
            print(True)
            exit(0)
        else:
            print(False)
            exit(1)
    elif args["probable"]:
        if args["<k>"]:
            print(probable(n, int(args["<k>"])))
            exit(0)

        else:
            print(probable(n))
            exit(1)

#!/usr/bin/env python3

"""
Usage:
    prime floor         <n>
    prime ceil          <n>
    prime nth           <n> [--all]
    prime upto          <n> [--all]
    prime exists        <n>
    prime probable      <n> [<k>]
"""

import secrets
import sys
from random import randrange
from textwrap import indent

import numpy as np
from docopt import docopt
from tabulate import tabulate


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
    Returns an list of primes where the nth prime is the last element.
    """

    return upto(ceil(n) + 1)[:n]


def upto(n):
    """
    Input n > 0,
    Returns an list of primes between 2 (inclusive) and n (exclusive)
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


def exists(n):
    """
    Returns true or false depending on if n is a prime
    """
    return n in upto(n+1)


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

    # Fix input + help
    helper = tabulate([
        ["floor <n>", floor.__doc__],
        ["ceil <n>", ceil.__doc__],
        ["nth <n>", "Returns the nth prime. If option [--all] is present, also return all primes up to nth prime."],
        ["upto <n> [--all]",
            "Returns the last prime before n (exclusive). If option[--all] is present, return all primes up to n."],
        ["exists <n>", "Returns a boolean whether n is a prime or not."],
        ["probable", probable.__doc__]
    ], tablefmt="plain") + "\n\nBoolean options also exits with code (0 | 1)"

    args = docopt(__doc__ + "\nDescription:\n" + indent(helper, "    "))

    # Fix fn args
    fn = globals().get(sys.argv[1])

    fn_argc = fn.__code__.co_argcount
    fn_argnames = fn.__code__.co_varnames[:fn_argc]

    str_args = ','.join(map(lambda s: args['<'+s+'>'], fn_argnames))

    # Main logic
    ans = eval(fn.__name__ + '(' + str_args + ')')

    # Print results:
    if isinstance(ans, list):
        if args["--all"]:
            print(ans)
        else:
            print(ans[-1])

    else:
        print(ans)

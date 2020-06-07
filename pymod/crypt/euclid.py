#!/usr/bin/env python3

"""
Euclidean algorithms. Or general algorithms applicable to cryptography.

Usage:
    euclid gcd <a> <b>
    euclid exgcd <a> <b>
    euclid lcm <a> <b>
    euclid phi <n>
    euclid crt <d1> <q1> <d2> <q2>
"""

import sys
from textwrap import indent

from docopt import docopt
from tabulate import tabulate


def gcd(a, b):
    """
    Euclid's algorithm. Returns the greatest common divider of a and b.
    """
    while b != 0:
        a, b = b, a % b

    return a


def exgcd(a, b):
    """
    Extended Euclidean algorithm. Return (g, x, y) such that g = a*x + b*y = gcd(a, b)
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def lcm(a, b):
    """
    Returns the least common multiple of a and b.
    """
    return a * b // gcd(a, b)


def phi(a):
    """
    Euler's totient function. Naive implementation
    """
    sum = 0
    for b in range(1, a + 1):
        if gcd(a, b) == 1:
            sum += 1
    return sum


# Something is not right here
# def crt(d1, q1, d2, q2):
#    """
#    Chinese Remainder Theorem. Returns the number when divided by d1 returns q1 and when divided by d2 returns q2.
#    """
#    (_, x, y) = exgcd(d1, d2)
#    m = d1 * d2
#    n = q2 * x * d1 + q1 * y * d2
#    return (n % m + m) % m


if __name__ == '__main__':
    helper = tabulate([
        ["gcd <a> <b>", gcd.__doc__],
        ["exgcd <a> <b>", exgcd.__doc__],
        ["lcm <a> <b>", lcm.__doc__],
        ["phi <n>", phi.__doc__],
        #["crt <d1> <q1> <d2> <q2>", crt.__doc__]
    ], tablefmt="plain")

    args = docopt(__doc__ + "\nDescription:\n" + indent(helper, "    ") +
                  "\nWill throw garbage errors if given garbage input")

    fn = globals().get(sys.argv[1])

    fn_argc = fn.__code__.co_argcount
    fn_argnames = fn.__code__.co_varnames[:fn_argc]

    str_args = ','.join(map(lambda s: args['<'+s+'>'], fn_argnames))
    print(eval(fn.__name__ + '(' + str_args + ')'))

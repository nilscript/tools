#!/usr/bin/env python

"""
Euclidean algorithms. Or general algorithms applicable to cryptography.

Usage:
    euclid gcd <a> <b>
    euclid ex-gcd <a> <b>
    euclid lcm <a> <b>
    euclid phi <a>
    euclid chi-rem <a> <b> <x> <y>

gcd <a> <b>                 Returns the greatest common divider of a and b.
ex-gcd <a> <b>              Return (g, x, y) such that a*x + b*y = g = gcd(a, b)
lcm <a> <b>                 Returns the least common multiple of a and b.
phi <n>                     Returns phi of a.
crt <a> <b> <x> <y>         Returns the chinese remained.

Will throw garbage errors if given garbage input.
"""

from docopt import docopt


def gcd(a, b):
    """
    Euclid's algorithm

    Returns the greatest common divider of a and b.
    """
    while b != 0:
        a, b = b, a % b

    return a


def ex_gcd(a, b):
    """
    Extended Euclidean algorithm

    Return (g, x, y) such that g = a*x + b*y = gcd(a, b)
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
    Euler's totient function

    Naive implementation
    """
    sum = 0
    for b in range(1, a + 1):
        if gcd(a, b) == 1:
            sum += 1
    return sum


def crt(n1, r1, n2, r2):
    """
    >>> crt(5,1,7,3)
    31
    Explanation : 31 is the smallest number such that
                (i)  When we divide it by 5, we get remainder 1
                (ii) When we divide it by 7, we get remainder 3
    >>> chinese_remainder_theorem(6,1,4,3)
    14
    """
    (_, x, y) = ex_gcd(n1, n2)
    m = n1 * n2
    n = r2 * x * n1 + r1 * y * n2
    return (n % m + m) % m


if __name__ == '__main__':
    args = docopt(__doc__)

    a = None
    b = None
    x = None
    y = None

    try:
        a = int(args["<a>"])
        b = int(args["<b>"])
        x = int(args["<x>"])
        y = int(args["<y>"])
    except:
        pass

    if args["gcd"]:
        print(gcd(a, b))
    elif args["ex-gcd"]:
        print(ex_gcd(a, b))
    elif args["lcm"]:
        print(lcm(a, b))
    elif args["phi"]:
        print(phi(a))
    elif args["crt"]:
        print(crt(a, b, x, y))

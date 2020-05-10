#!/usr/bin/env python

from euclid import gcd
import prime
import random
import sys
import numpy
import secrets

"""
This python program will generate rsa keys lossly following standard of
FIPS PUB 186-4.

It's written for academic purposes only and should not be used to generate
rsa keys as I am not a security expert. It's not properly seeded as it relies on
"random" for random numbers. It relies on Probable Primes rather than
Provable Primes.

Magic numbers and equations are sourced from
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
"""

"""SP 800-57, Part 1 (Page 53)"""
"""https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r4.pdf
"""
rsa_keylength_strength = {
    1024: 80,  # <= 80
    2048: 112,
    3072: 128,
    7680: 192,
    15360: 256
}
# Miller Rabin rounds table
MIN_MR_ROUNDS = {
    512: 5,
    1024: 5,
    2048: 4
}

# Miller Rabin minimum testing rounds same error probability of 2^-100
MIN_MR_ROUNDS_SAME_RISK = {
    512: 7,
    1024: 4,
    2048: 3
}


def probable_prime_pair(nlen, e):
    """
    Return 
    """

    if (nlen not in [2048, 3072] or
            e <= pow(2, 16) or
            e >= pow(2, 256) or
            e & 1 == 0
        ):
        return None

    MIN_KEY_LEN = numpy.sqrt(2) * pow(2, nlen/2 - 1)
    MIN_KEY_LEN_DIFF = pow(2, nlen / 2 - 100)
    MR_TEST_ROUNDS = MIN_MR_ROUNDS[nlen//2]

    i = 0
    max_iter = 5 * nlen / 2

    # Generate p
    p = 0
    while True:
        p = secrets.randbits(nlen//2) | 1

        if (p > MIN_KEY_LEN and
            gcd(p - 1, e) == 1 and
            prime.probable(p, MR_TEST_ROUNDS)
            ):
            break

        i += 1
        if i >= max_iter:
            return None

    # Generate q
    q = 0
    while True:
        q = secrets.randbits(nlen//2) | 1

        if (abs(p - q) > MIN_KEY_LEN_DIFF and
            q > MIN_KEY_LEN and
            gcd(q - 1, MR_TEST_ROUNDS) == 1 and
            prime.probable(q)
            ):
            break

        i += 1
        if i >= max_iter:
            return None

    return p, q


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

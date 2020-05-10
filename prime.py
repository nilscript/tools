"""
Usage: 
    prime floor         <n>
    prime ceil          <n>
    prime nth           <n> [--all]
    prime up-to         <n> [--all]
    prime is            <n>
    prime probable      <n> [<k>]

floor           <n>             Prints the approcimate lower limit of how big the nth prime could be.
ceil            <n>             Print the approximate upper limit of how big the nth prime could be.
nth             <n> [--all]     Print the nth prime. If option [--all] is present, print a list of all primes with size n.
up-to           <n> [--all]     Print the last prime before n (not including n). If option [--all] is present, print a list of all primes up to n.
is              <n>             Print a boolean (True | False) whether n is a prime or not. Also exits with code (0 | 1) where 0 is true and 1 is false.
probable    <n> [<k>]           Print a boolean (True | False) whether n remains an unproven prime or a proven coprime. Also exits with code (0 | 1) where 0 is true and 1 is false. k repeats the test, default value is 10. Algorithm used is Miller Rabin test.
"""

from docopt import docopt
import numpy as np
from random import randrange
import secrets



def floor(n):
    return "TODO"  # TODO


def ceil(n):
    """
    Input > 0, 
    Returns the approximate upper limit of how big the nth prime could be.
    https://math.stackexchange.com/a/1259
    """
    if n <= 0:
        return 0
    elif n < 4:
        return [2, 3, 5][n-1]
    else:
        return np.ceil(n * np.log(n) + n * np.log(np.log(n)))


def nth(n):
    """
    Input > 0,
    Returns an array of primes where the nth prime can be indexed by n - 1.
    """

    return up_to(ceil(n) + 1)


def up_to(n):
    """
    Input n > 0, 
    Returns an array of primes between 2 (inclusive) and n (exclusive)
    https://stackoverflow.com/a/3035188/10023360
    """

    if n <= 2:
        return []
    elif n == 3:
        return [2]
    else:
        sieve = np.ones(n//3 + (n % 6 == 2), dtype=np.bool)
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
    Miller Rabin Test is non deterministic.

    k is the number of rounds that n is tested

    https://gist.github.com/bnlucas/5857478

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
    args = docopt(__doc__)
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

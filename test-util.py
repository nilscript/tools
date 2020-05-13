#!/usr/bin/env python

"""
Usage:
    test-util spread <n>

spread <n>  Returns a sequen ce of unique numbers where the first number is as far apart from the previous number. 

"""

import sys
import numpy
import getopt
from docopt import docopt


def spread(n):
    """
    This function will generate all numbers inbetween start and stop
    (not including stop),
    Yields them not in order but as far apart from all previously
    yielded numbers.
    """

    # Used to safeguard so no number gets printed more than once.
    # (This generator is not optimized to avoid these)
    yielded = set([n-1])

    # Will only return after all numbers are yielded
    while len(yielded) != n:
        tail = 0

        # Will iterate from beginning to end over and over again
        # If something is yielded, then the medianvalue between tail and head
        # might not be
        for head in range(n):
            if head in yielded:
                median = (head + tail) // 2
                tail = head

                # Safeguard against recurring numbers
                if median not in yielded:
                    yielded.add(median)
                    yield median


if __name__ == '__main__':
    args = docopt(__doc__)

    if args["spread"]:
        for n in spread(int(args["<n>"])):
            print(n, end=" ")
        print()

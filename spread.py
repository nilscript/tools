#!/usr/bin/env python

import sys
import numpy
import getopt


def gen(items):
    items

    yielded = set()


def spread_gen(coarseness, start, stop):
    """
    This function will generate all numbers inbetween start and stop 
    (not including stop), 
    Yields them not in order but as far apart from all previously 
    yielded numbers.  
    """

    # Works by generating numbers in the range 0..size and then multiply them
    # and add a constant
    constant = start
    size = (stop - start) // coarseness + 1

    # Used to safeguard so no number gets printed more than once.
    # (This generator is not optimized to avoid these)
    yielded = numpy.full(size, False)
    yielded[-1] = True

    # Will only return after all numbers are yielded
    while False in yielded:
        tail = 0

        # Will iterate from beginning to end over and over again
        # If something is yielded, then the medianvalue between tail and head
        # might not be
        for head in range(size):
            if yielded[head] == True:
                median = (head + tail) // 2
                tail = head

                # Safeguard against recurring numbers
                if yielded[median] == False:
                    yield constant + median * coarseness
                    yielded[median] = True


if __name__ == '__main__':
    gen(range(10))

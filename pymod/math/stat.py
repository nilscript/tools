#!/usr/bin/env python

"""
Stat

Usage: 
    stat.py (mean|median|var|stddev) ([-]|--file=FILE|<input>...)
"""

import sys
from textwrap import indent

import scipy
from docopt import docopt
from numpy import floor, sqrt
from tabulate import tabulate


def mean(data):
    """
    Returns the average number by summing data.
    and dividing by the length of data.
    """
    return sum(data) / len(data)


def median(data):
    """
    Returns the middle value from a sorted list.
    If list has even number of elements return the average of the 2 middle numbers.
    """
    l = len(data)

    if l % 2 == 0:  # Is even
        x = int(floor(l / 2))
        return mean(data[x-1:x+1])

    else:  # Is odd
        return data[l // 2]


def var(data):
    """
    Returns the variance of data. 
    Variance is often written as 's^2'. 
    You probably want to use standard deviation instead.
    """
    avg = mean(data)
    return sum(map(lambda x: (x - avg) ** 2, data)) / (len(data) - 1)


def stddev(data):
    """
    Returns the standard deviation of data. Often written as 's'.
    """
    return sqrt(var(data))


def stats(data):
    """
    Prints information about data.
    """
    print("Mean:", mean(data))
    print("Median:", median(data))
    print("Sum:", sum(data))
    print("Var:", var(data))
    print("Std:", stddev(data))


def confidence_interval(data, level):

    avg = mean(data)
    l = len(data)
    a = stddev(data) / sqrt(l)

    t = scipy.stats.t.ppf(level, l - 1)

    return avg + t * a, avg - t * a


def goodness_of_fit():
    pass  # TODO


if __name__ == '__main__':

    # Fix input + help
    helper = tabulate([
        ["mean <data>", mean.__doc__],
        ["median <data>", median.__doc__],
        ["var <data>", var.__doc__],
        ["stddev <data>", stddev.__doc__]
    ], tablefmt="plain")

    args = docopt(__doc__ + "\nDescription:\n" + indent(helper, "    "))

    # Fix data:
    data = []

    if (args["--file"]):
        with args["--file"] as f:
            data = f.read().split()

    elif (args["<input>"]):
        data = args["<input>"]

    else:
        data = sys.stdin.read().split()

    data = list(map(int, data))

    # Main logic:
    print(eval(sys.argv[1] + "(" + str(data) + ")"))

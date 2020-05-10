"""
Stat

Usage: 
    stat.py (mean|median|variance|std-dev) ([-]|--file=FILE|<input>...)

"""

from numpy import sqrt, floor
import scipy
from docopt import docopt
import sys


def mean(data):
    """Average"""
    return sum(data) / len(data)


def median(data):
    """
    Returns the middle value from a sorted list.
    If list has even number of elements return the mean of the 2 middle numbers
    """
    l = len(data)

    if l % 2 == 0:  # Is even
        x = int(floor(l / 2))
        return mean(data[x-1:x+1])

    else:  # Is odd
        return data[l // 2]


def variance(data):
    """Variance. Ofter written as 's^2'. Rarely used"""
    avg = mean(data)
    return sum(map(lambda x: (x - avg) ** 2, data)) / (len(data) - 1)


def std_dev(data):
    """Standard Deviation. Often written as 's'"""
    return sqrt(variance(data))


def stats(data):
    """Prints information about data"""
    print("Mean:", mean(data))
    print("Median:", median(data))
    print("Sum:", sum(data))
    print("Var:", variance(data))
    print("Std:", std_dev(data))


def confidence_interval(data, level):

    avg = mean(data)
    l = len(data)
    a = std_dev(data) / sqrt(l)

    t = scipy.stats.t.ppf(level, l - 1)

    return avg + t * a, avg - t * a


def goodness_of_fit():
    pass  # TODO


if __name__ == '__main__':
    args = docopt(__doc__)

    data = []

    if (args["--file"]):
        with args["--file"] as f:
            data = f.read().split()

    elif (args["<input>"]):
        data = args["<input>"]

    else:
        data = sys.stdin.read().split()

    print(data)
    data = list(map(int, data))

    if (args["mean"]):
        print(mean(data))

    elif (args["median"]):
        print(median(data))

    elif (args["variance"]):
        print(variance(data))

    elif (args["std-dev"]):
        print(std_dev(data))

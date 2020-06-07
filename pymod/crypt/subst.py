#!/usr/bin/env python3

"""Substitution"""

from string import ascii_lowercase
from euclid import gcd
import re

def window(container, n):
    """
    Yields a sliding window iterating over all possible linear subslices
    of container with len(n).
    """
    for i in range(len(container) + 1 - n):
        yield container[i:i+n]


def find_keylength(crypt, n=3):
    """
    Returns a dictionary of potential keylengths for provided crypt text

    The lhs of an entry tells us the potential keylength while the rhs
    tells us how likely it is to be correct.

    The n variable determins the length of segments to check on the crypt
    text. The greater the segment the fewer
    and more likely keylenghts gets returned,
    but the longer it takes to compute
    """

    gcd_dict = {}

    for segment in set(window(crypt, n)): # Notice that set is used. We don't iterate over duplicated strings

        # If segment matches something, save where the match started to a list
        # Matches is a list of positions where common segments occur
        matches = [match.start() for match in re.finditer(segment, crypt)]

        # Calcylate the offsets between each matching segment
        offsets = [matches[i+1] - matches[i] for i in range(len(matches) - 1)]

        # Calcylate the gcd between each offset.
        gcds = [gcd(offsets[i], offsets[i+1]) for i in range(len(offsets) - 1)]

        # Count all gcds
        for g in gcds:
            gcd_dict[g] = gcd_dict.get(g, 0) + 1

    if n < 1 and len(gcd_dict) == 0:
        gcd_dict = find_keylength(crypt, n - 1)

    return gcd_dict

#! /usr/bin/env python
"""
# File: verify_pylint.py
#
# Author: Mike Lum
# Copyright 2021 by the author.
#
# Usage: python -m verify_pylint <min pylint score>
#
# Description: Runs pylint
#
# Revision History:
#    Date        Vers.    Author    Description
#   2021-08-06   1.0a1    Lum       New file
"""

import os
import sys

from collections import deque

DEFAULT_MIN_SCORE = 9.5
DEFAULT_OUTFILE = 'pylint.out'

def parse_out(outfile: str = DEFAULT_OUTFILE, min_score: float = DEFAULT_MIN_SCORE) -> float:
    """
    parse_out

    Parse the pylint results, looking for the score.

    Args:
        outfile (str): The name of the file containing the pylint results
        min_score (float): THe minimum score that we will accept

    Returns:
        result (float): The score from this pylint run

    Raises:
        None
    """
    fptr = open(outfile)
    try:
        result = float(fptr.readlines()[-2].split()[6].split('/')[0])
    except ValueError:
        print("Failure to obtain pylint result")
        sys.exit(1)

    if result < min_score:
        print("Pylint validation failed. Code score too low.")
        sys.exit(2)

    return result


if __name__ == '__main__':

    # Parse your command line call - Command line options ignored for now.
    ARGV = deque(sys.argv)

    # lose the function call
    ARGV.popleft()

    # Filename to check
    TEST_FILENAME = ARGV.popleft()

    PYLINT_COMM = 'pylint {0:s} >> {1:s}'.format(TEST_FILENAME, DEFAULT_OUTFILE)
    os.system(PYLINT_COMM)

    # Minimum acceptable PyLint score
    MIN_SCORE = DEFAULT_MIN_SCORE
    try:
        MIN_SCORE = float(ARGV.popleft())
    except ValueError:
        MIN_SCORE = DEFAULT_MIN_SCORE

    RESULT = parse_out(DEFAULT_OUTFILE, min_score=MIN_SCORE)

    if RESULT > MIN_SCORE:
        print("\t{0:s} - Passed pylint check. Score:{1:5.2f}".format(TEST_FILENAME, RESULT))

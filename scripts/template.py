#!/usr/bin/env python
"""Template script: Duplicate word n times.

Customize the framework below for your particular need.
"""

import argparse
import requests


def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Your script description (often top line of script's DocString; eg. Duplicate word n times)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Create a sequential argument (eg. it has to come in the order defined)
    parser.add_argument('word', # name of the argument, we will later use args.word to get this user input
                        metavar='WORD', # shorthand to represent the input value
                        help='Word to duplicate', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        default='Hello', # default option if no input is given by the user
                        required=False # whether this input must be given by the user, could also be True
                        )
    # Create a flagged argument (eg. input comes after a short "-i" or long "--input" form flag)
    parser.add_argument('-n', '--number', # name of the argument, we will later use args.number to get this user input
                        metavar='INT', # shorthand to represent the input value
                        help='Number of times to duplicate', # message to the user, it goes into the help menu
                        type=int, # type of input expected, could also be int or float
                        default=1, # default option if no input is given by the user
                        required=False # whether this input must be given by the user, could also be True
                        )

    return(parser.parse_args())


def name_of_function(word, n=1):
    """What the function does (eg. Return duplicated word.)"""

    # Do things with the parameters above
    # to get to defining the "thing" you will return
    duplicated_word = word * n

    return(duplicated_word)


if __name__ == "__main__":
    args = get_args()
    result = name_of_function(args.word, args.number)

    # Output the result
    print(result)

    # or just print the function if this is all we are doing:
    #print(name_of_function(args.word, args.number))
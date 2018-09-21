from __future__ import print_function # for 2.7 users
import pandas as pd
import argparse
import os
# need spaCy


# full-query extract function
def full_extract(file):

    # File operations
    source_file = os.path.basename(file)
    base = os.path.splitext(source_file)[0]


    """
    Source code goes here.
    Need to:
        1. Triage file types
        2. Collect into an object
        3. Create NLP object
        4. Extract likely entities
        5. Categorize findings
        6. Structure output
        7. Format and produce
    """


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='NEEDED')
    parser.add_argument("file", help="NEEDED")
    args = parser.parse_args()

    # run puppy, run
    full_extract(args.file)

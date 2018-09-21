import argparse # inorder to port to command line
import os # system controls
# import spaCy # NLP tooling to detect certain kinds of entities
# import pandas as pd # dataframe data structure for outputs


# main function call
def PIMINER(input_file):

    # file operations
    source_file = os.path.basename(input_file)
    base = os.path.splitext(source_file)[0]

    # read the input file and print content to sdtout
    file_object = open(source_file)
    for text_line in file_object:
        print(text_line)

if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='NEEDED')
    parser.add_argument("input_file", help="NEEDED")
    args = parser.parse_args()

    # run puppy, run
    PIMINER(args.input_file)

import argparse # inorder to port to command line
import os # system controls
import pandas as pd # dataframe data structure for outputs
import textract # used to parse PDF files
import spacy # industrial strength NLP engine
import re # string operations, mostly data cleaning

# load NLP library object
nlp = spacy.load('en_core_web_lg')

# main function call
def PIMINER(input_file):

    # file operations
    source_file = os.path.basename(input_file)
    base = os.path.splitext(source_file)[0]

    # create nlp object from input_file
    text = str(textract.process(source_file))
    doc = nlp(text)

    # test prints
    for ent in doc.ents:
        print(ent.text, ent.label_)


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='NEEDED')
    parser.add_argument("input_file", help="NEEDED")
    args = parser.parse_args()

    # run puppy, run
    PIMINER(args.input_file)

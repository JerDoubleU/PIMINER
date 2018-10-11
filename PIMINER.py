#!/usr/bin/env python

import argparse # inorder to port to command line
import os # system controls
import pandas as pd # dataframe data structure for outputs
import textract # used to parse PDF files
import spacy # industrial strength NLP engine
import re # string operations, mostly data cleaning
import subprocess # used to invoke shell scripts

# main function call
def PIMINER(input_file):

    model = 'en_core_web_lg'
    print('Loading spacy library: ' + str(model))

    # load NLP library object
    nlp = spacy.load(model)
    print('Library loaded successfully.')

    # file operations
    source_file = os.path.basename(input_file)
    base = os.path.splitext(source_file)[0]

    """
    need to make simple file handling more robust.
    it may be the case that this is better suited for another script,
    or should be called from main. TDB.

    possible to invoke shell cleaning script from this script like below:

    # # this code can trigger shell script cleaning operations
    # cleanFiles = 'text_cleaner.sh'
    # process = subprocess.Popen(cleanFiles.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()
    """

    print('Reading file: ' + str(source_file))
    # create nlp object from input_file
    text = str(textract.process(input_file))
    print('Read COMPLETE.')

    print('Converting file to spacy object: ' + str(source_file))
    doc = nlp(text)
    print('Convert COMPLETE.')

    print('Checking ' + str(base) + ' for phone numbers...')
    ## this is a check for possible phone numbers, saved to list
    ## Need to look for 9 digits phone numbers
    PHONE_NUMBER = re.compile('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
    PHONE_NUMBER_LIST = []

    for phone_match in re.finditer(PHONE_NUMBER, doc.text):
        if phone_match:
            PHONE_NUMBER_LIST.append("{}".format(phone_match.group(0)))
            # print("POSSIBLE PHONE NUMBER: {}".format(phone_match.group(0)))
    print('Phone number analysis COMPLETE.')

    print('Checking ' + str(source_file) + ' for email addresses...')
    ## this is a check for possible email addresses, saved to a list
    # EMAIL_ADDRESS = re.compile('[^@]+@[^@]+\.[^@]+')
    # EMAIL_ADDRESS_LIST = []
    #
    # for email_match in re.finditer(EMAIL_ADDRESS, doc.text):
    #     if email_match:
    #         PHONE_NUMBER_LIST.append("{}".format(email_match.group(0)))
    #         print("POSSIBLE EMAIL ADDRESS: {}".format(email_match.group(0)))
    print('Email addresses analysis COMPLETE.')

    """
    ## this is a list of spacy entities types
    ## that may be useful for tagging when checking for PII
    ## THIS LIST IS NOT EXHAUSTIVE
    """

    entity_types = ['PERSON', # People, including fictional.
                    'NORP', # Nationalities or religious or political groups.
                    'FAC', # Buildings, airports, highways, bridges, etc.
                    'ORG', # Companies, agencies, institutions, etc.
                    'GPE', # Countries, cities, states.
                    'LOC', # Non-GPE locations, mountain ranges, bodies of water.
                    'EVENT', # Named hurricanes, battles, wars, sports events, etc
                    'WORK_OF_ART', # Titles of books, songs, etc.
                    'LAW', # Named documents made into laws.
                    'DATE' # Absolute or relative dates or periods.
                    ]
    print('Checking ' + str(source_file) + ' for names, organizations, and dates...')
    ENTITY_LIST = []
    # print out detected named entities
    for entity in doc.ents:

        # for now, limit output to the entity types in the list above
        if entity.label_ in entity_types:
            ENTITY_LIST.append(str(entity.label_).upper() + ": " + str(entity.text))
            # print('POSSIBLE ' + str(entity.label_).upper() + ": " + str(entity.text))

    # # iteration through file and print noun chunks
    # for chunk in doc.noun_chunks:
    #     print(chunk)

    ### need to check dependencies


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("input_file", help="choose the text file to process.")
    args = parser.parse_args()

    # run puppy, run
    PIMINER(args.input_file)

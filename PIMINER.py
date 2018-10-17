#!/usr/bin/env python

import argparse # inorder to port to command line
import os # system controls
import pandas as pd # dataframe data structure for outputs
import textract # used to parse PDF files
import re # string operations, mostly data cleaning
import subprocess # used to invoke shell scripts
import spacy # industrial strength NLP engine
from spacy.symbols import nsubj, VERB


"""
Iterate through a series of regex expressions for matches
Expressions defined in the piminer() function
"""
def getRegexMatches(patterns, doc):

    regex_matches = []

    for search_pattern in patterns:
        search_cout = 0
        print('Searching for: ' + str(search_pattern[0]))

        for regex_match in re.finditer(re.compile(search_pattern[1]), doc.text):
            if regex_match:
                search_cout += 1
                match_as_string = "{}".format(regex_match.group(0))
                tup = (search_pattern[0], match_as_string)
                regex_matches.append(tup)

        print(str(search_pattern[0] + ' search COMPLETE.'))
        print('Found ' + str(search_cout) + '\n')

    return regex_matches


"""
Iterate through named_entity for matches of certain types
entity_types defined in piminer() function
"""
def getNamedEntities(entity_types, doc):
    print('Searching for named_entity...')

    valid_ent = re.compile("^[a-zA-Z0-9_]*$")
    ENTITY_LIST = []

    for entity in doc.ents:
        # for now, limit output to the entity types in the list above,, clean output
        if entity.label_ in entity_types:
            NER_tup = (str(entity.label_).upper(), re.sub('[^A-Za-z0-9]+', ' ', str(entity.text)))
            ENTITY_LIST.append(NER_tup)

    print('named_entity search COMPLETE.')
    print('Found' + str(len(ENTITY_LIST)) + '\n')
    return ENTITY_LIST

"""
Main control function
Call aux functions and print statuses to stdin
"""
def piminer(input_file):

    # model = 'en_core_web_lg'
    model = 'en_core_web_md'
    print('Loading spacy library: ' + str(model))

    # load NLP library object
    nlp = spacy.load(model)
    print('Library load COMPLETE.\n')

    # file operations
    source_file = os.path.basename(input_file)
    base = os.path.splitext(source_file)[0]

    """
    need to make simple file handling more robust.
    it may be the case that this is better suited for another script,
    or should be called from main. TDB.
    """

    print('Reading file: ' + str(source_file))
    # create nlp object from input_file
    text = str(textract.process(input_file))
    print('Read COMPLETE.\n')

    print('Converting file to spacy object: ' + str(source_file))
    doc = nlp(text)
    print('Convert COMPLETE.\n')

    patterns = [
        ('phone_number', '\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}'),
        ('email_address', '^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$'),
        ('social_security_number', '^(?!000)([0-6]\d{2}|7([0-6]\d|7[012])) ([ -])? (?!00)\d\d([ -|])? (?!0000)\d{4}$'),
        ('EIN_number', '/[0-9]{2}-[0-9]{7}/'),
        ('passport_number', '/[0-9]{2}-[0-9]{7}/'),
        ('Iv4', '/[0-9]{2}-[0-9]{7}/'),
        ('Iv6', '/^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$/i'),
        ('credit_card_number', '/^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$/i')
    ]

    # define lists based off of first-pass regex and NER
    getRegexMatches(patterns, doc)

    entity_types = ['PERSON', # People, including fictional.
                    'NORP', # Nationalities or religious or political groups.
                    'FAC', # Buildings, airports, highways, bridges, etc.
                    'ORG', # Companies, agencies, institutions, etc.
                    'GPE', # Countries, cities, states.
                    'LOC', # Non-GPE locations, mountain ranges, bodies of water.
                    'EVENT', # Named hurricanes, battles, wars, sports events, etc
                    'WORK_OF_ART', # Titles of books, songs, etc.
                    'LAW', # Named documents made into laws.
                    'DATE'] # Absolute or relative dates or periods.

    getNamedEntities(entity_types, doc)


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("input", help="Choose the text file to process.")
    args = parser.parse_args()

    # run puppy, run
    piminer(args.input)

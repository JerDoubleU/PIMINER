#!/usr/bin/env python

import argparse # inorder to port to command line
import os # system controls
import pandas as pd # dataframe data structure for outputs
import math
import textract # used to parse PDF files
"""
Textract supports the following file types:
    [.csv, .doc , .docx , .eml , .epub, .gif, .jpg, .jpeg, .json,
    .html, .htm, .mp3, .msg, .odt, .ogg, .pdf, .png, .pptx, .ps,
    .rtf, .tiff,  .tif, .txt, .wav, .xlsx, .xls]
"""
import re # string operations, mostly data cleaning
# import subprocess # used to invoke shell scripts
import spacy # industrial strength NLP engine
from spacy.symbols import nsubj, VERB


# function to handle input larger than 1000000 character
def textSplit(text, size):
    text_splits = []
    for i in range(0, len(text), size):
        text_splits.append(text[i:i + size])

    return text_splits


def getTokens(document):
    """
    If needed: https://spacy.io/api/annotation#pos-tagging
    """

    tokenList = []

    for token in document:
        tup = (token.text,[token.lemma_, token.pos_, token.tag_, token.dep_,\
              token.shape_, token.is_alpha, token.is_stop])
        tokenList.append(tup)
    return tokenList


def getChunks(document):
    chunkList = []

    for chunk in document.noun_chunks:
        tup = (chunk.text, [chunk.root.text, chunk.root.dep_, \
          chunk.root.head.text])
        chunkList.append(tup)

    return chunkList


def getChildren(document):
    childList = []

    for token in document:

        print(token.text, token.dep_, token.head.text, token.head.pos_,
              [child for child in token.children], '\n')


"""
Iterate through a series of regex expressions for matches
Expressions defined in the piminer() function
"""
def getRegexMatches(regex_patterns, document):

    regex_matches = []

    for search_pattern in regex_patterns:
        search_cout = 0
        print('Searching for: ' + str(search_pattern[0]))

        for regex_match in re.finditer(re.compile(search_pattern[1]), document.text):
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
def getNamedEntities(named_entity_types, document):
    print('Searching for named_entity...')

    valid_ent = re.compile("^[a-zA-Z0-9_]*$")
    ENTITY_LIST = []

    for entity in document.ents:
        # for now, limit output to the entity types in the list above,, clean output
        if entity.label_ in entity_types:
            NER_tup = (str(entity.label_).upper(), re.sub('[^A-Za-z0-9]+', ' ', str(entity.text)))
            ENTITY_LIST.append(NER_tup)

    print('named_entity search COMPLETE.')
    print('Found ' + str(len(ENTITY_LIST)) + '\n')
    return ENTITY_LIST

"""
Main control function
Call aux functions and print statuses to stdin
"""
def piminer(input_file):

    # model = 'en_core_web_lg'
    model = 'en_core_web_md'
    print('Loading language library: ' + str(model) + '...')

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

    print('Reading file: ' + str(source_file) + '...')
    # create nlp object from input_file
    text = str(textract.process(input_file,
            method='tesseract',
            language='en'))

    print('Read COMPLETE.\n')


    """
    Need to break larger text files into multiple chunks because
    spacy can only take 1000000 characters at a time...
    """

    if len(text) > 999999:
        text_list = []

        # break document into fewest possible splits:
        splits = math.ceil(len(text)/999999)

        print('Document with length ' + str(len(text)) + \
            ' must be distributed between ' + str(splits) + ' splits...\n')

        text_list.append(textSplit(text, math.ceil(len(text)/splits)))
    else:
        text_list = []
        text_list.append(text)

        """
        Need to iterate through input to run on smaller string sections
        """

    for split in text_list:
        document = nlp(str(split))

        [print(x) for x in getTokens(document)]




    # print('Converting file to spacy object: ' + str(source_file))
    # document = nlp(text)
    # print('Convert COMPLETE.\n')
    # #
    #
    # """
    # Some testing for dependency parsing
    # """
    # # [print(x) for x in getTokens(document)]
    # # [print(x) for x in getChunks(document)]
    # getChildren(document)
    #
    # regex_patterns = [
    #     ('phone_number', '\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}'),
    #     ('phone_number','(^\+[0-9]{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0)([0-9]{9}$|[0-9\-\s]{10}$)'),
    #     ('VIN_number', "^[^iIoOqQ'-]{10,17}$"),
    #     ('email_address', '^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$'),
    #     ('latitude_longitude', '^[NS]([0-8][0-9](\.[0-5]\d){2}|90(\.00){2})\040[EW]((0\d\d|1[0-7]\d)(\.[0-5]\d){2}|180(\.00){2})$'),
    #     ('social_security_number', '^(?!000)([0-6]\d{2}|7([0-6]\d|7[012])) ([ -])? (?!00)\d\d([ -|])? (?!0000)\d{4}$'),
    #     ('EIN_number', '/[0-9]{2}-[0-9]{7}/'),
    #     ('passport_number', '/[0-9]{2}-[0-9]{7}/'),
    #     ('Iv4', '/[0-9]{2}-[0-9]{7}/'),
    #     ('Iv6', '/^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$/i'),
    #     ('credit_card_number', '/^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$/i'),
    #     ('CA_driver_license', '"^[A-Z]{1}\d{7}$')
    # ]
    #
    # # define lists based off of first-pass regex and NER
    # getRegexMatches(regex_patterns, document)
    #
    # named_entity_types = ['PERSON', # People, including fictional.
    #                 'NORP', # Nationalities or religious or political groups.
    #                 'FAC', # Buildings, airports, highways, bridges, etc.
    #                 'ORG', # Companies, agencies, institutions, etc.
    #                 'GPE', # Countries, cities, states.
    #                 'LOC', # Non-GPE locations, mountain ranges, bodies of water.
    #                 'EVENT', # Named hurricanes, battles, wars, sports events, etc
    #                 'WORK_OF_ART', # Titles of books, songs, etc.
    #                 'LAW', # Named documents made into laws.
    #                 'DATE'] # Absolute or relative dates or periods.
    #
    # getNamedEntities(named_entity_types, document)


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("input", help="Choose the text file to process.")
    args = parser.parse_args()

    # run puppy, run
    piminer(args.input)

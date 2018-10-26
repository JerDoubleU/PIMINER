#!/usr/bin/env python

import argparse # # inorder to port to command line
import os # # system controls
import pandas as pd # # dataframe data structure for outputs
import math # # used to break files into chunks
import textract # # used to parse PDF files
import re # # string operations, mostly data cleaning
import spacy # # industrial strength NLP engine
from spacy.symbols import nsubj, VERB

# # function to handle input larger than 1000000 character
# # takes a string (not NLP object) and a list size as an input
def textSplit(text, size):
    text_splits = []

    for i in range(0, len(text), size):
        text_splits.append(text[i:i + size])

    return text_splits


# # get list of single words
# # takes an NLP object as input
# # if needed: https://spacy.io/api/annotation#pos-tagging
def getTokens(document):
    tokenList = []

    for token in document:
        tup = (token.text,[token.lemma_, token.pos_, token.tag_, token.dep_,\
              token.shape_, token.is_alpha, token.is_stop])
        tokenList.append(tup)

    return tokenList


# # get list of noun-chunks from an NLP object
# # takes an NLP object as input
def getChunks(document):
    chunkList = []

    for chunk in document.noun_chunks:
        tup = (chunk.text, [chunk.root.text, chunk.root.dep_, \
          chunk.root.head.text])
        chunkList.append(tup)

    return chunkList


# # get list of items that preceed the current token
# # takes an NLP object as input
def getChildren(token):
    childList = []

    print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children], '\n')

# # takes an NLP object as input
# # returns a dataframe of position, type, and value
def getEntities(document):

    print('Conducting individual entity searches...\n')

    # # list structure to transform into dataframe
    new_rows = []

    print('Conducting named entity search...')

    for entity in document.ents:

        # print(dir(entity))

        # print('for:', entity.text)

        # store the left and right tokens for all NEs
        lefts = []
        subtree = []

        [lefts.append(x) for x in entity.lefts]
        [rights.append(x) for x in entity.lefts]
        [subtree.append(x) for x in entity.subtree]

        row = {'entity_type':str(entity.label_).upper(),
            'text_value':str(entity.text),
            'start_position':entity.start_char,
            'end_position':entity.end_char,
            'lefts':lefts,
            'subtree':subtree}

        new_rows.append(row)

    print('Named entity search COMPLETE.\n')

    # # easily extendable regex_patterns
    regex_patterns = {
        'PHONE_NUMBER': '\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}',
        'INTERNATIONAL_PHONE_NUMBER':'(?:[+]\d{1,4}-\d{3}-\d{3}-\d{4}|\d{1,4}-\d{3}-\d{3}-\d{4})',
        'VIN_NUMBER': "^[^iIoOqQ'-]{10,17}$",
        'EMAIL_ADDRESS': '^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$',
        'LATITUDE_LONGITUDE': '^[NS]([0-8][0-9](\.[0-5]\d){2}|90(\.00){2})\040[EW]((0\d\d|1[0-7]\d)(\.[0-5]\d){2}|180(\.00){2})$',
        'SOCIAL_SECURITY_NUMBER': '^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$',
        'EIN_number': '^(?:\d{2}-\d{7})$',
        'passport_NUMBER': '/[0-9]{2}-[0-9]{7}/',
        'Iv4': '/[0-9]{2}-[0-9]{7}/',
        'Iv6': '/^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$/i',
        'CREDIT_CARD_NUMBER': '/^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$/i'
    }

    print('Conducting regex search...')
    for search_pattern in regex_patterns:

        for regex_match in re.finditer(re.compile(regex_patterns[search_pattern]), document.text):
            if regex_match:

                # get position of match
                span = regex_match.span()

                # token = document[span[0]:span[1]]
                # print(token)


                match_as_string = "{}".format(regex_match.group(0))

                # build row
                row = {'entity_type':search_pattern,
                    'text_value':match_as_string,
                    'start_position':span[0],
                    'end_position':span[1]}

                # save to list for conversion to dataframe
                new_rows.append(row)

    print('Regex search COMPLETE.\n')

    print('Found ' + str(len(new_rows)) + ' total entities...')
    print('Individual entity search COMPLETE.\n')
    # # return dataframe with results for clustering
    return pd.DataFrame(new_rows)


# # flow control function
# # takes a a commandline argument (file)
def piminer(input_file):

    # # model = 'en_core_web_lg'
    model = 'en_core_web_md'
    print('Loading language library: ' + str(model) + '...')

    # # load NLP library object
    nlp = spacy.load(model)
    print('Library load COMPLETE.\n')

    # # file operations to manage printing
    # # probably need to get full path as well...
    source_file = os.path.basename(input_file)
    base = os.path.splitext(source_file)[0]

    # # need to make simple file handling more robust
    # # it may be the case that this is better suited for another script,
    # # or should be called from main. TDB.

    print('Reading file: ' + str(source_file) + '...')

    # # create nlp object from input_file
    text = str(textract.process(input_file,
            method='tesseract',
            language='en'))

    print('Read COMPLETE.\n')


    # # breaks files into manageable chunks
    # # may be suited for a separate function call
    # # though likely called only once
    if len(text) > 999999:
        text_list = []

        # # break document into fewest possible splits:
        splits = math.ceil(len(text)/999999)

        print('Document with length ' + str(len(text)) + \
            ' must be distributed between ' + str(splits) + ' splits...')

        # # add all splits to new list
        [text_list.append(x) for x in textSplit(text, math.ceil(len(text)/splits))]
        print('Document split COMPLETE.\n')
    else:
        # # if document under 10000000 chars, just store
        splits = 1
        text_list = []
        text_list.append(text)

    # # index the chunks of the file
    processing_count = 1

    # # process all string chunks
    for string_chunk in text_list:

        print('Converting file to spacy object: ' + str(source_file) + '...')
        print('Part ' + str(processing_count) + ' of ' + str(splits))
        document = nlp(string_chunk)
        print('Convert COMPLETE.\n')

        # # increment the document chunk
        processing_count += 1

        # get dataframe with entity type, entity value, and position
        frame = getEntities(document)
        print(frame)
        frame.to_csv(str(base) + "_PII_Results.csv")

if __name__ == "__main__":

    # # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("input", help="Choose the text file to process.")
    args = parser.parse_args()

    # # run puppy, run
    piminer(args.input)

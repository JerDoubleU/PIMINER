#!/usr/bin/env python3

import argparse # # inorder to port to command line
import os # # system controls
import pandas as pd # # dataframe data structure for outputs
import math # # used to break files into chunks
import textract # # used to parse PDF files
import re # # string operations, mostly data cleaning
import spacy # # industrial strength NLP engine
import time # used to print timing metrics
from spacy.symbols import nsubj, VERB
# from sklearn import covariance, cluster # attempt at clustering

# # function to handle input larger than 1000000 characters
# # takes a string (not NLP object) and a list size as an input
def textSplit(text, size):
    text_splits = []

    for i in range(0, len(text), size):
        text_splits.append(text[i:i + size])

    return text_splits


# # function to parse regex input
def regexPatternsFromFile(regex_input):
    pattenFile = open(regex_input, 'r')

    pattern_dict = {}

    for line in pattenFile:
        row = line.split(';')
        pattern_dict[row[0]] = row[1]

    return pattern_dict


# # takes an NLP object as input
# # returns a dataframe of position, type, and value
def getEntities(document, regex_input):

    print('Conducting individual entity searches...\n')

    # # list structure to transform into dataframe
    new_rows = []

    # # merge entities and noun chunks into one token
    # spans = list(document.ents) + list(document.noun_chunks)
    # for span in spans:
    #     span.merge()

    print('Conducting named entity search...')
    nerTime = time.time()

    for entity in document.ents:
        # store the left and right tokens for all NEs
        lefts = []
        rights = []
        subtree = []
        relations = []

        [lefts.append(x) for x in entity.lefts]
        [rights.append(x) for x in entity.rights]
        [subtree.append(x) for x in entity.subtree]

        # if entity.dep_ in ('attr', 'dobj'):
        #     subject = [w for w in entity.head.lefts if w.dep_ == 'nsubj']
        #     if subject:
        #         subject = subject[0]
        #         relations.append((subject, entity))
        # elif entity.dep_ == 'pobj' and entity.head.dep_ == 'prep':
        #     relations.append((entity.head.head, entity))

        # print('for', entity.text)
        # [print(x) for x in realtions]
        # print()

        row = {'entity_type':str(entity.label_).upper(),
            'text_value':str(entity.text),
            'start_position':entity.start_char,
            'end_position':entity.end_char,
            'lefts':lefts,
            'rights':rights,
            'subtree':subtree}

        new_rows.append(row)

    nerTimeEnd = time.time()
    print('Named entity search COMPLETE: ' + str(nerTimeEnd - nerTime) + ' seconds\n')

    regexTime = time.time()

    # # get regex patterns from file (more easily extendable)
    regex_patterns = regexPatternsFromFile(regex_input)

    print('Conducting regex search...')
    for search_pattern in regex_patterns:

        for regex_match in re.finditer(re.compile(regex_patterns[search_pattern]), document.text):
            if regex_match:

                # # get position of match
                # # not sure of this is correct,
                # # pulling from the document text, not the doc object
                span = regex_match.span()

                match_as_string = "{}".format(regex_match.group(0))

                # # build row
                row = {'entity_type':search_pattern,
                    'text_value':match_as_string,
                    'start_position':span[0],
                    'end_position':span[1],
                    'lefts':"",
                    'rights':"",
                    'subtree':""}

                # # save to list for conversion to dataframe
                new_rows.append(row)

    regexTimeEnd = time.time()
    print('Regex search COMPLETE: ' + str(regexTimeEnd - regexTime) + ' seconds\n')

    print('Found ' + str(len(new_rows)) + ' total entities...')
    print('Individual entity search COMPLETE.\n')

    # # return dataframe with results for clustering
    return pd.DataFrame(new_rows)


# # flow control function
# # takes a a commandline argument (file)
def piminer(input_file, regex_input):
    modelLoadTime = time.time()

    # # model = 'en_core_web_lg'
    model = 'en_core_web_md'

    print('Loading language library: ' + str(model) + '...')
    nlp = spacy.load(model)
    modelLoadTimeEnd = time.time()

    print('Library load COMPLETE: ' + str(modelLoadTimeEnd - modelLoadTime) + ' seconds\n')

    # file operstions for naming output
    source_file = os.path.basename(input_file)
    base = os.path.splitext(source_file)[0]

    # # need to make simple file handling more robust
    print('Reading file: ' + str(source_file) + '...')
    fileReadTime = time.time()

    # # create nlp object from input_file
    text = str(textract.process(input_file,
            method='tesseract',
            language='en'))

    # # spacy has a limit of 1000000 chars
    # # break into multiple files to handle
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

    fileReadTimeEnd = time.time()
    print('Read COMPLETE: ' + str(fileReadTimeEnd - fileReadTime) + ' seconds\n')

    # # process all string chunks
    for string_chunk in text_list:


        print('Converting file to spacy object: ' + str(source_file) + '...')
        print('Part ' + str(processing_count) + ' of ' + str(splits))
        spacyObjectTime = time.time()
        document = nlp(string_chunk)
        spacyObjectTimeEnd = time.time()
        print('Convert COMPLETE: ' + str(spacyObjectTimeEnd - spacyObjectTime) + ' seconds\n')

        # # increment the document chunk
        processing_count += 1

        # get dataframe with entity type, entity value, and position
        frame = getEntities(document, regex_input)
        frame.to_csv(str(base) + "_PII_Results.csv")


if __name__ == "__main__":

    # # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("--input_file", help="Choose the text file to process.")
    parser.add_argument("--regex_input", help="Choose the text file to process.")
    args = parser.parse_args()

    totalTime = time.time()
    # # run puppy, run
    piminer(args.input_file, args.regex_input)

    totalTimeEnd = time.time()
    print('piminer COMPLETE: ' + str(totalTimeEnd - totalTime) + ' seconds\n')

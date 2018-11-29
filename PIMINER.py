#!/usr/bin/env python3

"""
#----------------------------- Authors ----------------------------------------#
Author: Cooper Stansbury
Author: Dom Korzecke
Author: Kevin Peters
Author: Robert Kaster

#----------------------------- Overview ---------------------------------------#
Piminer.py is a command line tool written in python3 that can be used to extract
possible named entities and patterns matching custom regex expressions in
unstructured text documents.

#----------------------------- Arguments --------------------------------------#
TWO Positional Arguments:
1. --input_file: A text file to extract PII elements from.
2. --regex_input: A text file containing regular expressions and labels.
"""

#----------------------------- Dependencies -----------------------------------#
import argparse # # inorder to port to command line
import os # # system controls
import pandas as pd # # dataframe data structure for outputs
import math # # used to break files into chunks
import textract # # used to parse PDF files
import re # # string operations, mostly data cleaning
import spacy # # industrial strength NLP engine
import time # used to print timing metrics
from spacy.symbols import nsubj, VERB
from tqdm import tqdm # status bar


################################## Helper Functions ############################
def textSplit(text, size):
    """
    note: Handle doc input larger than 1000000 characters
    inputs:
        'text' a string (not NLP object)
        'size' an integer list size.
    return: 'text' deivided into 'size' partitions in a list.
    """

    text_splits = []

    for i in range(0, len(text), size):
        text_splits.append(text[i:i + size])

    return text_splits


def regexPatternsFromFile(regex_input):
    """
    note: parse regex input arguement
    input:
        'regex_input': file passed from commandline arg
    return: dictionary of labels and patterns
    """

    pattenFile = open(regex_input, 'r')

    pattern_dict = {}

    for line in pattenFile:
        row = line.split(';')
        pattern_dict[row[0]] = row[1].strip()

    return pattern_dict


def possibleRelations(sentence):
    """
    note: find syntactic dependencies in sentence for possible relationsself. A
        subtree is a sequence of all the token's syntactic descendants.
    input:
        'sentence': a tokenized sentence.
    return: list of all possible dependents.
    """

    subtree = []

    [subtree.append(str(x.ent_type_).strip() + ":" + str(x).strip())\
        for x in sentence.subtree if str(x.ent_type_).strip() != "" \
            and str(x).strip() != ""]

    return subtree


################################## Entity Search ###############################
def entitySearch(document, regex_input):
    """
    note: search through document and construct dataframe for all PII elements.
    inputs:
        'document': an NLP object.
        'regex_input': regex pattern file

    return: a dataframe of entities and metadata.
    """

    entitySearchTime= time.time()

    print('Conducting entity searches...')

    # # list structure to transform into dataframe
    new_rows = []

    # # get regex patterns from file (more easily extendable)
    regex_patterns_dict = regexPatternsFromFile(regex_input)

    #---------------------------- NER Search ----------------------------------#
    for sentence in tqdm(document.sents):

        # # check if sentence contains named entities
        # # if yes, add these entities to the list
        if sentence.ents:
            entity_list = sentence.ents
            [new_rows.append({
                    'entity_type':str(x.label_).upper(),
                    'text_value':str(x.text),
                    'raw_sentence':str(x.sent),
                    'sentence_position':x.sent.start,
                    'sentence_root':sentence.root,
                    'possible_dependents': ", ".join(possibleRelations(sentence)),
                    'n_possible_dependents': len(possibleRelations(sentence))
                    }) for x in entity_list]

    #----------------------------- Regex Search -------------------------------#
    """
    note: regex patterns are called on raw string values for each sent AND on
        cleaned sentences to maximize the chances of discovering PII elements.
    """
        for search_pattern in regex_patterns_dict:

            # # need to declare the string each time, not sure why
            # # provide two sentences just in case this helps matching
            plaintext_sent = sentence.text
            cleaned_sentence = re.sub('\W+',' ', sentence.text.strip())

            regex = 'r' + regex_patterns_dict[search_pattern]

            # findall returns  list
            plaintext_matches = re.findall(regex, plaintext_sent)

            [new_rows.append(
                {
                    'entity_type':str(search_pattern),
                    'text_value':str(x),
                    'raw_sentence':str(sentence.text),
                    'sentence_position':sentence.start,
                    'sentence_root':sentence.root,
                    'possible_dependents': ", ".join(possibleRelations(sentence)),
                    'n_possible_dependents': len(possibleRelations(sentence))
                }) for x in plaintext_matches if len(x) > 0]

            cleaned_text_matches = re.findall(regex, cleaned_sentence)

            [new_rows.append(
                {
                    'entity_type':str(search_pattern),
                    'text_value':str(x),
                    'raw_sentence':str(sentence.text),
                    'sentence_position':sentence.start,
                    'sentence_root':sentence.root,
                    'possible_dependents': ", ".join(possibleRelations(sentence)),
                    'n_possible_dependents': len(possibleRelations(sentence))
                }) for x in cleaned_text_matches if len(x) > 0]

    entitySearchTimeEnd= time.time()
    print('\nFOUND: ', len(new_rows))
    print('Entity searches COMPLETE: ' + str(modelLoadTimeEnd - modelLoadTime) \
        + ' seconds\n')

    return pd.DataFrame(new_rows)


################################## Main ########################################
if __name__ == "__main__":

    #----------------------------- Argument Definition ------------------------#
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("--input_file", \
        help="Choose the text file to process.")

    parser.add_argument("--regex_input", \
        help="Choose the text file to process.")
    args = parser.parse_args()

    #----------------------------- NLP Model Loading --------------------------#
    totalTime = time.time()
    modelLoadTime = time.time()

    # # model = 'en_core_web_lg'
    model = 'en_core_web_md'

    print('Loading language library: ' + str(model) + '...')
    nlp = spacy.load(model)
    modelLoadTimeEnd = time.time()

    print('Library load COMPLETE: ' + str(modelLoadTimeEnd - modelLoadTime) \
        + ' seconds\n')

    #----------------------------- File Operations ----------------------------#
    # file operstions for naming output
    source_file = os.path.basename(args.input_file)
    base = os.path.splitext(source_file)[0]

    # # need to make simple file handling more robust
    print('Reading file: ' + str(source_file) + '...')
    fileReadTime = time.time()

    # # create nlp object from input_file
    text = str(textract.process(args.input_file,
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
        [text_list.append(x) for x in \
            textSplit(text, math.ceil(len(text)/splits))]

        print('Document split COMPLETE.\n')
    else:
        # # if document under 10000000 chars, just store
        splits = 1
        text_list = []
        text_list.append(text)

    # # index the chunks of the file
    processing_count = 1

    fileReadTimeEnd = time.time()
    print('Read COMPLETE: ' + str(fileReadTimeEnd - fileReadTime) \
        + ' seconds\n')

    # # process all string chunks
    for string_chunk in text_list:

        print('Converting file to spacy object: ' + str(source_file) + '...')
        print('Part ' + str(processing_count) + ' of ' + str(splits))
        spacyObjectTime = time.time()
        document = nlp(string_chunk)
        spacyObjectTimeEnd = time.time()
        print('Convert COMPLETE: ' + \
            str(spacyObjectTimeEnd - spacyObjectTime) + ' seconds\n')

        # # increment the document chunk
        processing_count += 1

    #----------------------------- Entity Search ------------------------------#

        # get dataframe with entity type, entity value, and position
        frame = entitySearch(document, args.regex_input)
        frame.to_csv("results_for_" + str(base) + ".csv")

    totalTimeEnd = time.time()
    print('piminer COMPLETE: ' + str(totalTimeEnd - totalTime) + ' seconds\n')

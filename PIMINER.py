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
        pattern_dict[row[0]] = row[1].strip()

    return pattern_dict


# # takes an NLP object and regex pattern file as input
# # returns a dataframe of position, type, and value
def entitySearch(document, regex_input):

    print('Conducting entity searches...\n')

    # # list structure to transform into dataframe
    new_rows = []

    # # get regex patterns from file (more easily extendable)
    regex_patterns = regexPatternsFromFile(regex_input)

    for sentence in document.sents:

        # check if sentence contains named entities
        if sentence.ents:
            entity_list = sentence.ents
            [new_rows.append({
                    'entity_type':str(x.label_).upper(),
                    'text_value':str(x.text),
                    'sentence':str(x.sent),
                    'sentence_position':x.sent.start
                    }) for x in entity_list]

        # print(dir(sentence.as_doc()))

        for search_pattern in regex_patterns:

            plaintext_sent = sentence.text
            cleaned_sentence = re.sub('\W+',' ', sentence.text)

            regex = 'r' + regex_patterns[search_pattern]

            plaintext_matches = re.findall(regex, plaintext_sent)

            [print(
                {
                    'entity_type':str(search_pattern),
                    'text_value':str(x),
                    'sentence':str(sentence.text),
                    'sentence_position':sentence.start
                },'\n') for x in plaintext_matches if len(x) > 0]

            cleaned_text_matches = re.findall(regex, cleaned_sentence)

            [print(
                {
                    'entity_type':str(search_pattern),
                    'text_value':str(x),
                    'sentence':str(sentence.text),
                    'sentence_position':sentence.start
                },'\n') for x in cleaned_text_matches if len(x) > 0]


            #
            # if compiled_pattern.match(plaintext_sent):
            #     match_as_string = "{}".format(compiled_pattern.match(plaintext_sent).group(0))
            #
            #     row = {
            #         'entity_type':str(search_pattern),
            #         'text_value':str(match_as_string),
            #         'sentence':str(sentence.text),
            #         'sentence_position':sentence.start
            #     }
            #
            #     print(row)
            #
            #     new_rows.append(row)

            # elif compiled_pattern.match(sentence.text):
            #     match_as_string = "{}".format(compiled_pattern.match(sentence.text).group(0))
            #
            #     row = {
            #         'entity_type':str(search_pattern),
            #         'text_value':str(match_as_string),
            #         'sentence':str(sentence.text),
            #         'sentence_position':sentence.start
            #     }
            #
            #     print(row)
            #
            #     new_rows.append(row)



    # [print(x) for x in new_rows]

    return pd.DataFrame(new_rows)


if __name__ == "__main__":

    # # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("--input_file", help="Choose the text file to process.")
    parser.add_argument("--regex_input", help="Choose the text file to process.")
    args = parser.parse_args()

    totalTime = time.time()
    modelLoadTime = time.time()

    # # model = 'en_core_web_lg'
    model = 'en_core_web_md'

    print('Loading language library: ' + str(model) + '...')
    nlp = spacy.load(model)
    modelLoadTimeEnd = time.time()

    print('Library load COMPLETE: ' + str(modelLoadTimeEnd - modelLoadTime) + ' seconds\n')

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
        frame = entitySearch(document, args.regex_input)
        frame.to_csv("results_for_" + str(base) + ".csv")

    totalTimeEnd = time.time()
    print('piminer COMPLETE: ' + str(totalTimeEnd - totalTime) + ' seconds\n')

import argparse # inorder to port to command line
import os # system controls
import pandas as pd # dataframe data structure for outputs
import textract # used to parse PDF files
import spacy # industrial strength NLP engine
import re # string operations, mostly data cleaning
import subprocess # used to invoke shell scripts

# load NLP library object
nlp = spacy.load('en_core_web_lg')

# main function call
def PIMINER(input_file):

    # file operations
    source_file = os.path.basename(input_file)
    base = os.path.splitext(source_file)[0]
    print('*** PRINTING RESULTS FOR: ' + str(base) + ' ***')

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

    # create nlp object from input_file
    text = str(textract.process(input_file))
    doc = nlp(text)

    ## this is a check for possible phone numbers, saved to list
    PHONE_NUMBER = re.compile('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
    PHONE_NUMBER_LIST = []

    for phone_match in re.finditer(PHONE_NUMBER, doc.text):
        if phone_match:
            PHONE_NUMBER_LIST.append("{}".format(phone_match.group(0)))
            print("POSSIBLE PHONE NUMBER: {}".format(phone_match.group(0)))

    ## this is a check for possible email addresses, saved to a list
    # EMAIL_ADDRESS = re.compile('[^@]+@[^@]+\.[^@]+')
    # EMAIL_ADDRESS_LIST = []
    #
    # for email_match in re.finditer(EMAIL_ADDRESS, doc.text):
    #     if email_match:
    #         PHONE_NUMBER_LIST.append("{}".format(email_match.group(0)))
    #         print("POSSIBLE EMAIL ADDRESS: {}".format(email_match.group(0)))

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

    # print out detected named entities
    for ent in doc.ents:

        # for now, limit output to the entity types in the list above
        if ent.label_ in entity_types:
            print('POSSIBLE ' + str(ent.label_).upper() + ": " + str(ent.text))

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

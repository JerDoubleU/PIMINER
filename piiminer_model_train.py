from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import en_core_web_md

nlp = en_core_web_md.load()

# training data
TRAIN_DATA = [
    ("Kirkland & Ellis represent me", {
        'entities':  [(0, 16, 'ORG')]
    }),
    ("The case is taken on by Latham & Watkins", {
        'entities':  [(24, 39, 'ORG')]
    }),
    ("John Frank works for DLA Piper", {
        'entities':  [(0, 9, "NAME"), (21, 29, "ORG")]
    }),
    ("He was represented by James Flooney JD", {
        'entities':  [(22, 34, "NAME")]
    }),
    ("George can be reached at 687-483-9384", {
        'entities':  [(0, 5, "NAME")]
    }),
    ("Allen & Overy will proceed with litigation ", {
        'entities':  [(0, 12, "ORG")]
    }),
    ("The legal firm on the assignment is DLA Piper", {
        'entities':  [(36, 44, 'ORG')]
    }),
    ("Joseph Frank JD is here representing Steve & Steve", {
        'entities':   [(0, 11, "NAME"), (37, 49, "ORG")]
    }),
    ("Jospeh and Jospeh is the firm assigned",  {
        'entities':  [(0, 9, "NAME")]
    }),
    ("John banks pressed charges on Camel", {
        'entities':  [(0, 9, "NAME"), (30, 34, "ORG")]
    }),
    ("Blane's credit card number was redacted", {
        'entities':  [(0, 6, "NAME")]
    }),
    ("Upon further review evidence suggests Ryan Colber was responsible", {
        'entities':  [(38, 48, "NAME")]
    }),
    ("Johnson and Johnson - 578-454-3456", {
        'entities':  [(0, 18, 'ORG')]
    }),
    ("The Lawyer representing the case is Steven Enkle", {
        'entities':  [(35, 47, "ORG")]
    }),
    ("The victim is Erik Swinkler", {
        'entities':  [(14, 26, "NAME")]
    }),
    ("provided by Morgan Lewis & Bockius", {
        'entities':  [(12, 33, "NAME")]
    }),
    ('Bernard "billy" Romaine was victim', {
        'entities':  [(0, 22, "NAME")]
    }),
    ("Robert Butter was 14 at the time", {
        'entities':  [(0, 12, "NAME")]
    }),
    ("The Tobacco Company advertised to Steve (15)", {
        'entities':  [(35, 39, "NAME")]
    }),
    ("legal@lawfirm.com - Ropes & Gray", {
        'entities':  [(20, 31, "ORG")]
    }),
    ('Advertisements targeted at Suzan "Susie" Smith', {
        'entities':  [(27, 45, "NAME")]
    }),
    ("A representative from Simpson Thacher & Bartlett then went on to say", {
        'entities':  [(22, 47, "NAME")]
    }),
    ("Fredrick Small who is representing Philip Morris International argued the claim was unfair", {
        'entities':  [(0, 13, "NAME"), (35,61,"ORG")]
    }),
    (" ------------ Kutchner & Associates", {
        'entities':  [(14, 34, "ORG")]
    }),
    ('"The advertisements looked fun" stated Jim Neely', {
        'entities':  [(39, 47, "NAME")]
    }),
    ("Multiple children were targets of recent advertisements by Imperial Brands", {
        'entities':  [(59, 73, 'ORG')]
    }),
    ("Judge Abdul proceeded to call upon Francis Down", {
        'entities':  [(0, 10, "NAME"), (35, 46, "ORG")]
    }),
    ("The Judge, Samantha Stuart ordered the defendant to stop", {
        'entities':  [(11, 25, "NAME")]
    }),
    ("The Alabama Clean Indoor Act prevents these actions from happening", {
        'entities':  [(0, 27, "LAW")]
    }),
    ("Reynold Little referred to the The Tobacco Control Act when arguing againt claims made by K&L Gates", {
        'entities':  [(0, 13, "NAME"), (31, 53, "LAW"), (90, 98, "ORG")]
    }),
    ("Marlboro was exempt from the Food, Drug, and Cosmetic Act", {
        'entities':  [(0, 7, "ORG"), (32, 59, "LAW")]
    }),
    ("Rebecca Gardner pleaded with Judge Smith for the consideration of a special examination", {
        'entities':  [(0, 14, 'NAME'), (29, 39, "NAME")]
    }),
    ("Cooper was up to two packs a day with the stress University of Michigan brought", {
        'entities':  [(0, 6, 'PERSON'), (49, 71, 'ORG')]
    }),
    ("Mr Stansbury has become a heavy smoker over the years", {
        'entities':  [(0, 12, 'PERSON')]
    }),
    ("It has been stressful for Dr Stansbury", {
        'entities':  [(26, 38, "PERSON")]
    }),
    ("Litigation was arranged with Baker & McKenzie", {
        'entities':  [(29, 45, 'ORG')]
    }),
    ("Mr Korzecke was briefed by the legal council of Skadden, Arps, Slate, Meagher & Flom", {
        'entities':  [(0, 11, "PERSON"), (48, 84, 'ORG')]
    }),
    ("K&L Gates thinks they have a real case after Birhanu Eshete's 11 year old son Joanne started smoking a pack a day", {
        'entities':  [(0, 9, "ORG"), (45, 59, 'PERSON'), (78, 84, 'PERSON')]
    }),
    ("Usually Geoffery expects long hours working as an attorney, and Simpson Thacher & Bartlett is no exception", {
        'entities':  [(8, 15, "PERSON"), (64, 90, 'ORG')]
    }),
    ("O'Melveny & Myers would love to win the bid to litigate against the major tobacco companies", {
        'entities':  [(0, 17, "ORG")]
    }),
    ("It wasn't since recently, Akin Gump Strauss Hauer & Feld realized they had a real case over the sickness caused to Mrs. Jenison", {
        'entities':  [(26, 56, "ORG"), (115, 127, 'PERSON')]
    }),
    ("Freshfields Bruckhaus Deringer is very experienced in cigarette litagation claims", {
        'entities':  [(0, 30, "ORG")]
    }),
    ("The biggest law firm in the US is Baker & McKenzie Law", {
        'entities':  [(34, 54, "ORG")]
    }),
    ("Miss Winkle filed a tobacco litigation case against Phillip Morris", {
        'entities':  [(0, 11, "PERSON"), (52, 66, 'ORG')]
    }),
    ("This was the biggest lawsuit filed against Altria Group in 10 years", {
        'entities':  [(43, 55, "ORG")]
    }),
    ("British American Tobacco is in litigation with DLA Piper over underage smokers illnesses", {
        'entities':  [(0, 24, "ORG"), (47, 56, 'ORG')]
    }),
    ("Mr Jazz is likely to get a large settlement from Freshfields", {
        'entities':  [(0, 7, "PERSON"), (49, 60, 'ORG')]
    }),
    ("Peter Flemming is an underage smoker who is now living in an iron lung", {
        'entities':  [(0, 14, "PERSON")]
    }),
    ("Japan tobacco got Cindy hooked as a chain smoker at the age of 12.", {
        'entities':  [(0, 13, "ORG"), (18, 23, 'PERSON')]
    }),
    ("Bob Flynn wanted to be in the cool group at school.", {
        'entities':  [(0, 9, "PERSON")]
    }),
    ("Reynolds American is being represented by Allen & Overy in a large litigation case against Miss Zingerman", {
        'entities':  [(0, 17, "ORG"), (42, 55, 'ORG'),(91, 105, 'PERSON')]
    })
     ]

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model='en_core_web_md', output_dir='C:\\Users\\Dom Korzecke\\Train', n_iter=100): #Insert PATH for model to save in
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print('Losses', losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
            print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == '__main__':
    plac.call(main)
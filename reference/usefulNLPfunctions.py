#!/usr/bin/env python


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




relations = extract_relations(doc)
for r1, r2 in relations:
    print('{:<10}\t{}\t{}'.format(r1.text, r2.ent_type_, r2.text))


def extract_relations(doc):
    # merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()

    relations = []
    for ent in doc:
        if ent.dep_ in ('attr', 'dobj'):
            subject = [w for w in ent.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, ent))
        elif ent.dep_ == 'pobj' and ent.head.dep_ == 'prep':
            relations.append((ent.head.head, ent))
    return relations

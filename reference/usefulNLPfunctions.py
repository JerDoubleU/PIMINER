#!/usr/bin/env python


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

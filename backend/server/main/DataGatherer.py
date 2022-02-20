import nltk
nltk.download('punkt')
import json
import random
import numpy as np
import pandas as pd
from estnltk import Text
import re
from estnltk.wordnet import Wordnet
import logging
import jsonlines


def getData():
    # Loeme sisse
    data = pd.read_json('server/main/results.jl', lines=True)
    # Kaotame definitsioonide duplikaadid
    data.drop_duplicates(inplace=True)
    # Kõik suureks
    data['name'] = data['name'].str.upper()
    # Jätame alles ainult kindlate sümbolitega read
    keepPattern = '^[A-ZÜÖÄÕ ]*$'
    filtering = data['name'].str.contains(keepPattern)
    data = data[filtering]
    # Seame uued indeksid
    data.reset_index(drop=True, inplace=True)

    data = data.sort_values(ascending=False, by="name", key=lambda x: x.str.len())

    mask = (data['name'].str.len() <= 18) & (data['name'].str.len() >= 3)
    data = data.loc[mask]
    data = data.reset_index(drop=True)
    #print(data)

    #logging.info("Removing anwsers from questions")
    #data['def'] = data.apply(lambda row : removeAnswerFromQuestion(row), axis = 1)
    #data = data.to_json(orient='records', lines=True)
    #f = open("backend/server/main/testRes.jl", "w", encoding='utf-8')
    #f.write(data)
    #f.close()

    return data


def removeAnswerFromQuestion(row):
    question = row['def']
    answer = row['name'].lower()
    #print(answer, question)

    tekst = Text(question)
    tekst.tag_layer()

    for w in tekst.words:
        #print(w.lemma)
        if answer in w.lemma:
            question = question.replace(w.text, len(answer) * "_ ")

    pattern = re.compile(answer, re.IGNORECASE)
    return pattern.sub(len(answer) * "_ ", question)

#Gathers data from the Wordnet and outputs to .jl file
def getWordnetData():
    wn = Wordnet()
    logging.info("Getting wordnet data")
    with jsonlines.open('backend/server/main/wordnetData.jl', mode='a') as writer:
        for synset in enumerate(wn):
            if synset.definition != None:
                #print(synset.lemmas)
                #print(synset.definition)
                for lemma in synset.lemmas:
                    writer.write({
                                'name': lemma,
                                'def': synset.definition,
                            })


#data = getData()
#getWordnetData()
#print(data)
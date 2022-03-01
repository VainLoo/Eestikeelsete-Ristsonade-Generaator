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
from estnltk.vabamorf.morf import synthesize
import pandas as pd


def getTestData():
    # Loeme sisse
    data = pd.read_json('backend/server/main/test.jl', lines=True)
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

    return data

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
    logging.info("Data row count {}".format(len(data.index)))
    #print(data)

    return data

def cleanWikiData(data):
    logging.info("Removing anwsers from questions")
    data['def'] = data.apply(lambda row : removeAnswerFromQuestion(row), axis = 1)
    data = data.to_json(orient='records', lines=True, force_ascii=False)
    with open("backend/server/main/testRes.jl", "w", encoding='utf-8') as f:
        f.write(data)



def removeAnswerFromQuestion(row):
    question = row['def'].lower()
    answer = row['name'].lower().split()
    print(answer)
    #print(answer, question)

    tekst = Text(question)
    tekst.tag_layer()

    for w in tekst.words:
        for i in answer:
            print("answer in:", i, w.lemma)
            if i in w.lemma:
                print("LEIDIS:", w)
                len(w.text) * "_"
                question = question.replace(w.text, len(i) * "_ ")

    pattern = re.compile(i, re.IGNORECASE)
    return pattern.sub(len(i) * "_ ", question)

#Gathers data from the Wordnet and outputs to .jl file
def getWordnetData():
    wn = Wordnet()
    logging.info("Getting wordnet data")
    with jsonlines.open('backend/server/main/wordnetData.jl', mode='a') as writer:
        for synset in enumerate(wn):
            if synset.definition != None:
                for lemma in synset.lemmas:
                    writer.write({
                                'name': lemma,
                                'def': synset.definition,
                            })

#https://github.com/estnltk/estnltk/blob/version_1.6/tutorials/miscellaneous/morphological_synthesis.ipynb
cases = [
    # label, Estonian case name, English case name
    ('g', 'omastav', 'genitive'),
    ('p', 'osastav', 'partitive'),
    ('ill', 'sisseütlev', 'illative'),
    ('in', 'seesütlev', 'inessive'),
    ('el', 'seestütlev', 'elative'),
    ('all', 'alaleütlev', 'allative'),
    ('ad', 'alalütlev', 'adessive'),
    ('abl', 'alaltütlev', 'ablative'),
    ('tr', 'saav', 'translative'),
    ('ter', 'rajav', 'terminative'),
    ('es', 'olev', 'essive'),
    ('ab', 'ilmaütlev', 'abessive'),
    ('kom', 'kaasaütlev', 'comitative')]

def synthesize_all(word):
    case_rows = []
    sing_rows = []
    plur_rows = []
    for case, case_name_est, case_name_eng in cases:
        case_rows.append( case_name_est )
        sing_rows.append(', '.join(synthesize(word, 'sg ' + case, 'S')))
        plur_rows.append(', '.join(synthesize(word, 'pl ' + case, 'S')))

    return pd.DataFrame({'case': case_rows, 'singular': sing_rows, 'plural': plur_rows}, columns=['case', 'singular', 'plural'])

#Gathers data from the Wordnet and outputs to .jl file
def generateWordnetInflections():
    wn = Wordnet()
    logging.info("Getting wordnet data")
    with jsonlines.open('backend/server/main/wordnetInflections.jl', mode='a') as writer:
        for i, synset in enumerate(wn):
            if synset.definition != None:
                for lemma in synset.lemmas:
                    inflections_df = synthesize_all(lemma)
                    for index, row in inflections_df.iterrows():
                        if row['singular']:
                            writer.write({
                                        'name': row['singular'],
                                        'def': 'Sõna {} käändes anisuse {}'.format(lemma, row['case']),
                                    })
                        if row['plural']:
                            writer.write({
                                        'name': row['plural'],
                                        'def': 'Sõna {} käändes mitmuse {}'.format(lemma, row['case']),
                                    })

#data = getTestData()
#cleanWikiData(data)
#generateWordnetInflections()
#getWordnetData()
#print(data)
#data = getData()
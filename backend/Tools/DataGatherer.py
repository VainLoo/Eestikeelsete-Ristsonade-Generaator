import nltk
import logging
import jsonlines
import pandas as pd
import numpy as np
from estnltk import Text
from estnltk.wordnet import Wordnet
from estnltk.vabamorf.morf import synthesize

nltk.download('punkt')

ShortFormIdent = [
    "lühend",
    "lühend, mis võib tähendada järgmist:",
    "mitme nime lühend",
    "lühend, mis võib tähendada:",
    "mitmetähenduslik lühend",
    "mitme tähendusega lühend",
    "lühend, mis võib tähistada:",
    "lühend, mis võib tähendada mitut asja:",
    "lühend, mille tähendus võib olla erinev.",
    "lühend",
    "lühend, mis tähendab:",
    "kolmetäheline lühend, mis võib märkida mõnd allkirjutatut:",
    "lühend, mille all võib mõelda:",
    "lühend, mis võib tähendada näiteks:",
    "lühend, mis võib tähistada mitut mõistet:",
    "mitme asja lühend",
    "mitmetähenduslik lühend, mis võib tähendada:",
    "mitmetähenduslik sõna või lühend",
    "mitme tähendusega lühend või sõna:",
    "lühend, mille tähenduste seas on:",
    "lühend, mis võib tähistada eri mõisteid:",
    "lühend, mil on eri tähendusi:",
    "mitme asutuse lühend",
    "mitmeid asju tähistav lühend",
    "mitme asja lühend:",
    "mitmetähenduslik lühend.",
    "mitme nime lühend:",
    "mitme tähendusega lühend.",
    "mitmetähenduslik lühend:",
    "lühend:",
    "mitmetähenduslik sõna või lühend.",
    "mitme asja lühend:",
    "lühend, mis võib tähendada mitut asja.",
    "lühend, mis võib tähendada",
    "lühend, mil on mitu tähendust:",
    "mitme asutuse lühend:",
    "mitmeid asju tähistav lühend.",
    "akronüüm, millel on mitu tähendust.",
    "akronüüm, mis võib tähendada:",
    "kolmetäheline akronüüm, mis võib tähendada:",
    "akronüüm, mis võib tähendada mitut asja:",
    "akronüüm, mis võib tähendada üht järgmistest asutustest või organisatsioonidest:",
    "võib tähendada järgmist:",
    "mitmetähenduslik sõna, mis võib tähendada:",
    "teadusdistsipliinides rakendatav kontseptsioon ja võib tähendada:",
    "mitmetähenduslik sõna. See võib tähendada:",
    "tähtlühend, mis võib tähendada:",
    "võib tähendada järgmist:",
    "mitmetähenduslik sõna.",
    "mitmetähenduslik sõna, vt",
    "mitmetähenduslik sõna:",
    "mitmetähenduslik sõna",
    "mitmetähenduslik sõna. Selle all võidakse mõelda",
    "mitmetähenduslik.",
    "mitmetähenduslik",
    "mitmetähenduslik:",
    "mitmetähenduslik sõna, mis võib tähendada:",
    "itmetähenduslik mõiste:",
    "itmetähenduslik mõiste",
    "itmetähenduslik mõiste.",
    "mitmetähenduslik sõna, mis võib viidata järgnevale:",
    "mitmetähenduslik termin.",
    "mitmetähenduslik termin:",
    "mitmetähenduslik termin.",
    "eesti keeles mitmetähenduslik sõna",
    "eesti keeles mitmetähenduslik sõna.",
    "eesti keeles mitmetähenduslik sõna:",
    "mitmetähenduslik sõna, mida kasutatakse järgmistes tähendustes:",
    "mitmetähenduslik sõna ja mitme koha nimi.",
    "mitmetähenduslik sõna. Selle all võidakse mõelda",
    "mitmetähenduslik mõiste:",
    "kokkutulek') on mitmetähenduslik sõna",
    "mitmetähenduslik sõna. See võib tähendada:",
    "mitmetähenduslik sõna, mis võib tähendada",
    "mitmetähendusega sõna:",
    "mitme tähendusega lühend:",
    "mitme fraasi suurtähtlühend.",
    "mitme fraasi suurtähtlühend:",
    "mitme fraasi suurtähtlühend",
    "nimi, mis võib tähistada mitut asja:",
    "sõna, mis võib tähistada:",
    ":",
    "aga ka muid tähendusi."
]


def FilterData():
    # Loeme sisse
    data = pd.read_json('backend/Tools/Data/wordnetInflections.jl', lines=True)
    # Kaotame definitsioonide duplikaadid
    data.drop_duplicates(inplace=True)
    # Kõik suureks
    data['name'] = data['name'].str.upper()
    # Jätame alles ainult kindlate sümbolitega read
    keepPattern = '^[A-ZÜÖÄÕŠŽ ]*$'
    filtering = data['name'].str.contains(keepPattern)
    data = data[filtering]
    # Seame uued indeksid
    data.reset_index(drop=True, inplace=True)

    data = data.sort_values(ascending=False, by="name", key=lambda x: x.str.len())

    mask = (data['name'].str.len() <= 12) & (data['name'].str.len() >= 3)
    data = data.loc[mask]
    data = data.reset_index(drop=True)
    logging.info("Data row count {}".format(len(data.index)))

    logging.info("Removing unfitting")
    data['def'] = data.apply(lambda row : removeUnfitting(row), axis = 1)

    data.replace('', np.nan, inplace=True)
    data.dropna(how='any', inplace=True)

    data.reset_index(drop=True, inplace=True)

    data.to_csv('backend/Tools/finalInflections.csv', index=False)
    #print(data)

    return data

def removeUnfitting(row):
    question = row['def'].lower().strip()
    answer = row['name'].lower().split()

    if question in ShortFormIdent:
        return None

    return row['def']

def getData():

    # Loeme sisse
    data = pd.read_csv('backend/Tools/finalData.csv')

    logging.info("Data row count {}".format(len(data.index)))
    print(data.head)
    #print(data)

    return data

def cleanWikiData(data):
    logging.info("Removing anwsers from questions")
    data['def'] = data.apply(lambda row : removeAnswerFromQuestion(row), axis = 1)
    data = data.to_json(orient='records', lines=True, force_ascii=False)
    with open("backend/Tools/Data/testRes.jl", "w", encoding='utf-8') as f:
        f.write(data)



def removeAnswerFromQuestion(row):
    question = row['def']
    answer = row['name'].lower().split()
    #print(answer)
    #print(answer, question)

    tekst = Text(question)
    tekst.tag_layer(['morph_analysis'])

    found = False

    for spans in tekst.morph_analysis.rolling(window=len(answer)):
        found = False
        for indx, answerWord in enumerate(answer):
            if answerWord not in [l.lower() for l in spans[indx].lemma]:
                found = False
                break
            found = True
        if found: 
            #logging.info("FOUND appearence")

            joined = ""
            for s in spans:
               joined += s.text+" "
            joined = joined.strip() 

            #print(joined)
            question = question.replace(joined, len(joined) * "_ ")

    return question

#Gathers data from the Wordnet and outputs to .jl file
def getWordnetData():
    wn = Wordnet()
    logging.info("Getting wordnet data")
    with jsonlines.open('backend/Tools/Data/wordnetData.jl', mode='a') as writer:
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
    with jsonlines.open('backend/Tools/Data/testInflections.jl', mode='a') as writer:
        for i, synset in enumerate(wn):
            if synset.definition != None:
                for lemma in synset.lemmas:
                    inflections_df = synthesize_all(lemma)
                    for index, row in inflections_df.iterrows():
                        if row['singular']:
                            for r in row['singular'].split(", "):
                                writer.write({
                                            'name': r,
                                            'def': 'Sõna {} käändes ainsuse {}'.format(lemma, row['case']),
                                        })
                        if row['plural']:
                            for r in row['plural'].split(", "):
                                writer.write({
                                            'name': r,
                                            'def': 'Sõna {} käändes mitmuse {}'.format(lemma, row['case']),
                                        })

data = FilterData()
#cleanWikiData(data)
#generateWordnetInflections()
#getWordnetData()
#print(data)
#data = getData()
#generateWordnetInflections()
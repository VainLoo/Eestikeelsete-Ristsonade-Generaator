from cmath import log
import random
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
import numpy as np
import pandas as pd

from server.main.GridGenerator import CellInfo, createGrid, printGrid

anyChar = '[A-ZÜÖÄÕ ]|'
data = None
grid = None
words = None
allWords = []
complete = False

def getData():
    # Loeme sisse
    data = pd.read_json('server/main/defs.jl', lines=True)
    # Kaotame definitsioonide duplikaadid
    data.drop_duplicates('def', inplace=True)
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
    # print(data)
    return data


common = [
    "T",
    "L",
    "D",
    "E",
    "I",
    "S",
    "R",
    "A",
    "O",
    "Y",
    "P",
    "C",
    "N",
    "M",
]


class Word:
    def __init__(self, w="", r=None, c=""):
        if r is None:
            r = []
        self.word = w
        self.ref = r
        self.clue = c


class Words:
    def __init__(self, a=None, d=None):
        if a is None:
            self.across = {}
        if d is None:
            self.down = {}


def makeWords(length, width):
    global allWords
    allWords = []
    global complete
    words = Words()

    numberCount = 1

    for i in range(length):
        wordAdded = False

        for j in range(width):
            current: CellInfo = grid[i][j]

            if current.contents == "#":
                current.acrossMarked = True
                current.downMarked = True

            if current.acrossMarked is True and current.downMarked is True:
                continue

            # Mark across

            if not current.acrossMarked:
                if len(grid[i]) > j + 1:
                    if grid[i][j + 1].contents != "#":
                        current.acrossMarked = True
                        current.acrossNumber = numberCount

                        for x in range(1, 100):
                            try:
                                nextCell = grid[i][j + x]
                            except:
                                nextCell = None

                            if nextCell == None or nextCell.contents == "#":
                                wordAdded = True
                                w = Word()

                                for z in range(x - 1, -1, -1):
                                    w.ref.insert(0, grid[i][j + z])

                                words.across[numberCount] = w
                                break
                            else:
                                nextCell.acrossMarked = True
                                nextCell.acrossNumber = numberCount

            # Mark down words

            if not current.downMarked:
                if len(grid) > i + 1:
                    if grid[i + 1][j].contents != "#":
                        current.downMarked = True
                        current.downNumber = numberCount

                        for x in range(1, 100):
                            try:
                                nextCell = grid[i + x][j]
                            except:
                                nextCell = None

                            if nextCell == None or nextCell.contents == "#":
                                wordAdded = True

                                w = Word()

                                for z in range(x - 1, -1, -1):
                                    w.ref.insert(0, grid[i + z][j])

                                words.down[numberCount] = w
                                break
                            else:
                                nextCell = grid[i + x][j]
                                nextCell.downMarked = True
                                nextCell.downNumber = numberCount

            if wordAdded:
                wordAdded = False
                numberCount += 1

    return words


def isValidWord(result, comparison):
    return (len(result) != 0) and (result not in allWords) and (len(result) == len(comparison.ref))


def getNewWord(searchParams: str):
    # print("Got params:",searchParams)
    return data[data['name'].str.match(searchParams) == True]


def setWord(retrivedPair, word: Word):
    clue = retrivedPair['def'].values[0]
    word.clue = clue
    word.word = retrivedPair['name'].values[0]
    allWords.append(retrivedPair['name'].values[0])

    splitWord = list(word.word)
    leng = len(splitWord)

    acrossNumb = word.ref[0].acrossNumber
    downNumb = word.ref[0].downNumber
    for l in range(leng):
        if word.ref[l].acrossNumber != acrossNumb: word.ref[0].clueCellNumber = word.ref[0].downNumber
        elif word.ref[l].downNumber != downNumb: word.ref[0].clueCellNumber = word.ref[0].acrossNumber
        word.ref[l].contents = splitWord[l]


def findDownWords(word: Word):
    global words
    for m in range(len(word.ref)):
        if word.ref[m].downNumber != "":
            try:
                downWord: Word = words.down[word.ref[m].downNumber]
            except:
                print(words.down)
                print(word.ref[m])
                raise Exception("error2")
                
            count = 0

            for square in downWord.ref:
                if square.contents == "":
                    count += 1

            if count > 0:
                qParams = ((anyChar * len(downWord.ref))[:-1]).split('|')

                for indx, cell in enumerate(downWord.ref):
                    if cell.contents != "":
                        qParams[indx] = cell.contents

                qParams = ''.join(map(str, qParams))
                qParams = '^' + qParams + '$'

                downWordList = getNewWord(qParams)

                if len(downWordList) <= 0:
                    raise FileNotFoundError("No words found")

                retrivedDownPair = downWordList.sample()

                downWordList = downWordList.drop(retrivedDownPair.index)
                retrivedDownWord = retrivedDownPair['name'].values[0]

                while not isValidWord(retrivedDownWord, downWord):
                    retrivedDownPair = downWordList.sample()
                    downWordList = downWordList.drop(retrivedDownPair.index)
                    retrivedDownWord = retrivedDownPair['name'].values[0]

                #print("Valid word", retrivedDownWord)

                # Seame sõna ristsõna külge
                setWord(retrivedDownPair, downWord)


def fillRemainingDownWords():
    allDownWords = list(words.down.keys())

    for i in range(len(allDownWords)):
        current: Word = words.down[allDownWords[i]]

        if current.ref[0].contents == "":
            query = ((anyChar * len(current.ref))[:-1]).split('|')
            randIndx = random.randint(0, len(query) - 1)
            query[randIndx] = random.choice(common)

            newWordList = getNewWord(query)

            if len(newWordList) <= 0:
                raise FileNotFoundError("No words found")

            finalNewPair = newWordList.sample()
            newWordList = newWordList.drop(finalNewPair.index)
            retrivedWord = finalNewPair['name'].values[0]

            while not isValidWord(retrivedWord, current):
                finalNewPair = newWordList.sample()
                newWordList = newWordList.drop(finalNewPair.index)
                retrivedWord = finalNewPair['name'].values[0]

            setWord(finalNewPair, current)


def createWordsAndClues():
    # Loo päringu sisu

    acrossWords = list(words.across.keys())

    for i in range(len(acrossWords)):
        #print("Across I",acrossWords[i])
        #print(words.across[acrossWords[i]])
        try:
            word = words.across[acrossWords[i]]
        except:
            print(words.across)
            print(acrossWords)
            raise Exception("error")
            
        leng = len(word.ref)
        queryParams = ((anyChar * leng)[:-1]).split('|')

        count = 0

        for j in range(leng):
            if word.ref[j].contents != "":
                count += 1
                queryParams[j] = word.ref[j].contents

        if count == 0:
            randIndx = random.randint(0, len(queryParams) - 1)
            queryParams[randIndx] = random.choice(common)

        queryParams = ''.join(map(str, queryParams))
        queryParams = '^' + queryParams + '$'

        retrivedWordList = getNewWord(queryParams)
        retrivedWord: str = ""

        # print(retrivedWordList)

        if len(retrivedWordList) <= 0:
            raise FileNotFoundError("No words found")

        retrivedPair = retrivedWordList.sample()
        retrivedWordList = retrivedWordList.drop(retrivedPair.index)
        retrivedWord = retrivedPair['name'].values[0]

        while not isValidWord(retrivedWord, word):
            retrivedPair = retrivedWordList.sample()
            retrivedWordList = retrivedWordList.drop(retrivedPair.index)
            retrivedWord = retrivedPair['name'].values[0]

        #print("Valid word", retrivedWord)

        # Seame sõna ristsõna külge
        setWord(retrivedPair, word)

        findDownWords(word)

    fillRemainingDownWords()
    complete = True

    showClues()


def showClues():
    print("Vasakult paremale")
    for key, acWord in words.across.items():
        print(key,'->', acWord.word, ':', acWord.clue)

    print()
    print("Ülalt alla")
    for key, doWord in words.down.items():
        print(key,'->', doWord.word, ':', doWord.clue)


def getCrossword(length, width):
    logging.info("Starting generation")
    global data
    global grid
    global words
    data = getData()
    logging.info("Data gathered")

    while True:
        try:
            grid = createGrid(length, width)
            logging.info("Grid generated")
            words = makeWords(length, width)
            logging.info("Words generated")
            createWordsAndClues()
            logging.info("Crossword generated")
            #printGrid(grid)
            return grid, words
        except FileNotFoundError:
            logging.info("Trying again")
        except ValueError:
            logging.info("ValueError")

#grid, words = getCrossword()
#printGrid(grid)

def getGridList():
    gridList = []

    for index, row in enumerate(grid):
        gridList.append([])
        for index2, cell in enumerate(row):
            gridList[index].append(
            {
            'contents': cell.contents,
            'acrossNumber': cell.acrossNumber,
            'downNumber': cell.downNumber,
            'acrossMarked': cell.acrossMarked,
            'downMarked': cell.downMarked,
            'cords': (index, index2),
            'clueNumber': cell.clueCellNumber
            })
        #logging.info(gridList[index])
    return gridList

def getClueList():
    wordDict = {
        'across': [],
        'down': []
    }

    for key, acWord in words.across.items():
        wordDict['across'].append(
            {
            'index': key,
            'word': acWord.word,
            'clue': acWord.clue,
            'dir': 'across'
            })
        #print(acWord.word, ':', acWord.clue)

    for key, doWord in words.down.items():
        wordDict['down'].append({
            'index': key,
            'word': doWord.word,
            'clue': doWord.clue,
            'dir': 'down'
            })
        #print(doWord.word, ':', doWord.clue)

    wordDict['across'] = sorted(wordDict['across'], key = lambda i: i['index'])
    wordDict['down'] = sorted(wordDict['down'], key = lambda i: i['index'])

    return wordDict


#grid, words = getCrossword()
          


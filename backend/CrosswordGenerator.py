import random

import numpy as np
import pandas as pd

from GridGenerator import CellInfo, createGrid, printGrid

anyChar = '[A-ZÜÖÄÕ ]|'
data = None
grid = None
words = None

def getData():
    # Loeme sisse
    data = pd.read_json('defs.jl', lines=True)
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


def makeWords():
    global allWords
    global complete
    words = Words()

    numberCount = 1

    for i in range(10):
        wordAdded = False

        for j in range(10):
            current: CellInfo = grid[i][j]

            if current.contents == "#":
                current.acrossMarked = True
                current.downMarked = True

            if current.acrossMarked is True and current.downMarked is True:
                continue

            # Mark across

            if not current.acrossMarked:
                if len(grid[i]) > j + 1 and grid[i][j + 1]:
                    if grid[i][j + 1].contents != "#":
                        current.acrossNumber = numberCount

                        for x in range(1, 100):
                            try:
                                nextCell = grid[i][j + x]
                            except:
                                nextCell = None

                            if not nextCell or nextCell.contents == "#":
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
                if len(grid) > i + 1 and grid[i + 1][j]:
                    if grid[i + 1][j].contents != "#":
                        current.downNumber = numberCount

                        for x in range(100):

                            if len(grid) <= i + x or grid[i + x][j].contents == "#":
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

    allWords = []
    complete = False

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

    for l in range(leng):
        word.ref[l].contents = splitWord[l]


def findDownWords(word: Word):
    global words
    for m in range(len(word.ref)):
        if word.ref[m].downNumber != "":
            downWord: Word = words.down[word.ref[m].downNumber]

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

    bufferAmount = 3
    acrossWords = list(words.across.keys())

    for i in range(len(acrossWords)):
        word = words.across[acrossWords[i]]
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

        suffledWordList = []
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
        print(acWord.word, ':', acWord.clue)

    print()
    print("Ülalt alla")
    for key, doWord in words.down.items():
        print(doWord.word, ':', doWord.clue)


def getCrossword():
    global data
    global grid
    global words
    data = getData()
    grid = createGrid()
    words = makeWords()

    while True:
        try:
            createWordsAndClues()
            #printGrid(grid)
            return grid, words
        except FileNotFoundError:
            # print("failed")
            # printGrid(grid)
            grid = createGrid()
            words = makeWords()
        except ValueError:
            # print("failed")
            # printGrid(grid)
            grid = createGrid()
            words = makeWords()

#grid, words = getCrossword()
#printGrid(grid)

def getGridList():
    gridList = {}

    for index, row in enumerate(grid):
        gridList[index] = []
        for cell in row:
            gridList[index].append(cell.contents)
    return gridList

def getClueDict():
    wordDict = {
        "across": {},
        "down": {}
    }

    for key, acWord in words.across.items():
        wordDict["across"][key] = (acWord.word, acWord.clue)
        #print(acWord.word, ':', acWord.clue)

    for key, doWord in words.down.items():
        wordDict["down"][key] = (doWord.word, doWord.clue)
        #print(doWord.word, ':', doWord.clue)
    return wordDict
          


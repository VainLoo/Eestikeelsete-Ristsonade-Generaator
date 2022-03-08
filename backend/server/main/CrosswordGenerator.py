from ast import List
import random
import logging
from xmlrpc.client import Boolean
import time
from pandas import DataFrame
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

from server.main.DataGatherer import getData
from server.main.GridGenerator import CellInfo, createGrid, printGrid
#from DataGatherer import getData
#from GridGenerator import CellInfo, cleanGrid, createGrid, printGrid

anyChar = '[A-ZÜÖÄÕŠŽ ]|'
grid = None
words = None
allWords = []
data = None

logging.info("Getting data")
data = getData()
logging.info("Data fetched")


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
    "P",
    "N",
    "M",
]


class Word:
    def __init__(self, w="", r=None, c="", b=None, d=False):
        if r is None:
            r = []
        if b is None:
            b = []
        self.word = w
        self.ref = r
        self.clue = c
        self.backtrack = b
        self.done = d


class Words:
    def __init__(self, a=None, d=None):
        if a is None:
            self.across = {}
        if d is None:
            self.down = {}


def makeWords(length, width):
    global allWords
    allWords = []
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
    word.done = True
    allWords.append(retrivedPair['name'].values[0])

    splitWord = list(word.word)
    leng = len(splitWord)

    acrossNumb = word.ref[0].acrossNumber
    downNumb = word.ref[0].downNumber
    for l in range(leng):
        if word.ref[l].acrossNumber != acrossNumb: word.ref[0].clueCellNumber = word.ref[0].downNumber
        elif word.ref[l].downNumber != downNumb: word.ref[0].clueCellNumber = word.ref[0].acrossNumber
        word.ref[l].contents = splitWord[l]

def removeWord(word: Word):
    word.clue = ""
    allWords.remove(word.word)
    word.word = ""
    leng = len(word.ref)
    for l in range(leng):
        if l not in word.backtrack:
            word.ref[l].contents = ""
    word.done = False
    


def findDownWords(word: Word):
    global words
    m = 0
    while m < len(word.ref):
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
                    for refIndx in range(m, -1, -1):
                        if refIndx == 0:
                            backer: Word = word
                            return False
                        if word.ref[m].downNumber != "":
                            backer: Word = words.down[word.ref[m].downNumber]
                            for cell in backer.ref:
                                cell.contents = ""
                                m = refIndx
                                continue


                    #raise FileNotFoundError("No words found")

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

        m += 1


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

def chooseWord(word: Word, retrivedWordList):
    if len(retrivedWordList) <= 0:
        return False, retrivedWordList
    retrivedPair = retrivedWordList.sample()
    retrivedWordList = retrivedWordList.drop(retrivedPair.index)
    retrivedWord = retrivedPair['name'].values[0]

    while not isValidWord(retrivedWord, word):
        if len(retrivedWordList) <= 0:
            return False, retrivedWordList
        retrivedPair = retrivedWordList.sample()
        retrivedWordList = retrivedWordList.drop(retrivedPair.index)
        retrivedWord = retrivedPair['name'].values[0]
    setWord(retrivedPair, word)
    return True, retrivedWordList


def recursionFill(word: Word, isAcross: bool, acrossIndx: int, downIndx: int, acrossKeys: List, downKeys: List):

    leng = len(word.ref)
    queryParams = ((anyChar * leng)[:-1]).split('|')

    count = 0
    word.backtrack.clear()
    for j in range(leng):
        if word.ref[j].contents != "":
            word.backtrack.append(j)
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
        return False
        raise FileNotFoundError("No words found")
    
    retrivedPair = retrivedWordList.sample()
    retrivedWordList = retrivedWordList.drop(retrivedPair.index)
    retrivedWord = retrivedPair['name'].values[0]

    while not isValidWord(retrivedWord, word):
        if len(retrivedWordList) <= 0:
            return False
        retrivedPair = retrivedWordList.sample()
        retrivedWordList = retrivedWordList.drop(retrivedPair.index)
        retrivedWord = retrivedPair['name'].values[0]

    # Seame sõna ristsõna külge
    setWord(retrivedPair, word)
    #printGrid(grid)
    gotWord = True

    if isAcross:
        for indx, cell in enumerate(word.ref):
            if cell.downMarked:
                w = words.down[cell.downNumber]
                if not w.done:
                    tries = 0
                    while True:
                        if tries >= 10:
                            removeWord(word)
                            #printGrid(grid)
                            return False
                        if not recursionFill(w, not isAcross, acrossIndx, downIndx+1, acrossKeys, downKeys):
                            tries+=1
                            removeWord(word)
                            gotWord, retrivedWordList = chooseWord(word, retrivedWordList)
                            #printGrid(grid)
                            if not gotWord: return False 
                        else:
                            word.backtrack.append(indx)
                            break
    else:
        for indx, cell in enumerate(word.ref):
            if cell.acrossMarked:
                w = words.across[cell.acrossNumber]
                if not w.done:
                    tries = 0
                    while True:
                        if tries >= 30:
                            removeWord(word)
                            #printGrid(grid)
                            return False
                        if not recursionFill(w, not isAcross, acrossIndx+1, downIndx, acrossKeys, downKeys):
                            tries+=1
                            removeWord(word)
                            gotWord, retrivedWordList = chooseWord(word, retrivedWordList)
                            #printGrid(grid)
                            if not gotWord: return False
                        else:           
                            word.backtrack.append(indx)  
                            break
    return True

def createWordsAndClues():
    # Loo päringu sisu

    acrossWords = list(words.across.keys())
    i = 0
    while i < len(acrossWords):
        #print("Across I",acrossWords[i])
        #print(words.across[acrossWords[i]])
        try:
            word: Word = words.across[acrossWords[i]]
        except:
            print(words.across)
            print(acrossWords)
            raise Exception("error")
            
        leng = len(word.ref)
        queryParams = ((anyChar * leng)[:-1]).split('|')

        count = 0

        for j in range(leng):
            if word.ref[j].contents != "":
                word.backtrack.append(word.ref[j].contents)
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

        if not findDownWords(word):
            for indx, cell in enumerate(word.ref):
                if indx not in word.backtrack:
                    cell.contents = ""
                i -= 1
                continue

        i += 1

    fillRemainingDownWords()


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
    global grid
    global words
    
    while True:
        #try:
        grid = createGrid(length, width)
        logging.info("Grid generated")
        words = makeWords(length, width)
        logging.info("Words generated")
        #createWordsAndClues()
        aKeys = list(words.across.keys())
        bKeys = list(words.down.keys())
        recursionFill(word=words.across[aKeys[0]], isAcross=True, acrossIndx=0, downIndx=0, acrossKeys=aKeys, downKeys=bKeys)
        return grid, words
        #except FileNotFoundError:
            #logging.info("Trying again")
        #except ValueError:
            #logging.info("ValueError")

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
        

    for key, doWord in words.down.items():
        wordDict['down'].append({
            'index': key,
            'word': doWord.word,
            'clue': doWord.clue,
            'dir': 'down'
            })
        

    wordDict['across'] = sorted(wordDict['across'], key = lambda i: i['index'])
    wordDict['down'] = sorted(wordDict['down'], key = lambda i: i['index'])

    return wordDict


#start = time.time()
#grid, words = getCrossword(6,7)
#end = time.time()
#logging.info("AJAKULU: {}".format(end - start))

#printGrid(grid)
#showClues()


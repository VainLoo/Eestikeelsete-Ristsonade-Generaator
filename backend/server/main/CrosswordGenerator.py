from weakref import ref
from server.main.GridGenerator import CellInfo, createGrid, printGrid
from server.main.DataGatherer import getData
import logging

#from DataGatherer import getData
#from GridGenerator import CellInfo, cleanGrid, createGrid, printGrid

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

anyChar = '[A-ZÜÖÄÕŠŽ ]|'
grid = None
words = None
allWords = []
data = None

logging.info("Getting data")
data = getData()
logging.info("Data fetched")

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


def recursionFill(word: Word, isAcross: bool):

    leng = len(word.ref)
    queryParams = ((anyChar * leng)[:-1]).split('|')

    word.backtrack.clear()
    for j in range(leng):
        if word.ref[j].contents != "":
            word.backtrack.append(j)
            queryParams[j] = word.ref[j].contents

    queryParams = ''.join(map(str, queryParams))
    queryParams = '^' + queryParams + '$'

    retrivedWordList = getNewWord(queryParams)
    retrivedWord: str = ""

    # print(retrivedWordList)

    if len(retrivedWordList) <= 0:
        return False
    
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
                        if tries >= 30:
                            removeWord(word)
                            #printGrid(grid)
                            return False
                        if not recursionFill(w, not isAcross):
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
                        if not recursionFill(w, not isAcross):
                            tries+=1
                            removeWord(word)
                            gotWord, retrivedWordList = chooseWord(word, retrivedWordList)
                            #printGrid(grid)
                            if not gotWord: return False
                        else:           
                            word.backtrack.append(indx)  
                            break
    return True


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
    
    grid = createGrid(length, width)
    logging.info("Grid generated")
    words = makeWords(length, width)
    logging.info("Words generated")
    checkWords(words)
    logging.info("Word length checked")
    recursionFill(word=words.across[list(words.across.keys())[0]], isAcross=True)
    logging.info("Crossword filled")
    checkWordsFilled(words)
    logging.info("Words fill checked")
    return grid, words


def checkWords(words: Words):
    for key, aw in words.across.items():
        if len(aw.ref) <= 2:
            raise Exception("Too short word")
    for key, dw in words.down.items():
        if len(dw.ref) <= 2:
            raise Exception("Too short word")

def checkWordsFilled(words: Words):
    for key, aw in words.across.items():
        if len(aw.word) <= 0:
            raise Exception("Not every word filled")
    for key, dw in words.down.items():
        if len(dw.word) <= 0:
            raise Exception("Not every word filled")

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
#grid, words = getCrossword(12,12)
#end = time.time()
#logging.info("AJAKULU: {}".format(end - start))

#printGrid(grid)
#showClues()


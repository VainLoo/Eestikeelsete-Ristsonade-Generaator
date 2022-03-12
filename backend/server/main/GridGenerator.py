import numpy as np
import random
import math

blackSqCount = 0
letterCount = 0


class CellInfo:
    contents = ""
    acrossNumber = ""
    downNumber = ""
    clueCellNumber = ""
    acrossMarked = False
    downMarked = False
    opposite = None
    above = None
    below = None
    prev = None
    next = None

def printGrid(grid, header="default"):
    print(header)
    print('\n'.join([''.join(['{:4}'.format(item.contents) for item in row])
                     for row in grid]))


def preventBlockedWhiteSquares(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            curCell = grid[i][j]

            blocked = ((not curCell.above or curCell.above.contents == "#") and
                       (not curCell.below or curCell.below.contents == "#") and
                       (not curCell.prev or curCell.prev.contents == "#") and
                       (not curCell.next or curCell.next.contents == "#"))
            if blocked:
                surrounding = []

                curCell.above and surrounding.append([curCell.above, curCell.above.opposite])
                curCell.below and surrounding.append([curCell.below, curCell.below.opposite])
                curCell.prev and surrounding.append([curCell.prev, curCell.prev.opposite])
                curCell.next and surrounding.append([curCell.next, curCell.next.opposite])

                if len(surrounding) > 0:
                    index = random.randint(0, len(surrounding) - 1)
                    for cellinfo in surrounding[index]:
                        cellinfo.contents = ""


def processTwoLetterWords(i: int, j: int, direction, grid):
    curCell: CellInfo = grid[i][j] if direction == "across" else grid[j][i]
    global letterCount

    if curCell.contents == "":
        letterCount += 1

    if letterCount == 2 and curCell.contents == "#":
        curCell.contents = ""
        curCell.opposite.contents = ""
        letterCount = 0

    if curCell.contents == "#":
        letterCount = 0


def eliminateTwoLetterWords(grid):
    global letterCount
    # vasakult paremale, ülevalt alla
    for i in range(len(grid)):
        letterCount = 0
        for j in range(len(grid[0])):
            processTwoLetterWords(i, j, "across", grid)

    # paremalt vasakule, alt ülesse
    for i in range(math.floor(len(grid)/2)-1, -1, -1):
        letterCount = 0
        for j in range(len(grid[0])-1, -1, -1):
            processTwoLetterWords(i, j, "across", grid)

    # Ülevalt alla, vasakult paremale
    for j in range(len(grid[0])):
        letterCount = 0
        for i in range(len(grid)):
            processTwoLetterWords(j, i, "down", grid)

    # alt ülesse, paremalt vasakule
    for j in range(len(grid[0])-1, -1, -1):
        letterCount = 0
        for i in range(len(grid)-1, -1, -1):
            processTwoLetterWords(j, i, "down", grid)


def processDisjointedWordsDown(rowCount: int, colCount: int, grid):
    for i in range(colCount):
        for j in range(rowCount):

            if j >= rowCount:
                    break

            curCell: CellInfo = grid[j][i]
            if curCell.contents != "#":
                count = 1
                disconnected = 0
                checking = True
                blackSquareArr = []

                while (checking and j < rowCount):
                    currentGridItem = None
                    nextGridItem = None
                    try:
                        currentGridItem = grid[j + (count - 1)][i]
                        nextGridItem = grid[j + count][i]
                    except:
                        nextGridItem = None

                    a = currentGridItem.prev
                    b = currentGridItem.next

                    if nextGridItem is not None and nextGridItem.contents != "#":
                        count += 1
                    else:
                        checking = False

                    if (not a or a.contents == "#") and (not b or b.contents == "#"):
                        disconnected += 1
                        if a:
                            blackSquareArr.append(a)
                        if b:
                            blackSquareArr.append(b)

                if disconnected == count and count > 1:
                    targetSquare: CellInfo = blackSquareArr[random.randint(0, len(blackSquareArr) - 1)]
                    targetSquare.contents = ""
                    targetSquare.opposite.contents = ""
                j += count
            else:
                continue


def processDisjointedWordsAcross(rowCount: int, colCount: int, grid):
    for i in range(rowCount):
        for j in range(colCount):

            if i >= rowCount:
                break

            curCell: CellInfo = grid[i][j]

            if curCell.contents != "#":
                count = 1
                disconnected = 0
                checking = True
                blackSquareArr = []

                while (checking and j < colCount):
                    currentGridItem = None
                    nextGridItem = None
                    try:
                        currentGridItem = grid[i][j + (count - 1)]
                        nextGridItem = grid[i][j + count]
                    except:
                        nextGridItem = None

                    a = currentGridItem.above
                    b = currentGridItem.below

                    if nextGridItem is not None and nextGridItem.contents != "#":
                        count += 1
                    else:
                        checking = False

                    if (not a or a.contents == "#") and (not b or b.contents == "#"):
                        disconnected += 1
                        if a:
                            blackSquareArr.append(a)
                        if b:
                            blackSquareArr.append(b)

                if disconnected == count and count > 1:
                    targetSquare: CellInfo = blackSquareArr[random.randint(0, len(blackSquareArr) - 1)]
                    targetSquare.contents = ""
                    targetSquare.opposite.contents = ""
                j += count
            else:
                continue

# Reduce large blocks of white spaces
def reduceLargeWhiteSquares(length, width, grid):
    for i in range(1, length-1):
        for j in range(1, width-1):
            curCell: CellInfo = grid[i][j]

            nineSquare = [
                grid[i - 1][j - 1],
                curCell.above,
                grid[i - 1][j + 1],
                grid[i + 1][j - 1],
                curCell.below,
                grid[i + 1][j + 1],
                curCell.prev,
                curCell.next,
                curCell
            ]

            whiteSquareCount = 0

            for cell in nineSquare:
                if cell.contents != "#": whiteSquareCount += 1

            if whiteSquareCount > 7:
                curCell.contents = "#"
                curCell.opposite.contents = "#"

def cleanGrid(grid):
    for row in grid:
        for cell in row:
            if cell.contents != "#":
                cell.contents = ""



def createGrid(length, width):
    global blackSqCount
    global letterCount

    blackSqCount = 0
    letterCount = 0

    grid = np.empty(length, dtype=object)

    for i in range(length):
        grid[i] = np.empty(width, dtype=CellInfo)

    for i in range(length):
        for j in range(width):
            grid[i][j] = CellInfo()

    for i in range(length):
        for j in range(width):
            grid[i][j].opposite = grid[length - 1 - i][width - 1 - j]
            grid[i][j].above = grid[i - 1][j] if i > 0 else False
            grid[i][j].below = grid[i + 1][j] if i < length-1 else False
            grid[i][j].prev = grid[i][j - 1] if j > 0 else False
            grid[i][j].next = grid[i][j + 1] if j < width-1 else False

    while blackSqCount < (length*width*0.4):
        for i in range(math.floor(length/2)):
            for j in range(width):
                rand = random.random()
                # print("random:", rand)
                if rand < 0.7:
                    grid[i][j].contents = "#"
                    grid[length - 1 - i][width - 1 - j].contents = "#"

                    blackSqCount += 2

                    if blackSqCount > (length*width*0.8)-1:
                        break

    #printGrid(grid, "first grid")
    preventBlockedWhiteSquares(grid)
    #printGrid(grid, "Prevent Blocked White Squares")

    eliminateTwoLetterWords(grid)
    #printGrid(grid, "Eliminate Two letter words")

    reduceLargeWhiteSquares(length, width, grid)

    preventBlockedWhiteSquares(grid)
    #printGrid(grid, "Prevent Blocked White Squares")
    processDisjointedWordsAcross(length, width, grid)
    processDisjointedWordsDown(length, width, grid)
    #printGrid(grid, "Process Disjointed Words")

    eliminateTwoLetterWords(grid)
    #printGrid(grid, "Reeliminate two letter words")

    return grid

#g = createGrid(7,6)
#printGrid(g)
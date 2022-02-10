import pandas as pd
import numpy as np
import random

size = 10
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
    for i in range(5):
        for j in range(10):
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
    for i in range(5):
        letterCount = 0
        for j in range(10):
            processTwoLetterWords(i, j, "across", grid)

    # paremalt vasakule, alt ülesse
    for i in range(4, -1, -1):
        letterCount = 0
        for j in range(9, -1, -1):
            processTwoLetterWords(i, j, "across", grid)

    # Ülevalt alla, vasakult paremale
    for j in range(10):
        letterCount = 0
        for i in range(5):
            processTwoLetterWords(j, i, "down", grid)

    # alt ülesse, paremalt vasakule
    for j in range(9, -1, -1):
        letterCount = 0
        for i in range(4, -1, -1):
            processTwoLetterWords(j, i, "down", grid)


def processDisjointedWords(rowCount: int, colCount: int, direction: str, grid):
    for i in range(rowCount):
        for j in range(colCount):
            if direction == "across":
                if i >= rowCount:
                    break
            else:
                if j >= rowCount:
                    break

            curCell: CellInfo = grid[i][j] if direction == "across" else grid[j][i]
            if curCell.contents != "#":
                count = 1
                disconnected = 0
                checking = True
                blackSquareArr = []

                while (checking and j < colCount):
                    currentGridItem = None
                    nextGridItem = None
                    try:
                        currentGridItem = grid[i][j + (count - 1)] if direction == "across" else \
                            grid[j + (count - 1)][i]
                        nextGridItem = grid[i][j + count] if direction == "across" else grid[j + count][i]
                    except:
                        nextGridItem = None

                    a = currentGridItem.above if direction == "across" else currentGridItem.prev
                    b = currentGridItem.below if direction == "across" else currentGridItem.next

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


def createGrid():
    global blackSqCount
    global letterCount
    global size

    size = 10
    blackSqCount = 0
    letterCount = 0

    grid = np.empty(size, dtype=object)

    for i in range(size):
        grid[i] = np.empty(size, dtype=CellInfo)

    for i in range(size):
        for j in range(size):
            grid[i][j] = CellInfo()

    for i in range(size):
        for j in range(size):
            grid[i][j].opposite = grid[size - 1 - i][size - 1 - j]
            grid[i][j].above = grid[i - 1][j] if i > 0 else False
            grid[i][j].below = grid[i + 1][j] if i < 9 else False
            grid[i][j].prev = grid[i][j - 1] if j > 0 else False
            grid[i][j].next = grid[i][j + 1] if j < 9 else False

    while blackSqCount < 80:
        for i in range(5):
            for j in range(10):
                rand = random.random()
                # print("random:", rand)
                if rand < 0.7:
                    grid[i][j].contents = "#"
                    grid[size - 1 - i][size - 1 - j].contents = "#"

                    blackSqCount += 2

                    if blackSqCount > 79:
                        break

    #printGrid(grid, "first grid")
    preventBlockedWhiteSquares(grid)
    #printGrid(grid, "Prevent Blocked White Squares")

    eliminateTwoLetterWords(grid)
    #printGrid(grid, "Eliminate Two letter words")

    # Reduce large blocks of white spaces
    for i in range(1, 5):
        for j in range(1, 9):
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

    preventBlockedWhiteSquares(grid)
    #printGrid(grid, "Prevent Blocked White Squares")

    processDisjointedWords(5, 10, "across", grid)
    processDisjointedWords(10, 5, "down", grid)
    #printGrid(grid, "Process Disjointed Words")

    eliminateTwoLetterWords(grid)
    #printGrid(grid, "Reeliminate two letter words")

    return grid


# escape level editor, by Eric Manning
# created Jul 30, 2023

import curses
from curses import wrapper
from Levels import levels
from curses.textpad import rectangle
from subprocess import call

enemiesList = ["!", "@", "%", "Z"]
cursorValue = "O"
wallCorner = [15, 30]
levelMap = [
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
]

# print screen function
def printScreen(stdscr, cursorLoc):
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    blackred = curses.color_pair(3)
    blackwhite = curses.color_pair(4)
    redmagenta = curses.color_pair(5)
    white = curses.color_pair(6)
    red = curses.color_pair(7)
    whitemagenta = curses.color_pair(8)
    stdscr.clear()
    rectangle(stdscr, 0, 0, 15, 29)
    for i, row in enumerate(levelMap):
        for j, value in enumerate(row):
            iPrintPos, jPrintPos = i + 1, j * 2 + 1
            if value == "O":
                stdscr.addstr(iPrintPos, jPrintPos, "O", cyan | curses.A_BOLD)
            elif value == "#" or value == "9":
                stdscr.addstr(iPrintPos, jPrintPos, "▧", white)
            elif value == "X":
                stdscr.addstr(iPrintPos, jPrintPos, "X", blackred | curses.A_BOLD)
            elif value in enemiesList:
                stdscr.addstr(iPrintPos, jPrintPos, value, red | curses.A_BOLD)
    stdscr.addstr(cursorLoc[0], cursorLoc[1], cursorValue, blackwhite)
    stdscr.refresh()

# move cursor funciton
def moveCursor(stdscr, cursorLoc, direction):
    if direction == "up" and cursorLoc[0] > 1:
        cursorLoc[0] -= 1
    elif direction == "down" and cursorLoc[0] < 14:
        cursorLoc[0] += 1
    elif direction == "left" and cursorLoc[1] > 1:
        cursorLoc[1] -= 2
    elif direction == "right" and cursorLoc[1] < 27:
        cursorLoc[1] += 2
    printScreen(stdscr, cursorLoc)

# change cursor function
def changeCursor(stdscr, cursorLoc, direction):
    global cursorValue
    cursors = ["O", "X", "▧", "#", "!", "@", "%", "Z"]

    for index, c in enumerate(cursors):
        if c == cursorValue:
            startIndex = index
    
    if direction == "next":
        endIndex = startIndex + 1
        if startIndex == len(cursors) - 1:
            endIndex = 0
    elif direction == "previous":
        endIndex = startIndex - 1
        if startIndex == 0:
            endIndex = len(cursors) - 1
            
    cursorValue = cursors[endIndex]
    printScreen(stdscr, cursorLoc)

# place item function
def placeItem(stdscr, cursorLoc):
    global levelmap, wallCorner

    # wall item
    if cursorValue == "▧":
        wallCorner = [cursorLoc[0], cursorLoc[1]]
        for i, row in enumerate(levelMap):
            for j, value in enumerate(row):
                if levelMap[i][j] == "#":
                    levelMap[i][j] = " "
                if i == cursorLoc[0] - 1 or j == int((cursorLoc[1] - 1) / 2):
                    levelMap[i][j] = "#"
                if i > cursorLoc[0] - 1 or j > int((cursorLoc[1] - 1) / 2):
                    levelMap[i][j] = " "

    # check if cursor within walls
    if cursorLoc[0] < wallCorner[0] and cursorLoc[1] < wallCorner[1]:

        # player item
        if cursorValue == "O":
            for i, row in enumerate(levelMap):
                for j, value in enumerate(row):
                    if levelMap[i][j] == "O":
                        levelMap[i][j] = " "
            levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = "O"

        # inner wall item
        if cursorValue == "#":
            levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = "9"

        # finish item
        if cursorValue == "X":
            for i, row in enumerate(levelMap):
                for j, value in enumerate(row):
                    if levelMap[i][j] == "X":
                        levelMap[i][j] = " "
            levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = "X"

        # enemy 1 item
        if cursorValue == "!":
            for i, row in enumerate(levelMap):
                for j, value in enumerate(row):
                    if levelMap[i][j] == "!":
                        levelMap[i][j] = " "
            levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = "!"

        # enemy 2 item
        if cursorValue == "@":
            for i, row in enumerate(levelMap):
                for j, value in enumerate(row):
                    if levelMap[i][j] == "@":
                        levelMap[i][j] = " "
            levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = "@"

        # enemy 3 item
        if cursorValue == "%":
            for i, row in enumerate(levelMap):
                for j, value in enumerate(row):
                    if levelMap[i][j] == "%":
                        levelMap[i][j] = " "
            levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = "%"

        # enemy 4 item
        if cursorValue == "Z":
            for i, row in enumerate(levelMap):
                for j, value in enumerate(row):
                    if levelMap[i][j] == "Z":
                        levelMap[i][j] = " "
            levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = "Z"

    printScreen(stdscr, cursorLoc)

# delete item function
def delItem(stdscr, cursorLoc):
    global levelmap, wallCorner
    if cursorLoc[0] < wallCorner[0] and cursorLoc[1] < wallCorner[1]:
        levelMap[cursorLoc[0] - 1][int((cursorLoc[1] - 1) / 2)] = " "

# make level list function
def makeLevelList(stdscr):
    newLevelMap = list(levelMap)
    wallCornerIndex = [wallCorner[0] - 1, wallCorner[1] / 2 - 1]
    try:
        for i, row in enumerate(newLevelMap):
            if i >= wallCornerIndex[0]:
                del newLevelMap[i:len(newLevelMap)]
    except:
        pass
    try:
        for i, row in enumerate(newLevelMap):
            for j, value in enumerate(row):
                if j >= wallCornerIndex[1]:
                    del newLevelMap[j:len(newLevelMap)]
    except:
        pass

# main function
def main(stdscr):

    # color initialization
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    cursorLoc = [1, 1]
    printScreen(stdscr, cursorLoc)

    key = stdscr.getch()
    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP:
            moveCursor(stdscr, cursorLoc, "up")
        elif key == curses.KEY_DOWN:
            moveCursor(stdscr, cursorLoc, "down")
        elif key == curses.KEY_LEFT:
            moveCursor(stdscr, cursorLoc, "left")
        elif key == curses.KEY_RIGHT:
            moveCursor(stdscr, cursorLoc, "right")
        elif key == ord("n"):
            changeCursor(stdscr, cursorLoc, "next")
        elif key == ord("p"):
            changeCursor(stdscr, cursorLoc, "previous")
        elif key == ord(" "):
            placeItem(stdscr, cursorLoc)
        elif key == ord("d"):
            delItem(stdscr, cursorLoc)
        elif key == ord("r"):

            # Run the other script
            call(["python", "Escape.py"])
        elif key == ord("t"):
            makeLevelList(stdscr)

            # Run the other script
            call(["python", "TestLevel.py"])
        elif key == 27:
            break
        else:
            continue

wrapper(main)
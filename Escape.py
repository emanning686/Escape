# escape, by Eric Manning
# created Apr 2, 2023

import curses
from curses import wrapper
import queue
import copy
import time
from curses.textpad import rectangle
from subprocess import call
import ast

# create levels list from file
levels = []
with open('Levels.txt', 'r') as filehandle:
    for line in filehandle:
        currentPlace = line[:-1]
        levels.append(currentPlace)

for i, row in enumerate(levels):
    levels[i] = ast.literal_eval(row)

# function to refresh the level using the screen config in printLevel
def refreshLevel(level, stdscr, enemiesList, levelNum, moves, rectangleMode, pathsList):
    stdscr.clear()
    printLevel(level, stdscr, enemiesList, levelNum, moves, rectangleMode)
    # path debug
    # printLevel(level, stdscr, enemiesList, levelNum, moves, rectangleMode, pathsList)
    stdscr.refresh()

# function to configure the screen, can show the bredth first search paths
def printLevel(level, stdscr, enemiesList, levelNum, moves, rectangleMode, pathsList = []):
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    blackred = curses.color_pair(3)
    blackwhite = curses.color_pair(4)
    redmagenta = curses.color_pair(5)
    white = curses.color_pair(6)
    red = curses.color_pair(7)
    topLeftFound = False
    for i, row in enumerate(level):
        for j, value in enumerate(row):
            iPrintPos, jPrintPos = i + 1, (j + 1) * 2
            if pathsList != None: 
                for path in pathsList:
                    if path != None:
                        if (i, j) in path:
                            stdscr.addstr(iPrintPos, jPrintPos, "&", redmagenta)
            if value == "#":
                stdscr.addstr(iPrintPos, jPrintPos, "▧", white)
                if topLeftFound == False:
                    topLeftFound = True
                    topLeftX, topLeftY = iPrintPos, jPrintPos
            elif value == "X":
                stdscr.addstr(iPrintPos, jPrintPos, value, blackred | curses.A_BOLD)
            elif value == "O":
                stdscr.addstr(iPrintPos, jPrintPos, value, cyan | curses.A_BOLD)
            for enemy in enemiesList:
                if value == enemy:
                    stdscr.addstr(iPrintPos, jPrintPos, value, red | curses.A_BOLD)

    if rectangleMode == True:
        stdscr.attron(redmagenta)
        rectangle(stdscr, topLeftX, topLeftY, len(level), len(level[0]) * 2)
        stdscr.attroff(redmagenta)
    currentCol = len(level[0]) * 2 + 1
    stdscr.addstr(1, currentCol + 1, "level: " + str(levelNum), blackwhite)
    stdscr.addstr(2, currentCol + 1, "moves: " + str(moves), blackwhite)

# function to find the matrix location of a character, doesn't work with multiple, returns
# none if none exist
def findLocation(level, character):
    for i, row in enumerate(level):
        for j, value in enumerate(row):
            if value == character:
                return i, j
    return None

# function to find the fastest path from one point to another on the matrix grid, bredth
# first search method
def findPath(level, start, end, enemiesList):
    startPos = findLocation(level, start)

    q = queue.Queue()
    q.put((startPos, [startPos]))

    visited = set()

    # loops until all the neighbors and paths have been checked and returns the best path
    while not q.empty():
        currentPos, path = q.get()
        row, col = currentPos

        if level[row][col] == end:
            return path
        
        neighbors = findNeighbors(level, row, col)
        for neighbor in neighbors:
            r, c = neighbor
            if neighbor in visited:
                continue
            if level[r][c] == "#":
                continue
            if level[r][c] == "X":
                continue
            for enemy in enemiesList:
                if level[r][c] == enemy:
                    continue

            newPath = path + [neighbor]
            q.put((neighbor, newPath))
            visited.add(neighbor)

# function to get all the valid neighbors for the breadth first search
def findNeighbors(level, row, col):
    neighbors = []

    if row > 0: # up
        neighbors.append((row - 1, col))
    if row + 1 < len(level): # down
        neighbors.append((row + 1, col))
    if col > 0: # left
        neighbors.append((row, col - 1))
    if col + 1 < len(level[0]): # right
        neighbors.append((row, col + 1))

    return neighbors

# function to swap the position of an enemy with the spot first on the breadth first
# search path to the player
def moveEnemy(level, path, enemy):
    oldrow, oldcol = 10000, 10000
    try:
        oldrow, oldcol = findLocation(level, enemy)
    except TypeError:
        pass

    newrow, newcol = path[1]
    
    try:
        level[oldrow][oldcol] = " "
    except IndexError:
        pass
    level[newrow][newcol] = enemy

# function to move the play based on their input
def movePlayer(direction, level, player):
    oldrow, oldcol = findLocation(level, player)
    if direction == "up" and oldrow > 0: # up
        newrow, newcol = oldrow - 1, oldcol
    elif direction == "down" and  oldrow + 1 < len(level): # down
        newrow, newcol = oldrow + 1, oldcol
    elif direction == "left" and  oldcol > 0: # left
        newrow, newcol = oldrow, oldcol - 1
    elif direction == "right" and  oldcol + 1 < len(level[0]): # right
        newrow, newcol = oldrow, oldcol + 1
    else:
        return False

    # checks to make sure the spot the player is moving is not a wall and also returns
    # "escape" if the player has reached the endpoint
    newPosChar = level[newrow][newcol]
    if newPosChar == " ":
        level[oldrow][oldcol] = " "
        level[newrow][newcol] = player
    elif newPosChar == "X":
        level[oldrow][oldcol] = " "
        level[newrow][newcol] = player
        return "escape"
    elif newPosChar == "#":
        return False

    return True

# function to check if the player character is in the matrix
def checkLose(level, player):
    for row in level:
        for value in row:
            if value == player:
                return False
    return True

# function to display the window for if the player loses
def loseWindow(stdscr):
    magenta = curses.color_pair(2)
    stdscr.clear()
    stdscr.addstr(1, 6, "you lost!", magenta)
    stdscr.refresh()
    time.sleep(0.5)
    stdscr.addstr(2, 6, "press space to play again", magenta)
    stdscr.refresh()
    time.sleep(0.5)
    stdscr.addstr(3, 6, "or escape to quit", magenta)
    stdscr.refresh()

# function to display the window for if the player wins
def winWindow(stdscr, movesList):
    magenta = curses.color_pair(2)
    stdscr.clear()
    stdscr.addstr(1, 6, "you escaped the final room!", magenta)
    stdscr.refresh()
    row = 3
    for i, moves in enumerate(movesList):
        time.sleep(0.5)
        levelString = f"Level {str(i + 1)}: {str(moves).zfill(3)}"
        if i % 2 == 0:
            stdscr.addstr(row, 6, levelString, magenta)
        if i % 2 == 1:
            stdscr.addstr(row, 21, levelString, magenta)
            row += 1
        stdscr.refresh()
    if len(movesList) % 2 == 1:
        row += 1
    row += 1
    time.sleep(0.5)
    stdscr.addstr(row, 6, "press space to play again", magenta)
    stdscr.refresh()
    row += 1
    time.sleep(0.5)
    stdscr.addstr(row, 6, "or escape to quit", magenta)
    stdscr.refresh()

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

    # title screen 
    whitemagenta = curses.color_pair(8)
    stdscr.clear()
    stdscr.addstr(1, 6, "  ___  ___  ___ __ _ _ __   ___..", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(2, 6, " / _ \/ __|/ __/ _` | '_ \ / _ \ ", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(3, 6, "|  __/\__ \ (_| (_| | |_) |  __/.", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(4, 6, " \___||___/\___\__,_| .__/ \___|.", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(5, 6, "                    |_|         .", whitemagenta)
    stdscr.refresh()
    time.sleep(1)

    stdscr.clear()
    stdscr.addstr(1, 6, "Press", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(2, 12, "space", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(1, 18, "to", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(2, 21, "start", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(5, 6, "Press", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(4, 12, "E", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(5, 14, "to", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(4, 17, "edit", whitemagenta)
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(5, 22, "level", whitemagenta)
    stdscr.refresh()

    while True:
        homeInput = stdscr.getch()
        if homeInput == ord("e"):
            call(["python", "LevelEditor.py"])
            
        elif homeInput == ord(" "):
            break
        else:
            continue

    # variables that need to be initialized before the main loop
    levelStart = 0
    levelIndex = levelStart
    movesList = []
    rectangleMode = False
    enemiesList = ["!", "@", "%", "Z"]
    player = "O"
    endProgram = False

    # main loop
    while True:
        moves = 0

        # checks if there are any remaining levels, if not, displays the win window
        if levelIndex <= len(levels) - 1:
            level = copy.deepcopy(levels[levelIndex])
        else:
            time.sleep(1)
            winWindow(stdscr, movesList)
            while True:
                key = stdscr.getch()
                if key == ord(" "):
                    levelIndex = levelStart
                    movesList = []
                    break
                elif key == 27:
                    endProgram = True
                    break
            if endProgram == True:
                break
            continue

        # level loop, loops until the level ends by loss or finish
        while True:
            pathsList = []
            for enemy in enemiesList:
                if findLocation(level, enemy)!= None:
                    pathsList.append(findPath(level, enemy, player, enemiesList))
            refreshLevel(level, stdscr, enemiesList, levelIndex + 1, moves, rectangleMode, pathsList)

            # checks if the player has lost
            lossed = checkLose(level, player)
            if lossed:
                time.sleep(1)
                loseWindow(stdscr)
                while True:
                    key = stdscr.getch()
                    if key == ord(" "):
                        levelIndex = levelStart
                        movesList = []
                        break
                    elif key == 27:
                        endProgram = True
                        break
                
                break
            else:

                # player input loop
                while True:
                    goodMove = None
                    key = stdscr.getch()
                    if key == curses.KEY_UP:
                        goodMove = movePlayer("up", level, player)
                    elif key == curses.KEY_DOWN:
                        goodMove = movePlayer("down", level, player)
                    elif key == curses.KEY_LEFT:
                        goodMove = movePlayer("left", level, player)
                    elif key == curses.KEY_RIGHT:
                        goodMove = movePlayer("right", level, player)
                    elif key == ord("0"):
                        rectangleMode = not rectangleMode
                    elif key == 27:
                        endProgram = True
                    else:
                        continue

                    if goodMove == False:
                        continue

                    # what to do if the move is good, mainly just checks for every living
                    # enemy and moves them before restarting the loop
                    elif goodMove == True:
                        LivingEnemies = []
                        for enemy in enemiesList:
                            isAlive = findLocation(level, enemy)
                            if isAlive != None:
                                LivingEnemies.append(enemy)
                        for i, enemy in enumerate(LivingEnemies):
                            moveEnemy(level, pathsList[i], enemy)
                        moves += 1
                        break
                    elif goodMove == "escape":
                        levelIndex += 1
                        moves += 1
                        movesList.append(moves)
                        break
                    if endProgram == True:
                        break
                if goodMove == "escape":
                    break
                if endProgram == True:
                    break
        if endProgram == True:
            break

wrapper(main)
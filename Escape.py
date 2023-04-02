import curses
from curses import wrapper
import queue
import copy
import time

levels = [
    [
    ["#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", "X", " ", " ", "!", " ", "#"],
    ["#", " ", " ", " ", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", "O", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#"]
    ],
    [
    ["#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", "O", "#", "X", " ", " ", "#"],
    ["#", " ", " ", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", "!", " ", " ", "#"],
    ["#", " ", " ", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#"]
    ],
    [
    ["#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "O", "#"],
    ["#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "!", " ", "#"],
    ["#", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", " ", "@", " ", "#", "#"],
    ["#", "#", "#", " ", " ", "#"],
    ["#", "X", "#", " ", "#", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#"]
    ],
    [
    ["#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "X", "#"],
    ["#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "!", " ", "#"],
    ["#", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", " ", "@", " ", "#", "#"],
    ["#", "#", "#", " ", " ", "#"],
    ["#", "O", "#", " ", "#", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#"]
    ],
    [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "O", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
    ]
]

def refreshLevel(level, stdscr, enemiesList, levelNum, moves, pathsList):
    stdscr.clear()
    printLevel(level, stdscr, enemiesList, levelNum, moves)
    # path debug
    # printLevel(level, stdscr, enemiesList, levelNum, moves, pathsList)
    stdscr.refresh()

def printLevel(level, stdscr, enemiesList, levelNum, moves, pathsList = []):
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    blackred = curses.color_pair(3)
    blackwhite = curses.color_pair(4)
    redmagenta = curses.color_pair(5)
    for i, row in enumerate(level):
        for j, value in enumerate(row):
            iPrintPos, jPrintPos = i + 1, (j + 1) * 2
            if pathsList != None: 
                for path in pathsList:
                    if path != None:
                        if (i, j) in path:
                            stdscr.addstr(iPrintPos, jPrintPos, "&", redmagenta)
            if value == "#":
                stdscr.addstr(iPrintPos, jPrintPos, value, blackwhite)
            elif value == "X":
                stdscr.addstr(iPrintPos, jPrintPos, value, blackred)
            elif value == "O":
                stdscr.addstr(iPrintPos, jPrintPos, value, cyan)
            for enemy in enemiesList:
                if value == enemy:
                    stdscr.addstr(iPrintPos, jPrintPos, value, magenta)
    currentCol = len(level[0]) * 2 + 1
    stdscr.addstr(1, currentCol + 1, "level " + str(levelNum), blackwhite)
    stdscr.addstr(2, currentCol + 1, "total moves " + str(moves), blackwhite)

def findLocation(level, character):
    for i, row in enumerate(level):
        for j, value in enumerate(row):
            if value == character:
                return i, j
    return None

def findPath(level, start, end, enemiesList):
    startPos = findLocation(level, start)

    q = queue.Queue()
    q.put((startPos, [startPos]))

    visited = set()

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

def moveEnemy(level, path, enemy):
    oldrow, oldcol = findLocation(level, enemy)
    newrow, newcol = path[1]
    
    level[oldrow][oldcol] = " "
    level[newrow][newcol] = enemy

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

def checkLose(level, player):
    for row in level:
        for value in row:
            if value == player:
                return False
    return True

def loseWindow(stdscr):
    magenta = curses.color_pair(2)
    stdscr.clear()
    stdscr.addstr(1, 6, "you lost!", magenta)
    stdscr.refresh()
    time.sleep(0.5)
    stdscr.addstr(2, 6, "press space to play again", magenta)
    stdscr.refresh()

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

def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_MAGENTA)

    levelStart = 3
    levelIndex = levelStart
    enemiesList = ["!", "@"]
    player = "O"
    movesList = []
    while True:
        moves = 0
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
            continue
        while True:
            pathsList = []
            for enemy in enemiesList:
                if findLocation(level, enemy)!= None:
                    pathsList.append(findPath(level, enemy, player, enemiesList))
            refreshLevel(level, stdscr, enemiesList, levelIndex + 1, moves, pathsList)

            lost = checkLose(level, player)
            if lost:
                time.sleep(1)
                loseWindow(stdscr)
                while True:
                    key = stdscr.getch()
                    if key == ord(" "):
                        levelIndex = levelStart
                        break
                break
            else:
                while True:
                    key = stdscr.getch()
                    if key == curses.KEY_UP:
                        goodMove = movePlayer("up", level, player)
                    elif key == curses.KEY_DOWN:
                        goodMove = movePlayer("down", level, player)
                    elif key == curses.KEY_LEFT:
                        goodMove = movePlayer("left", level, player)
                    elif key == curses.KEY_RIGHT:
                        goodMove = movePlayer("right", level, player)
                    else:
                        continue

                    if goodMove == False:
                        continue
                    elif goodMove == True:
                        LivingEnemies = []
                        for enemy in enemiesList:
                            isAlive = findLocation(level, enemy)
                            if isAlive!= None:
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
                if goodMove == "escape":
                    break

wrapper(main)
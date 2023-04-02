import curses
from curses import wrapper
import queue
import time
import copy

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
    ["#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#"]
    ]
]

def refreshLevel(level, stdscr, path):
    stdscr.clear()
    printLevel(level, stdscr)
    # path debug
    printLevel(level, stdscr, path)
    stdscr.refresh()

def printLevel(level, stdscr, path = []):
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    red = curses.color_pair(3)
    white = curses.color_pair(4)
    for i, row in enumerate(level):
        for j, value in enumerate(row):
            if path != None: 
                if (i, j) in path:
                    stdscr.addstr(i, j * 2, "X", magenta)
            if value == "#":
                stdscr.addstr(i, j * 2, value, white)
            elif value == "X":
                stdscr.addstr(i, j * 2, value, red)
            elif value == "O":
                stdscr.addstr(i, j * 2, value, cyan)
            elif value == "!":
                stdscr.addstr(i, j * 2, value, magenta)

def findLocation(level, character):
    for i, row in enumerate(level):
        for j, value in enumerate(row):
            if value == character:
                return i, j

def findPath(level, start, end):
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

def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    magenta = curses.color_pair(2)

    levelIndex = 0
    enemy = "!"
    player = "O"
    while True:
        if levelIndex <= len(levels) - 1:
            level = copy.deepcopy(levels[levelIndex])
        else:
            stdscr.clear()
            stdscr.addstr(3, 6, "you escaped the final room!", magenta)
            stdscr.addstr(4, 6, "press space to play again", magenta)
            stdscr.refresh()
            while True:
                key = stdscr.getch()
                if key == ord(" "):
                    levelIndex = 0
                    break
            continue
        while True:
            path = findPath(level, enemy, player)
            refreshLevel(level, stdscr, path)

            lost = checkLose(level, player)
            if lost:
                stdscr.clear()
                stdscr.addstr(3, 6, "you lost", magenta)
                stdscr.addstr(4, 6, "press space to play again", magenta)
                stdscr.refresh()
                while True:
                    key = stdscr.getch()
                    if key == ord(" "):
                        levelIndex = 0
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
                        moveEnemy(level, path, enemy)
                        break
                    elif goodMove == "escape":
                        levelIndex += 1
                        break
                if goodMove == "escape":
                    break

wrapper(main)
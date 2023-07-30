# escape level editor, by Eric Manning
# created Jul 30, 2023

import curses
from curses import wrapper
from Levels import levels
from curses.textpad import rectangle

enemiesList = ["!", "@", "%", "Z"]
levelMap = [
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
]

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
    rectangle(stdscr, 0, 0, 15, 30)
    for i, row in enumerate(levelMap):
        for j, value in enumerate(row):
            if value == "O":
                stdscr.addstr(i + 1, j + 1, "O", cyan)
            elif value == "#":
                stdscr.addstr(i + 1, j + 1, "▧", white)
            elif value == "X":
                stdscr.addstr(i + 1, j + 1, "X", blackred | curses.A_BOLD)
            elif value in enemiesList:
                stdscr.addstr(i + 1, j + 1, value, red | curses.A_BOLD)
    stdscr.refresh()

# move cursor funciton
def moveCursor(stdscr, cursorLoc, direction):
    if direction == "up" and cursorLoc[0] > 1:
        cursorLoc[0] -= 1
    elif direction == "down" and cursorLoc[0] < 14:
        cursorLoc[0] += 1
    elif direction == "left" and cursorLoc[0] > 1:
        cursorLoc[1] -= 1
    elif direction == "right" and cursorLoc[0] < 28:
        cursorLoc[1] += 1
    printScreen(stdscr, cursorLoc)

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
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    blackred = curses.color_pair(3)
    blackwhite = curses.color_pair(4)
    redmagenta = curses.color_pair(5)
    white = curses.color_pair(6)
    red = curses.color_pair(7)
    whitemagenta = curses.color_pair(8)

    cursorLoc = (1, 1)
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
        elif key == 27:
            endProgram = True
        else:
            continue

wrapper(main)
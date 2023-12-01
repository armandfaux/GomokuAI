#!/usr/bin/env python3
import sys
from board import Board
from commands import runBrain

def main():
    displayMode = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("USAGE")
            print("    ./pbrain-gomoku-ai [--display]\n")
            print("    --display | -d : Optional, print the current board after every move\n")
            exit(0)
        elif sys.argv[1] == "--display" or sys.argv[1] == "-d":
            displayMode = True
        else:
            print("Wrong usage. Try './pbrain-gomoku-ai --help'")
            exit(1)

    board = Board(0)
    board.setMode(displayMode)

    while True:
        runBrain(board)

main()
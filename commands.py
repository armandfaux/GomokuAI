import sys
import time

def sendCommand(message):
    print(message)
    sys.stdout.flush()

def startCommand(board, options):
    if len(options) > 1 and int(options[1]) > 0:
        sendCommand("OK")
        board.setSize(int(options[1]))
        board.reset()
    else:
        sendCommand("ERROR")

def restartCommand(board):
    board.reset()
    sendCommand("OK")

def boardCommand(board):
    if board.getSize() < 5:
        board.setSize(20)
    board.reset()
    move = sys.stdin.readline().strip()
    board.setEmpty(False)
    while move != "DONE":
        if move == "END":
            exit(0)
        move = move.split(",")
        y = int(move[0])
        x = int(move[1])
        player = int(move[2])
        board.move([y, x, player])
        move = sys.stdin.readline().strip()
    sendCommand(board.bestMove(2))
    if board.getMode() == True:
        board.display()

def beginCommand(board):
    size = board.getSize()
    board.move([size // 2, size // 2, 1])
    sendCommand(str(size // 2) + ',' + str(size // 2))

def turnCommand(board, options):
    if len(options) < 2:
        sendCommand("ERROR")
        return
    coordinates = options[1].split(",")
    y = int(coordinates[0])
    x = int(coordinates[1])
    board.move([y, x, 2])
    board.setEmpty(False)
    sendCommand(board.bestMove(2))
    if board.getMode() == True:
        board.display()

def endCommand():
    exit(0)

def aboutCommand():
    sendCommand("name=\"pbrain\", version=\"1.0\", author=\"Hartman\", country=\"France\"")

def infoCommand():
    sendCommand("UNKNOWN")
    return

def runBrain(board):
    # get the manager's input
    cmd = sys.stdin.readline().strip()
    options = cmd.split(" ")

    if len(options) < 1:
        sendCommand("ERROR")
    elif options[0] == "START" or options[0] == "RECTSTART":
        startCommand(board, options)
    elif options[0] == "RESTART":
        restartCommand(board)
    elif options[0] == "BOARD":
        boardCommand(board)
    elif options[0] == "BEGIN":
        beginCommand(board)
    elif options[0] == "TURN":
        turnCommand(board, options)
    elif options[0] == "END":
        endCommand()
    elif options[0] == "ABOUT":
        aboutCommand()
    elif options[0] == "INFO":
        infoCommand()
    else:
        sendCommand("UNKNOWN")


import sys
import math

# Handle the board and the algorithm calculation
class Board:
    def __init__(self, size):
        # Init the empty board
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.height = size
        self.width = size
        self.empty = False # True if the board is empty
        self.yRange = [float('+inf'), float('-inf')]
        self.xRange = [float('+inf'), float('-inf')]

        # When activated, display the board after every move
        self.mode = False

    # getters
    def getBoard(self):
        return self.board

    def getSize(self):
        return self.size
    
    def getMode(self):
        return self.mode

    # setters
    def setBoard(self, board):
        self.board = [row[:] for row in board]

    def setSize(self, size):
        self.size = size
        self.height = size
        self.width = size

    def setEmpty(self, value):
        self.empty = value
        
    def setMode(self, mode):
        self.mode = mode

    def reset(self):
        self.empty = True
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

    # echo the board to the standard output
    def display(self):
        for row in self.board:
            print(row)

    # play on first cell available
    def defaultMove(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == 0:
                    self.move([y, x, 1])
                    return (f"{y},{x}")

    # Execute the given move on the board (move format : [y, x, player])
    def move(self, move):
        # Valid move format : [y, x, 1|2]
        if isinstance(move, list) and len(move) == 3 and (move[2] >= 1 and move[2] <= 2):
            if self.board[move[0]][move[1]] == 0:
                self.board[move[0]][move[1]] = move[2]
                self.yRange = [min(self.yRange[0], move[0]), max(self.yRange[1], move[0])]
                self.xRange = [min(self.xRange[0], move[1]), max(self.xRange[1], move[1])]
            else:
                print("[INTERNAL ERROR] Invalid move: cell", move[0:2], "already used")
        else:
            print("[INTERNAL ERROR] Invalid move: wrong format", file=sys.stderr)

    # Takes a list as parameter and return the index for the 1st winning move found
    def checkWinLine(self, line, player):
        for index, subLine in enumerate([line[i : i + 5] for i in range(len(line) - 4)]):
            if subLine.count(player) == 4 and subLine.count(0) == 1:
                return(subLine.index(0) + index)
        return -1

    # Checks all the lines & columns for a winning move
    def checkWinningMove(self, player):
        # Check rows & cols
        for y in range(self.height):
            x = self.checkWinLine(self.board[y], player)
            if x >= 0:
                self.move([y, x, 1])
                return (f"{y},{x}")

        for x, col in enumerate([[self.board[y][x] for y in range(self.height)] for x in range(self.width)]):
            y = self.checkWinLine(col, player)
            if y >= 0:
                self.move([y, x, 1])
                return (f"{y},{x}")

        # Check diagonals (left -> right)
        for offset, leftDiag in enumerate([[self.board[i + y][i] for i in range(self.width - y)] for y in range(self.height - 4)]):
            i = self.checkWinLine(leftDiag, player)
            if i >= 0:
                self.move([i + offset, i, 1])
                return (f"{i + offset},{i}")

        for offset, rightDiag in enumerate([[self.board[i][i + x] for i in range(self.width - x)] for x in range(1, self.width - 4)]):
            i = self.checkWinLine(rightDiag, player)
            if i >= 0:
                self.move([i, i + offset + 1, 1])
                return (f"{i},{i + offset + 1}")

        # Check diagonals (right -> left)
        for offset, botDiag in enumerate([[self.board[y + i][self.width - i - 1] for i in range(self.width - y)] for y in range(self.height - 4)]):
            i = self.checkWinLine(botDiag, player)
            if i >= 0:
                self.move([i + offset, self.width - i - 1, 1])
                return (f"{i + offset},{self.width - i - 1}")

        for offset, topDiag in enumerate([[self.board[i][x - i] for i in range(x + 1)] for x in range(self.width - 1, 3, -1)]):
            i = self.checkWinLine(topDiag, player)
            if i >= 0:
                self.move([i, self.width - offset - i - 1, 1])
                return (f"{i},{self.width - offset - i - 1}")

        # No winning move was found
        return("NONE")

    # Return a list of all the possible moves
    def getPossibleMoves(self, max_distance = 1):
        if self.empty:
            return [self.size // 2, self.size // 2]

        moves = []
        def closeToNonEmpty(y, x):
            for i in range(max(0, y - max_distance), min(self.size, y + max_distance + 1)):
                for j in range(max(0, x - max_distance), min(self.size, x + max_distance + 1)):
                    if self.board[i][j] != 0:
                        return True
            return False

        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == 0 and closeToNonEmpty(y, x):
                    moves.append([y, x])
        return moves

    # Implementation of the minimax recursive depth algorithm
    def minimax(self, depth, maxPlayer):
        # Recursive stop condition
        if depth == 0:
            return self.eval()

        # Return the best eval found (player 1)
        if maxPlayer:
            maxEval = -2
            for move in self.getPossibleMoves():
                board = Board(self.getSize())
                board.setBoard(self.getBoard())
                board.move(move + [1])
                val = board.minimax(depth - 1, False)
                maxEval = max(maxEval, val)
            return maxEval

        # Return the best worst eval found (player 2)
        else:
            minEval = 2
            for move in self.getPossibleMoves():
                board = Board(self.getSize())
                board.setBoard(self.getBoard())
                board.move(move + [2])
                val = board.minimax(depth - 1, True)
                minEval = min(minEval, val)
            return minEval

    # Return the best move found
    def bestMove(self, depth):
        if self.empty:
            self.empty = True
            return(f"{self.size // 2},{self.size // 2}")
        bestVal = float('-inf')
        bestMove = None

        # Checks for win / defense in 1
        simBoard = Board(self.getSize())
        simBoard.setBoard(self.getBoard())
        if simBoard.checkWinningMove(1) != "NONE":
            return self.checkWinningMove(1)
        if simBoard.checkWinningMove(2) != "NONE":
            return self.checkWinningMove(2)

        # Run the algorithm
        for move in self.getPossibleMoves():
            board = Board(self.getSize())
            board.setBoard(self.getBoard())
            board.move(move + [1])
            moveVal = board.minimax(depth - 1, False)
            if moveVal > bestVal:
                bestVal = moveVal
                bestMove = move
        self.move(bestMove + [1])
        return(f"{bestMove[0]},{bestMove[1]}")

    # Evaluate the position - return a float between -1 and 1
    # (positive number = advantage to player 1)
    # (negative number = advantage to player 2)
    def eval(self):
        scoreBoard = [0, 1, 7, 30, 90, 600]
        scoreA = 0
        scoreB = 0

        # Combine all lines and diagonals
        lines = self.board + [
            [self.board[y][x] for y in range(max(0, self.yRange[0] - 3), min(self.height, self.yRange[1] + 3))]
            for x in range(self.xRange[0], self.xRange[1] + 1)]
        lines += [
            [self.board[i + y][i] for i in range(self.width - y)] for y in range(self.yRange[0], min(self.yRange[1], self.height - 4))
        ]
        lines += [
            [self.board[i][i + x] for i in range(self.width - x)] for x in range(self.xRange[0], min(self.xRange[1], self.width - 4))
        ]
        lines += [
            [self.board[y + i][self.width - i - 1] for i in range(self.width - y)] for y in range(self.yRange[0], min(self.yRange[1], self.height - 4))
        ]
        lines += [
            [self.board[i][x - i] for i in range(x + 1)] for x in range(self.width - 1, 3, -1)
        ]

        # The evaluation is quite simple, yet efficient :
        # It assigns a score to both players according to their current open chains
        # The longer the chain, the higher the score
        for line in lines:
            if line.count(1) < 1 and line.count(2) < 1:
                continue
            for i in range(len(line) - 4):
                subline = line[i : i + 5]

                count_1 = subline.count(1)
                count_2 = subline.count(2)

                if count_1 == 5:
                    return 1
                if count_2 == 5:
                    return -1
                if count_2 == 0:
                    scoreA += scoreBoard[count_1]
                if count_1 == 0:
                    scoreB += scoreBoard[count_2] * 1.5

        diff = scoreA - scoreB

        # This formula convert the score difference into a float between -1 and 1
        return math.atan(diff / 50) * (2 / math.pi)


# Gomoku AI

The Gomoku is a 3rd year Epitech AI project

The goal is to create a bot for the Gomoku game

## Game rules

2 players are competing each other on a board (called goban)

Each turn, the players must place a stone anywhere on an empty cell of the board

The goal is to place 5 aligned stone (horizontal, vertical or diagonal) to win the game

## Algorithm

I implemented a minimax algorithm to compute the best move
The algorithm anticipates X moves in advance, you can configure the depth
However, a high depth implies higher calculation time

The AI evaluates the board based on a formula of my own design, in order to be able to pick the move that gives the best odds of winning

## Usage

- Clone the repo
- $ make
- ./pbrain-gomoku-ai [--display]

When the --display flag is activated, the game will display the board after every move
Be careful, the display mode is not compliant with the protocol (since it adds extra output)

/!\ The binary only works on Linux (for now)

## The protocol

Our IA is compliant with the following Piskvork protocol :

### START [size]

When the brain receives this command, it initializes itself and creates an empty board, but doesn't make any move yet. The parameter is size of the board. The brain must be able to play on board of size 20, because this size will be used in Gomocup tournaments. It is recommended but not required to support other board sizes. If the brain doesn't like the size, it responds ERROR. There can be a message after the ERROR word. The manager can try other sizes or it can display an error message to a user. The brain responds OK if it has been initialized successfully.

Example:

    The manager sends:
        START 20
    The brain answers:
        OK - everything is good
        ERROR message - unsupported size or other error

### TURN [X],[Y]

The parameters are coordinate of the opponent's move. All coordinates are numbered from zero.
Expected answer:
 two comma-separated numbers - coordinates of the brain's move

Example:

    The manager sends:
        TURN 10,10
    The brain answers:
        11,10


### BEGIN

This command is send by the manager to one of the players (brains) at the beginning of a match. This means that the brain is expected to play (open the match) on the empty playing board. After that the other brain obtains the TURN command with the first opponent's move. The BEGIN command is not used when automatic openings are enabled, because in that case both brains receive BOARD commands instead.

    Expected answer:
        two numbers separated by comma - coordinates of the brain's move

Example:

    The manager sends:
        BEGIN
    The brain answers:
        10,10

### BOARD

This command imposes entirely new playing field. It is suitable for continuation of an opened match or for undo/redo user commands. The BOARD command is usually send after START, RESTART or RECTSTART command when the board is empty. If there is any open match, the manager sends RESTART command before the BOARD command.
After this command the data forming the playing field are send. Every line is in the form:

    [X],[Y],[field]

where [X] and [Y] are coordinates and [field] is either number 1 (own stone) or number 2 (opponent's stone) or number 3 (only if continuous game is enabled, stone is part of winning line or is forbidden according to renju rules).
If game rule is renju, then the manager must send these lines in the same order as moves were made. If game rule is Gomoku, then the manager may send moves in any order and the brain must somehow cope with it. Data are ended by DONE command. Then the brain is expected to answer such as to TURN or BEGIN command.

Example:

    The manager sends:
        BOARD
        10,10,1
        10,11,2
        11,11,1
        9,10,2
        DONE
    The brain answers:
        9,9

### INFO [key] [value]

The manager sends information to the brain. The brain can ignore it. However, the brain will lose if it exceeds the limits. The brain must cope with situations when the manager doesn't send all information which is mentioned in this document. Most of this information is sent at the beginning of a match. The time limits will not be changed in the middle of a match during a tournament. It is recommended to react on commands at any time, because the human opponent can change these values even when the brain is thinking.

The key can be:

    timeout_turn  - time limit for each move (milliseconds, 0=play as fast as possible)
    timeout_match - time limit of a whole match (milliseconds, 0=no limit)
    max_memory    - memory limit (bytes, 0=no limit)
    time_left     - remaining time limit of a whole match (milliseconds)
    game_type     - 0=opponent is human, 1=opponent is brain, 2=tournament, 3=network tournament
    rule          - bitmask or sum of 1=exactly five in a row win, 2=continuous game, 4=renju, 8=caro
    evaluate      - coordinates X,Y representing current position of the mouse cursor
    folder        - folder for persistent files

Information about time and memory limits is sent before the first move (after or before START command). Info time_left is sent before every move (before commands TURN, BEGIN, BOARD and SWAP2BOARD). The remaining time can be negative when the brain runs out of time. Remaining time is equal to 2147483647 if the time for a whole match is unlimited. The manager is required to send info time_left if the time is limited, so that the brain can ignore info timeout_match and only rely on info time_left.
Time for a match is measured from creating a process to the end of a game (but not during opponent's turn). Time for a turn includes processing of all commands except initialization (commands START, RECTSTART, RESTART). Turn limit equal to zero means that the brain should play as fast as possible (eg count only a static evaluation and don't search possible moves).

INFO folder is used to determine a folder for files that are permanent. Because this folder is common for all brains and maybe other applications, the brain must create its own subfolder which name must be the same as the name of the brain. If the manager does not send INFO folder, then the brain cannot store permanent files.

Only debug versions should respond to INFO evaluate. For example, it can print evaluation of the square to some window. It cannot be written to the standard output. Release versions should just ignore INFO evaluate.

How should the brain behave when obtains unknown INFO command ?
- Ignore it, it is probably not important. If it was important, it is not in an INFO command form.

How should behave the brain obtaining the unachievable INFO command?
(for example too small memory limit)
- The brain should wait with the output of the problem until the manager sends the first command not having an INFO form (TURN, BOARD or BEGIN). The manager does not read messages from the brain when sending INFO command.

Example:

    INFO timeout_match 300000
    INFO timeout_turn 10000
    INFO max_memory 83886080
    
    Expected answer: none

### END

When the brain obtains this command, it must terminate as soon as possible. The manager waits until the brain is finished. If the time of termination is too long (e.g. 1 second), the brain will be terminated by the manager. The brain should not write anything to output after the END command. However, the manager should not close the pipe until the brain is ended.

    Expected answer: none
        The brain should delete its temporary files.

##
## EPITECH PROJECT, 2023
## Makefile
## File description:
## Gomoku Makefile
##

# Variables
MAIN = main.py
SRC_FILES = *.py

EXE_FILE = gomoku
OUT_DIR = dist
BINARY = pbrain-gomoku-ai
BINARY_WIN = pbrain-gomoku64.exe

WINDOWS = gomoku_windows
LINUX = gomoku_linux
ROOT = root

all: $(LINUX)
#	make $(WINDOWS)

$(LINUX):
	cp $(MAIN) $(BINARY)
	chmod +x $(BINARY)

$(WINDOWS):
	pyinstaller --onefile $(SRC_FILES)
	mv $(OUT_DIR)/$(EXE_FILE) $(OUT_DIR)/$(BINARY_WIN)

$(ROOT): $(WINDOWS)
	mv $(OUT_DIR)/$(BINARY_WIN) ./

clean:
	rm -f *.gcno

clean_win:
	rm -rf build
	rm gomoku.spec

fclean: clean
	rm -rf $(BINARY)

fclean_win: clean_win
	rm -rf $(OUT_DIR)
	rm -rf $(BINARY_WIN)

re: fclean all
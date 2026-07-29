import copy
import random

SIZE = 9
EMPTY = 0


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)

                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate

                        if fill_board(board):
                            return True

                        board[row][col] = EMPTY

                return False

    return True


def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues

    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)

        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1


def generate_puzzle(difficulty="medium"):
    difficulties = {
        "easy": 45,
        "medium": 35,
        "hard": 25
    }

    clues = difficulties.get(difficulty, 35)

    while True:
        board = create_empty_board()

        fill_board(board)

        solution = deep_copy(board)

        remove_cells(board, clues)

        if has_unique_solution(board):
            puzzle = deep_copy(board)
            return puzzle, solution


# Copilot suggested a basic Sudoku generation approach,
# but I evaluated the suggestion and modified it
# to include unique solution checking before accepting puzzles.
# This ensures every generated puzzle has exactly one solution.

def has_unique_solution(board):

    def count_solutions(board):
        for row in range(SIZE):
            for col in range(SIZE):

                if board[row][col] == EMPTY:
                    count = 0

                    for num in range(1, SIZE + 1):

                        if is_safe(board, row, col, num):

                            board[row][col] = num

                            count += count_solutions(board)

                            board[row][col] = EMPTY

                    return count

        return 1  # Found a valid solution

    return count_solutions(deep_copy(board)) == 1
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
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    current_clues = SIZE * SIZE

    for row, col in cells:
        if current_clues <= clues:
            break

        if board[row][col] == EMPTY:
            continue

        saved = board[row][col]
        board[row][col] = EMPTY

        if not has_unique_solution(board):
            board[row][col] = saved
        else:
            current_clues -= 1


def generate_puzzle(difficulty="medium"):
    difficulties = {
        "easy": 45,
        "medium": 35,
        "hard": 25
    }

    clues = difficulties.get(difficulty, 35)

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)

    return board, solution


# Copilot suggested removing the unique-solution check for better performance.
# I rejected that suggestion because the project rubric requires every Sudoku puzzle
# to have exactly one unique solution.
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
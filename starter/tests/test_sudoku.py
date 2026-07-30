import sudoku_logic


def test_create_empty_board():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_is_safe():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    board[0][1] = 3
    board[1][0] = 6

    assert sudoku_logic.is_safe(board, 0, 2, 1)
    assert not sudoku_logic.is_safe(board, 0, 2, 5)
    assert not sudoku_logic.is_safe(board, 0, 2, 3)
    assert not sudoku_logic.is_safe(board, 2, 2, 6)


def test_generate_puzzle_has_board_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle("easy")

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert puzzle != solution
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)


def test_generate_puzzle_unique_solution():
    puzzle, solution = sudoku_logic.generate_puzzle("easy")

    assert sudoku_logic.has_unique_solution(puzzle)


def test_has_unique_solution_known_board():
    board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, sudoku_logic.EMPTY],
    ]

    assert sudoku_logic.has_unique_solution(board)
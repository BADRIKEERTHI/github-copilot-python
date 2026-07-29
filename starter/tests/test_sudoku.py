import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sudoku_logic

def test_board_generation():
    puzzle, solution = sudoku_logic.generate_puzzle("easy")
    assert len(puzzle) == 9
    assert len(solution) == 9

def test_unique_solution():
    puzzle, solution = sudoku_logic.generate_puzzle("easy")
    assert sudoku_logic.has_unique_solution(puzzle)
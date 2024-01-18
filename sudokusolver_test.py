import unittest
from sudoku_solver import SudokuSolver
from block import Block
import numpy as np

class TestSudoku(unittest.TestCase):
    def test_init_board_is_empty(self):
        board = SudokuSolver().get_board()
        empty = True
        for row in board:
            for ele in row:
                if ele:
                    empty = False
        self.assertTrue(empty)

    def test_right_super_block(self):
        board = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
        solver = SudokuSolver()
        solver.set_board(np.array(board))
        expected_super_block = np.array([
                        [4, 0, 0],
                        [0, 7, 5],
                        [6, 0, 1]
        ])
        test_block = Block((1, 4), 7)
        super_block = solver.get_super_block(test_block)
        equal = True
        for i in range(3):
            for j in range(3):
                if super_block[i][j] != expected_super_block[i][j]:
                    equal = False
        self.assertTrue(equal)


if __name__ == '__main__':
    unittest.main()

import unittest
from sudoku_solver import SudokuSolver


class TestSudoku(unittest.TestCase):
    def test_init_board_is_empty(self):
        board = SudokuSolver().get_board()
        empty = True
        for row in board:
            for ele in row:
                if ele:
                    empty = False
        self.assertTrue(empty)


if __name__ == '__main__':
    unittest.main()

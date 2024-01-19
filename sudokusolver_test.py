import unittest
from sudoku_solver import SudokuSolver
from block import Block, LocationOccupiedError
import numpy as np


class TestSudoku(unittest.TestCase):
    _test_board = [
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

    def test_right_super_block(self):
        solver = SudokuSolver(np.array(self._test_board))
        expected_super_block = [
                        [4, 0, 0],
                        [0, 7, 5],
                        [6, 0, 1]
        ]
        test_block = Block((1, 4), 7)
        super_block = []
        for blocks in solver.get_super_block(test_block):
            row = []
            for block in blocks:
                row.append(int(block))
            super_block.append(row)
        equal = True
        for i in range(3):
            for j in range(3):
                if super_block[i][j] != expected_super_block[i][j]:
                    equal = False

        self.assertTrue(equal)

    def test_check_valid_add(self):
        solver = SudokuSolver(np.array(self._test_board))
        check_block = Block((6, 4), 8)
        solver.add_block(check_block)

    def test_check_invalid_add_in_row(self):
        solver = SudokuSolver(np.array(self._test_board))
        check_block = Block((6, 4), 1)
        self.assertFalse(solver.check_valid_add(check_block))

    def test_check_invalid_add_in_col(self):
        solver = SudokuSolver(np.array(self._test_board))
        check_block = Block((6, 4), 5)
        self.assertFalse(solver.check_valid_add(check_block))

    def test_check_invalid_add_in_super_block(self):
        solver = SudokuSolver(np.array(self._test_board))
        check_block = Block((4, 0), 4)
        self.assertFalse(solver.check_valid_add(check_block))

    def test_check_invalid_add_same_location(self):
        solver = SudokuSolver(np.array(self._test_board))
        check_block = Block((2, 3), 4)
        self.assertFalse(solver.check_valid_add(check_block))

    def test_add_block_already_exists(self):
        solver = SudokuSolver(np.array(self._test_board))
        test_block = Block((6, 3), 5)
        with self.assertRaises(LocationOccupiedError):
            solver.add_block(test_block)

    def test_remove_removable_block(self):
        _test_og_board = [
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
        solver = SudokuSolver(np.array(self._test_board))
        added_block = Block((6, 4), 8, True)
        solver.add_block(added_block)
        rem_block = Block((6, 4), 0)
        solver.remove_block(rem_block)
        _test_og_board[rem_block[0]][rem_block[1]] = 0
        new_board = solver.get_board()
        same = True
        for i in range(9):
            for j in range(9):
                if new_board[i][j] != _test_og_board[i][j]:
                    same = False

        self.assertTrue(same)

    def test_remove_not_removable_blocks(self):
        solver = SudokuSolver(np.array(self._test_board))
        rem_block = Block((3, 2), 4)
        solver.remove_block(rem_block)
        new_board = solver.get_board()
        same = True
        for i in range(9):
            for j in range(9):
                if new_board[i][j] != self._test_board[i][j]:
                    same = False

        self.assertTrue(same)

    def test_possible_number(self):
        solver = SudokuSolver(np.array(self._test_board))
        test_block = Block((6, 4), 4)
        expected = [8, 9]
        self.assertEqual(expected, solver.get_possible_nums(test_block))

    def test_possible_number_again(self):
        solver = SudokuSolver(np.array(self._test_board))
        test_block = Block((6, 6), 4)
        expected = [5, 6, 8]
        self.assertEqual(expected, solver.get_possible_nums(test_block))

    def test_possible_number_occupied(self):
        solver = SudokuSolver(np.array(self._test_board))
        test_block = Block((0, 0), 4)
        with self.assertRaises(LocationOccupiedError):
            solver.get_possible_nums(test_block)


if __name__ == '__main__':
    unittest.main()

import unittest
from sudoku_solver import SudokuSolver
from block import Block, LocationOccupiedError


class TestSudoku(unittest.TestCase):
    def setUp(self):
        print(self.id())
        self._test_board = [
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
        self.solver = SudokuSolver(self._test_board)

    def test_correct_super_block(self):
        expected_super_block = [
                        [4, 0, 0],
                        [0, 7, 5],
                        [6, 0, 1]
        ]
        test_block = Block((1, 4), 7)
        super_block = []
        for blocks in self.solver.get_super_block(test_block):
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
        check_block = Block((6, 4), 8)
        self.solver.add_block(check_block)

    def test_check_invalid_add_in_row(self):
        check_block = Block((6, 4), 1)
        self.assertFalse(self.solver.check_valid_add(check_block))

    def test_check_invalid_add_in_col(self):
        check_block = Block((6, 4), 5)
        self.assertFalse(self.solver.check_valid_add(check_block))

    def test_check_invalid_add_in_super_block(self):
        check_block = Block((4, 0), 4)
        self.assertFalse(self.solver.check_valid_add(check_block))

    def test_check_invalid_add_same_location(self):
        check_block = Block((2, 3), 4)
        self.assertFalse(self.solver.check_valid_add(check_block))

    def test_add_block_already_exists(self):
        test_block = Block((6, 3), 5)
        with self.assertRaises(LocationOccupiedError):
            self.solver.add_block(test_block)

    def test_remove_removable_block(self):
        added_block = Block((6, 4), 8, True)
        self.solver.add_block(added_block)
        rem_block = Block((6, 4), 0)
        self.solver.remove_block(rem_block)
        self._test_board[rem_block[0]][rem_block[1]] = 0
        new_board = [[int(column) for column in row] for row in self.solver.get_board()]
        same = True
        for i in range(9):
            for j in range(9):
                if int(new_board[i][j]) != self._test_board[i][j]:
                    same = False

        self.assertTrue(same)

    def test_remove_not_removable_blocks(self):
        rem_block = Block((3, 2), 4)
        self.solver.remove_block(rem_block)
        new_board = [[int(column) for column in row] for row in self.solver.get_board()]
        same = True
        for i in range(9):
            for j in range(9):
                if int(new_board[i][j]) != self._test_board[i][j]:
                    same = False

        self.assertTrue(same)

    def test_possible_number(self):
        test_block = Block((6, 4), 4)
        expected = [8, 9]
        self.assertEqual(expected, self.solver.get_possible_nums(test_block))

    def test_possible_number_again(self):
        test_block = Block((6, 6), 4)
        expected = [5, 6, 8]
        self.assertEqual(expected, self.solver.get_possible_nums(test_block))

    def test_possible_number_occupied(self):
        test_block = Block((0, 0), 4)
        with self.assertRaises(LocationOccupiedError):
            self.solver.get_possible_nums(test_block)

    def test_valid_board(self):
        ...

    def test_invalid_board(self):
        ...

    def test_solver(self):
        test_board = []
        nums = '3.542.81.4879.15.6.29.5637485.793.416132.8957.74.6528.2413.9.655.867.192.965124.8'
        for i in range(9):
            row = []

            for j in range(9):

                try:
                    row.append(int(nums[i * 9 + j]))

                except ValueError:
                    row.append(0)

            test_board.append(row)

        self.solver.set_board(test_board)
        self.solver.solve()
        self.solver.print_board()

    def test_multiple_solutions(self):
        self.solver.set_board(self._test_board)
        solutions = self.solver.solve(mode='multi')
        correctness = True
        if not self.solver.validate_board():
            correctness = False

        self.assertTrue(correctness)


if __name__ == '__main__':
    unittest.main()

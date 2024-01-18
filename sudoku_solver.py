import random

import numpy as np
from block import Block


class SudokuSolver:
    def __init__(self):
        self._board = np.array([[0 for _ in range(9)] for _ in range(9)])

    def get_board(self):
        return self._board

    def set_board(self, board):
        self._board = board

    def generate_board(self):
        ...

    def solve(self):
        ...

    def get_super_block(self, in_block):
        super_block_index = in_block.get_super_block_index()
        super_block = self._board[
                      super_block_index[0]*3:super_block_index[0]*3+3,
                      super_block_index[1]*3:super_block_index[1]*3+3
                      ]
        return super_block

    def check_valid_add(self, in_block):
        # Check for all the elements in the super block

        # Check for all the elements in the row
        # Check for all the elements in the column
        ...

    def add_block(self, in_block: Block):
        ...

    def remove_block(self, rem_block: Block):
        ...


if __name__ == "__main__":
    solver = SudokuSolver()
    add_block = Block((4, 0), 4)
    print(solver.get_board())
    print(solver.get_super_block(add_block))

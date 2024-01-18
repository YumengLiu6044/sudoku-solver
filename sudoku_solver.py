import numpy as np
from block import Block


class SudokuSolver:
    def __init__(self):
        self._board = np.array([[0 for _ in range(9)] for _ in range(9)])

    def get_board(self):
        return self._board

    def generate_board(self):
        ...

    def solve(self):
        ...

    def check_valid_add(self, in_block):
        ...

    def add_block(self, in_block: Block):
        ...

    def remove_block(self, rem_block: Block):
        ...

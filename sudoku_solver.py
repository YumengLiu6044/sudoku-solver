import random

import numpy as np
from block import Block


class SudokuSolver:
    def __init__(self):
        self._board = np.array([[0 for _ in range(9)] for _ in range(9)], dtype=int)
        self._blocks = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(Block((i, j), self._board[i][j], self._board[i][j] == 0))
            self._blocks.append(row)

    def get_board(self):
        return self._board

    def set_board(self, board):
        self._board = board
        self._blocks = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(Block((i, j), self._board[i][j], self._board[i][j] == 0))
            self._blocks.append(row)

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

    def check_valid_add(self, in_block: Block):
        # Check if the block is empty
        if self._board[in_block[0]][in_block[1]] != 0:
            return False

        # Check for all the elements in the super block
        super_block = self.get_super_block(in_block)
        if in_block.get_value() in super_block.ravel() and in_block.get_value() != 0:
            return False

        # Check for all the elements in the row
        if in_block.get_value() in self._board[in_block[0]] and in_block.get_value() != 0:
            return False

        # Check for all the elements in the column
        if in_block.get_value() in self._board[:, in_block[1]] and in_block.get_value() != 0:
            return False

        return True

    def add_block(self, in_block: Block):
        if self.check_valid_add(in_block):
            self._board[in_block[0]][in_block[1]] = in_block.get_value()
            self._blocks[in_block[0]][in_block[1]].set_value(in_block.get_value())

    def remove_block(self, rem_block: Block):
        self._board[rem_block[0]][rem_block[1]] = 0


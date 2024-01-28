import numpy as np
from block import Block, LocationOccupiedError


class NoSolutionError(Exception):
    ...


class SudokuSolver:
    def __init__(self, board: np.ndarray):
        self._board = board
        self._blocks = []
        self.set_board(board)

    def get_board(self):
        return self._blocks

    def set_board(self, board):
        self._board = board
        self._blocks = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(Block((i, j), self._board[i][j], self._board[i][j] == 0))
            self._blocks.append(row)
        self._blocks = np.array(self._blocks)

    def generate_board(self):
        ...

    def get_possible_nums(self, in_block: Block):
        possible_nums = []
        if self._blocks[in_block[0]][in_block[1]].get_value() != 0:
            raise LocationOccupiedError(f"{in_block.get_index()} is occupied")

        super_block = self.get_super_block(in_block)
        for i in range(1, 10):
            if i in map(int, super_block.ravel()):
                continue

            # Check for all the elements in the row
            if i in map(int, self._blocks[in_block[0]]):
                continue

            # Check for all the elements in the column
            if i in map(int, self._blocks[:, in_block[1]]):
                continue

            possible_nums.append(i)

        return possible_nums

    def get_unsolved_blocks(self):
        unsolved_blocks = []
        for i in self._blocks:
            for j in i:
                if int(j) == 0:
                    unsolved_blocks.append(j)
        return unsolved_blocks

    def solve(self, board):
        unsolved = self.get_unsolved_blocks()
        # Return the board if all is solved
        if len(unsolved) == 0:
            return board

        # Get a list a potential numbers
        current_block = unsolved[0]
        potential_blocks = self.get_possible_nums(current_block)

        # Go through the list one by one and recurse
        for num in potential_blocks:
            copy_of_board = board
            copy_of_board[current_block[0]][current_block[1]].set_value(num)
            return self.solve(copy_of_board)

        return board

    def get_super_block(self, in_block):
        super_block_index = in_block.get_super_block_index()
        super_block = self._blocks[
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
        if in_block.get_value() in map(int, super_block.ravel()) and in_block.get_value() != 0:
            return False

        # Check for all the elements in the row
        if in_block.get_value() in map(int, self._blocks[in_block[0]]) and in_block.get_value() != 0:
            return False

        # Check for all the elements in the column
        if in_block.get_value() in map(int, self._blocks[:, in_block[1]]) and in_block.get_value() != 0:
            return False

        return True

    def add_block(self, in_block: Block):
        if self.check_valid_add(in_block):
            self._blocks[in_block[0]][in_block[1]] = in_block
        else:
            raise LocationOccupiedError(f'{in_block.get_index()} is occupied')

    def remove_block(self, rem_block: Block):
        if self._blocks[rem_block[0]][rem_block[1]].is_removable():
            self._blocks[rem_block[0]][rem_block[1]].set_value(0)

    def print_board(self):
        for i in self._board:
            for j in i:
                print(j, " ", sep='', end='')

            print('\n')

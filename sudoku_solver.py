import numpy as np
from block import Block, LocationOccupiedError


class NoSolutionError(Exception):
    ...


class SudokuSolver:
    def __init__(self, board: list[list[int]]) -> None:
        self._blocks = []
        self.set_board(board)

    def get_board(self):
        return self._blocks

    def set_board(self, board: list[list[int]]):
        self._blocks = [[Block((i, j), board[i][j], board[i][j] == 0) for j in range(9)] for i in range(9)]
        self._blocks = np.array(self._blocks)

    def generate_board(self):
        ...

    @staticmethod
    def get_possible_nums(blocks, in_block: Block):
        possible_nums = []
        if blocks[in_block[0]][in_block[1]].get_value() != 0:
            raise LocationOccupiedError(f"{in_block.get_index()} is occupied")

        for i in range(1, 10):
            if i in map(int, SudokuSolver.get_super_block(blocks, in_block).ravel()):
                continue

            # Check for all the elements in the row
            if i in map(int, blocks[in_block[0]]):
                continue

            # Check for all the elements in the column
            if i in map(int, blocks[:, in_block[1]]):
                continue

            possible_nums.append(i)

        return possible_nums

    @staticmethod
    def get_unsolved_blocks(blocks):
        unsolved_blocks = []
        for i in blocks:
            for j in i:
                if int(j) == 0:
                    unsolved_blocks.append(j)
        return unsolved_blocks

    @staticmethod
    def back_track_solving_multiple_solution(blocks, unsolved_blocks):
        # Return the board as a solution if all is solved
        if len(unsolved_blocks) == 0:
            print('Found')
            yield blocks.copy()
            return

        # Get a list a potential numbers
        current_block = unsolved_blocks[0]
        potential_nums = SudokuSolver.get_possible_nums(blocks, current_block)

        for num in potential_nums:
            blocks[current_block[0]][current_block[1]].set_value(num)
            yield from SudokuSolver.back_track_solving_multiple_solution(blocks, unsolved_blocks[1:])
            blocks[current_block[0]][current_block[1]].set_value(0)

    @staticmethod
    def back_track_solving_single_solution(blocks, unsolved_blocks):
        # Return the board as a solution if all is solved
        if len(unsolved_blocks) == 0:
            print('Found')
            return True

        # Get a list a potential numbers
        current_block = unsolved_blocks[0]
        for num in SudokuSolver.get_possible_nums(blocks, current_block):
            blocks[current_block[0]][current_block[1]].set_value(num)
            if SudokuSolver.back_track_solving_single_solution(blocks, unsolved_blocks[1:]):
                return True

            blocks[current_block[0]][current_block[1]].set_value(0)

        return False

    @staticmethod
    def get_super_block(blocks, in_block):
        super_block_index = in_block.get_super_block_index()
        super_block = blocks[
                      super_block_index[0]*3:super_block_index[0]*3+3,
                      super_block_index[1]*3:super_block_index[1]*3+3
                      ]
        return super_block

    @staticmethod
    def check_valid_add(blocks, in_block: Block):
        # Check if the block is empty
        if blocks[in_block[0]][in_block[1]].get_value() != 0:
            return False

        # Check for all the elements in the super block
        super_block = SudokuSolver.get_super_block(blocks, in_block)
        if in_block.get_value() in map(int, super_block.ravel()) and in_block.get_value() != 0:
            return False

        # Check for all the elements in the row
        if in_block.get_value() in map(int, blocks[in_block[0]]) and in_block.get_value() != 0:
            return False

        # Check for all the elements in the column
        if in_block.get_value() in map(int, blocks[:, in_block[1]]) and in_block.get_value() != 0:
            return False

        return True

    def add_block(self, in_block: Block):
        if SudokuSolver.check_valid_add(self._blocks, in_block):
            self._blocks[in_block[0]][in_block[1]] = in_block
        else:
            raise LocationOccupiedError(f'{in_block.get_index()} is occupied')

    def remove_block(self, rem_block: Block):
        if self._blocks[rem_block[0]][rem_block[1]].is_removable():
            self._blocks[rem_block[0]][rem_block[1]].set_value(0)

    @staticmethod
    def print_board(blocks):
        for i in blocks:
            for j in i:
                print(j.get_value(), " ", sep='', end='')

            print('')

        print('\n')

    @staticmethod
    def validate_board(blocks) -> bool:
        for row in blocks:
            for single in row:
                og_value = single.get_value()
                single.set_value(0)
                if og_value != 0:
                    if og_value not in SudokuSolver.get_possible_nums(blocks, single):
                        return False

                single.set_value(og_value)

        return True

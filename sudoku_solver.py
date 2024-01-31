import numpy as np
from block import Block, LocationOccupiedError


class NoSolutionError(Exception):
    ...


class SudokuSolver:
    def __init__(self, board: list[list[int]]) -> None:
        self._blocks = []
        self._solution = []
        self.set_board(board)

    def get_board(self):
        return self._blocks

    def set_board(self, board: list[list[int]]):
        self._blocks = [[Block((i, j), board[i][j], board[i][j] == 0) for j in range(9)] for i in range(9)]
        self._blocks = np.array(self._blocks)
        self.get_unsolved_blocks()

    def generate_board(self):
        ...

    def get_possible_nums(self, in_block: Block):
        possible_nums = []
        if self._blocks[in_block[0]][in_block[1]].get_value() != 0:
            raise LocationOccupiedError(f"{in_block.get_index()} is occupied")

        for i in range(1, 10):
            if i in map(int, self.get_super_block(in_block).ravel()):
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
        return [i for i in self._blocks.ravel() if i.get_value() == 0]

    def _back_track_solving_multi_solution(self, unsolved_blocks):
        print('multi')
        # Append the blocks to self._solution if a solution is found
        if len(unsolved_blocks) == 0:
            print('Found')
            self._solution.append(self._blocks.copy())
            return

        # Get a list a potential numbers
        current_block = unsolved_blocks[0]
        potential_nums = self.get_possible_nums(current_block)

        for num in potential_nums:
            self._blocks[current_block[0]][current_block[1]].set_value(num)
            yield from self._back_track_solving_multi_solution(unsolved_blocks[1:])
            self._blocks[current_block[0]][current_block[1]].set_value(0)

        return

    def _back_track_solving_single_solution(self, unsolved_blocks):
        # Append the blocks to self._solution if a solution is found
        if len(unsolved_blocks) == 0:
            print('Found')
            self._solution.append(self._blocks.copy())
            return True

        # Get a list a potential numbers
        current_block = unsolved_blocks[0]
        for num in self.get_possible_nums(current_block):
            self._blocks[current_block[0]][current_block[1]].set_value(num)
            if self._back_track_solving_single_solution(unsolved_blocks[1:]):
                return True

            self._blocks[current_block[0]][current_block[1]].set_value(0)

        return False

    def solve(self, solve_mode='single'):
        if solve_mode == 'single':
            self._back_track_solving_single_solution(self.get_unsolved_blocks())
        elif solve_mode == 'multi':
            for _ in self._back_track_solving_multi_solution(self.get_unsolved_blocks()):
                pass
        else:
            raise ValueError("mode must be 'single' or 'multi'")

        # func = getattr(self, f'_back_track_solving_{mode}_solution')
        # return func(self.get_unsolved_blocks())

    def get_super_block(self, in_block):
        super_block_index = in_block.get_super_block_index()
        super_block = self._blocks[
                      super_block_index[0]*3:super_block_index[0]*3+3,
                      super_block_index[1]*3:super_block_index[1]*3+3
                      ]
        return super_block

    def check_valid_add(self, in_block: Block):
        # Check if the block is empty
        if self._blocks[in_block[0]][in_block[1]].get_value() != 0:
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
        for i in self._blocks:
            for j in i:
                print(j.get_value(), " ", sep='', end='')

            print('')

        print('\n')

    def get_solutions(self):
        return self._solution

    def validate_board(self, blocks) -> bool:
        if len(blocks) == 0:
            return False

        for row in blocks:
            for single in row:
                og_value = single.get_value()
                single.set_value(0)
                if og_value != 0:
                    if og_value not in self.get_possible_nums(single):
                        return False

                single.set_value(og_value)

        return True

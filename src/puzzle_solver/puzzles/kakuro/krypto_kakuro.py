from typing import Iterator

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_next_pos, get_pos, in_bounds, get_char
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, row_sums: list[list[str]], col_sums: list[list[str]], characters: list[str], min_value: int = 0, max_value: int = 9):
        legal_chars = characters + ['#'] + [str(i) for i in range(min_value, max_value + 1)]
        assert (len(row_sums), len(col_sums)) == board.shape, f'row_sums and col_sums must be the same shape as board, got {len(row_sums)}x{len(col_sums)} and {board.shape}'
        assert all(all(cc in legal_chars for cc in c.item().strip()) for c in np.nditer(board)), 'board must contain only #, space, or characters'
        assert all(all(all(cc in legal_chars for cc in c) for c in s) for s in row_sums), 'row_sums must be a list of lists of strings containing only # or characters'
        assert all(all(all(cc in legal_chars for cc in c) for c in s) for s in col_sums), 'col_sums must be a list of lists of strings containing only # or characters'
        self.board = board
        self.row_sums, self.col_sums = row_sums, col_sums
        self.characters = characters
        self.min_value, self.max_value = min_value, max_value
        assert (self.max_value - self.min_value + 1) == len(self.characters), f'max_value - min_value + 1 must be equal to the number of characters, got {self.max_value - self.min_value + 1} != {len(self.characters)}'
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.dictionary: dict[str, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for char in self.characters:
            self.dictionary[char] = self.model.NewIntVar(self.min_value, self.max_value, f'{char}')
        for pos in get_all_pos(self.V, self.H):
            if get_char(self.board, pos) == '#':
                continue
            self.model_vars[pos] = self.model.NewIntVar(self.min_value, self.max_value, f'{pos}')

    def get_consecutives(self, pos: Pos, direction: Direction) -> Iterator[list[Pos]]:
        consecutive = []
        while in_bounds(pos, self.V, self.H):
            if get_char(self.board, pos) == '#':
                if len(consecutive) > 0:
                    yield consecutive
                    consecutive = []
            else:
                consecutive.append(pos)
            pos = get_next_pos(pos, direction)
        if len(consecutive) > 0:
            yield consecutive

    def clue_to_var(self, clue: str) -> cp_model.IntVar:
        res = []
        for i,c in enumerate(clue[::-1]):
            res.append(self.dictionary[c] * 10**i)
        return lxp.sum(res)

    def add_all_constraints(self):
        self.model.AddAllDifferent(list(self.dictionary.values()))  # dictionary must be unique
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos).strip()
            if c not in ['', '#']:
                self.model.Add(self.model_vars[pos] == (self.dictionary[c] if c in self.dictionary else int(c)))
        for row in range(self.V):  # for row clues
            row_consecutives = self.get_consecutives(get_pos(x=0, y=row), Direction.RIGHT)
            for i, consecutive in enumerate(row_consecutives):
                self.model.AddAllDifferent([self.model_vars[p] for p in consecutive])
                clue = self.row_sums[row][i]
                if clue != '#':
                    self.model.Add(lxp.sum([self.model_vars[p] for p in consecutive]) == self.clue_to_var(clue))
            assert len(self.row_sums[row]) == i + 1, f'row_sums[{row}] has {len(self.row_sums[row])} clues, but {i + 1} consecutive cells'
        for col in range(self.H):  # for column clues
            col_consecutives = self.get_consecutives(get_pos(x=col, y=0), Direction.DOWN)
            for i, consecutive in enumerate(col_consecutives):
                self.model.AddAllDifferent([self.model_vars[p] for p in consecutive])
                clue = self.col_sums[col][i]
                if clue != '#':
                    self.model.Add(lxp.sum([self.model_vars[p] for p in consecutive]) == self.clue_to_var(clue))
            assert len(self.col_sums[col]) == i + 1, f'col_sums[{col}] has {len(self.col_sums[col])} clues, but {i + 1} consecutive cells'

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                is_shaded=lambda r, c: self.board[r, c] == '#',
                center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)]),
                text_on_shaded_cells=False
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

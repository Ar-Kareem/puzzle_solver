from typing import Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_char, get_next_pos, get_pos, get_row_pos, get_col_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, characters: set[str] = None, illegal_run: Optional[int] = 3, wall_char: Optional[str] = None):
        if characters is None:
            characters = set(c.item() for c in np.nditer(board) if c.item() not in [' ', wall_char])
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() in ([' ', wall_char] + list(characters)) for c in np.nditer(board)), 'board must contain only space or characters'
        self.board = board
        self.V, self.H = board.shape
        assert self.V % len(characters) == 0, f'board height must be divisible by number of characters, got {self.V} % {len(characters)} = {self.V % len(characters)}'
        assert self.H % len(characters) == 0, f'board width must be divisible by number of characters, got {self.H} % {len(characters)} = {self.H % len(characters)}'
        self.num_repeats_v = self.V // len(characters)
        self.num_repeats_h = self.H // len(characters)
        self.characters = characters
        self.illegal_run = illegal_run
        self.wall_char = wall_char

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            if get_char(self.board, pos) == self.wall_char:
                continue
            for char in self.characters:
                self.model_vars[pos, char] = self.model.NewBoolVar(f'{pos}:{char}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c == self.wall_char:
                continue
            self.model.AddExactlyOne([self.model_vars[pos, char] for char in self.characters])
            if c in self.characters:
                self.model.Add(self.model_vars[pos, c] == 1)
        for char in self.characters:
            for row in range(self.V):
                self.model.Add(lxp.Sum([self.model_vars[pos, char] for pos in get_row_pos(row, self.H)]) == self.num_repeats_v)
            for col in range(self.H):
                self.model.Add(lxp.Sum([self.model_vars[pos, char] for pos in get_col_pos(col, self.V)]) == self.num_repeats_h)
        if self.illegal_run is not None:
            for pos in get_all_pos(self.V, self.H):
                self.disallow_run_constraint(pos, Direction.RIGHT)
                self.disallow_run_constraint(pos, Direction.DOWN)

    def disallow_run_constraint(self, pos: Pos, direction: Direction):
        run = [pos]
        while len(run) < self.illegal_run:
            pos = get_next_pos(pos, direction)
            if not in_bounds(pos, self.V, self.H):
                return
            run.append(pos)
        assert len(run) == self.illegal_run, f'SHOULD NOT HAPPEN: run length != max run, {len(run)} != {self.illegal_run}'
        for char in self.characters:
            self.model.Add(lxp.Sum([self.model_vars[p, char] for p in run]) < self.illegal_run)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: char for (pos, char), var in board.model_vars.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), self.board[r, c]), text_on_shaded_cells=False))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

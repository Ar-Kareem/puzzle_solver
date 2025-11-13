from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, get_char, get_col_pos, get_next_pos, get_ray, get_row_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, Direction8], cp_model.IntVar] = {}
        self.pos_to_vars: dict[Pos, list[cp_model.IntVar]] = defaultdict(list)  # positions that will be hit by all variables in the board
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for row_idx in [-1, self.V]:
            for pos in get_row_pos(row_idx, H=self.H):
                for direction in Direction8:
                    next_pos = get_next_pos(pos, direction)
                    if not in_bounds(next_pos, self.V, self.H):
                        continue
                    self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')
        for col_idx in [-1, self.H]:
            for pos in get_col_pos(col_idx, V=self.V):
                for direction in Direction8:
                    next_pos = get_next_pos(pos, direction)
                    if not in_bounds(next_pos, self.V, self.H):
                        continue
                    self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')
        for key, var in self.model_vars.items():
            pos, direction = key
            start_pos = get_next_pos(pos, direction)
            ray = get_ray(start_pos, direction, self.V, self.H, include_self=True)
            for p in ray:
                self.pos_to_vars[p].append(var)

    def add_all_constraints(self):
        pos_vars = defaultdict(list)
        for (pos, direction) in self.model_vars:
            pos_vars[pos].append(self.model_vars[(pos, direction)])
        for vars_ in pos_vars.values():
            self.model.AddExactlyOne(vars_)
        for pos in get_all_pos(self.V, self.H):
            c = str(get_char(self.board, pos)).strip()
            if not c:
                continue
            self.model.Add(lxp.Sum(self.pos_to_vars[pos]) == int(c))

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: direction.name for (pos, direction), var in board.model_vars.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            combined = np.full((self.V+2, self.H+2), '', dtype=object)
            d_to_arrow = {'UP': '↑', 'DOWN': '↓', 'LEFT': '←', 'RIGHT': '→', 'UP_LEFT': '↖', 'UP_RIGHT': '↗', 'DOWN_LEFT': '↙', 'DOWN_RIGHT': '↘'}
            for pos in get_all_pos(self.V, self.H):
                combined[pos.y+1, pos.x+1] = get_char(self.board, pos)
            for pos, direction in single_res.assignment.items():
                combined[pos.y+1, pos.x+1] += d_to_arrow[direction]
            print(combined_function(self.V+2, self.H+2, center_char=lambda r, c: combined[r, c]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

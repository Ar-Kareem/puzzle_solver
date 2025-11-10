import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_char, get_next_pos, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, quadrant: np.array, color_sums: dict[str, int]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item().strip() != '' for c in np.nditer(board)), 'board must contain only non-empty strings'
        self.V, self.H = board.shape
        self.colors = {c.item().strip() for c in np.nditer(board)}
        assert quadrant.shape == (self.V-1, self.H-1), f'quadrant must be {(self.V-1, self.H-1)}, got {quadrant.shape}'
        assert all(str(c.item()).isdecimal() for c in np.nditer(quadrant)), 'quadrant must contain only digits'
        assert set(color_sums.keys()) == self.colors, f'color_sums must contain all colors, missing {self.colors - set(color_sums.keys())} and extra {set(color_sums.keys()) - self.colors}'
        self.N = self.V * self.H
        self.board = board
        self.quadrant = quadrant
        self.color_sums = color_sums
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def add_all_constraints(self):
        self.model.AddAllDifferent(list(self.model_vars.values()))  # all numbers are unique
        for color in self.colors:  # enforce color sums
            color_sum = self.color_sums[color]
            color_vars = [self.model_vars[pos] for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos) == color]
            self.model.Add(lxp.Sum(color_vars) == color_sum)
        for pos in get_all_pos(self.V - 1, self.H - 1):  # enforce the 2x2 sums
            quadrant_sum = int(get_char(self.quadrant, pos))
            tl = pos
            tr = get_next_pos(tl, Direction.RIGHT)
            bl = get_next_pos(tl, Direction.DOWN)
            br = get_next_pos(bl, Direction.RIGHT)
            quadrant = np.array([self.model_vars[tl], self.model_vars[tr], self.model_vars[bl], self.model_vars[br]])
            self.model.Add(lxp.Sum(quadrant) == quadrant_sum)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment[get_pos(x=c, y=r)]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

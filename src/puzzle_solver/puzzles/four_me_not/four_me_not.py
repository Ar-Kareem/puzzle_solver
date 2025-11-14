import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_next_pos, get_pos, in_bounds, get_char
from puzzle_solver.core.utils_ortools import force_connected_component, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(str(c.item()).strip() in ['', '1'] for c in np.nditer(board)), 'board must contain only space or 1'
        self.board = board
        self.V, self.H = board.shape

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            self.disallow_four(pos, Direction.RIGHT)
            self.disallow_four(pos, Direction.DOWN)
            if get_char(self.board, pos).strip() == '1':
                self.model.Add(self.model_vars[pos] == 1)
        force_connected_component(self.model, self.model_vars)

    def disallow_four(self, pos: Pos, direction: Direction):
        p1 = pos
        p2 = get_next_pos(p1, direction)
        p3 = get_next_pos(p2, direction)
        p4 = get_next_pos(p3, direction)
        if all(in_bounds(p, self.V, self.H) for p in [p1, p2, p3, p4]):
            self.model.AddBoolOr([self.model_vars[p1].Not(), self.model_vars[p2].Not(), self.model_vars[p3].Not(), self.model_vars[p4].Not()])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

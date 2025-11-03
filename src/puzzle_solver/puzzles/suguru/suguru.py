from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors8, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, id_board: np.array, num_board: np.array):
        assert id_board.ndim == 2, f'id_board must be 2d, got {id_board.ndim}'
        assert all(str(c.item()).isdecimal() for c in np.nditer(id_board)), 'id_board must contain only digits'
        assert num_board.ndim == 2, f'num_board must be 2d, got {num_board.ndim}'
        assert all(str(c.item()).strip() == '' or str(c.item()).isdecimal() for c in np.nditer(num_board)), 'num_board must contain only space or digits'
        assert id_board.shape == num_board.shape, f'id_board and num_board must have the same shape, got {id_board.shape} and {num_board.shape}'
        self.id_board = id_board
        self.num_board = num_board
        self.V, self.H = id_board.shape
        self.ids = {int(c.item()) for c in np.nditer(id_board)}
        self.id_to_pos: dict[int, set[Pos]] = defaultdict(set)
        for pos in get_all_pos(self.V, self.H):
            self.id_to_pos[int(get_char(self.id_board, pos))].add(pos)
        self.N = max([len(v) for v in self.id_to_pos.values()])

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def add_all_constraints(self):
        for cage in self.ids:
            cage_vars = [self.model_vars[pos] for pos in self.id_to_pos[cage]]
            self.model.AddAllDifferent(cage_vars)
            for pos in self.id_to_pos[cage]:
                self.model.Add(self.model_vars[pos] <= len(cage_vars))
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.num_board, pos).strip()
            if c:  # force clues
                self.model.Add(self.model_vars[pos] == int(c))
            for n in get_neighbors8(pos, self.V, self.H):
                self.model.Add(self.model_vars[pos] != self.model_vars[n])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

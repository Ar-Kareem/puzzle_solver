import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors8, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(str(c.item()).strip().isdecimal() or str(c.item()).strip() == '' for c in np.nditer(board)), 'board must contain only digits or spaces'
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
        hit_pos = set()
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos).strip()
            if not c:
                continue
            for p in get_neighbors8(pos, self.V, self.H, include_self=True):
                self.model.Add(self.model_vars[p] == 0)
            orthos = set(get_col_pos(pos.x, self.V)) | set(get_row_pos(pos.y, self.H)) - {pos}
            self.model.Add(lxp.Sum([self.model_vars[p] for p in orthos]) == int(c))
            hit_pos.update(orthos)
        for pos in get_all_pos(self.V, self.H):
            for p in get_neighbors8(pos, self.V, self.H):
                self.model.Add(self.model_vars[p] == 0).OnlyEnforceIf(self.model_vars[pos])  # lighthouse cannot touch eachother
            if pos in hit_pos:
                continue
            self.model.Add(self.model_vars[pos] == 0)  # positions that have no lighthouse horizontally or vertically must be empty

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1, center_char=lambda r, c: str(self.board[r, c]).strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

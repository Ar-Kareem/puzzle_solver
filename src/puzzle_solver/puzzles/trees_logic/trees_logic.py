import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors8, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((str(c.item()).isdecimal() for c in np.nditer(board))), 'board must contain only digits'
        self.board = board
        self.V, self.H = board.shape
        self.block_numbers = {int(c.item()) for c in np.nditer(board)}
        self.blocks = {num: [] for num in self.block_numbers}
        for pos in get_all_pos(self.V, self.H):
            self.blocks[int(get_char(board, pos))].append(pos)

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for row in range(self.V):  # each row must have exactly one tree
            self.model.Add(lxp.sum([self.model_vars[pos] for pos in get_row_pos(row, self.H)]) == 1)
        for col in range(self.H):  # each column must have exactly one tree
            self.model.Add(lxp.sum([self.model_vars[pos] for pos in get_col_pos(col, self.V)]) == 1)
        for block_number in self.block_numbers:  # each block must have exactly one tree
            self.model.Add(lxp.sum([self.model_vars[pos] for pos in self.blocks[block_number]]) == 1)
        # trees cannot touch even diagonally
        for pos in get_all_pos(self.V, self.H):
            for neighbor in get_neighbors8(pos, self.V, self.H, include_self=False):
                self.model.Add(self.model_vars[neighbor] == 0).OnlyEnforceIf(self.model_vars[pos])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1, cell_flags=id_board_to_wall_fn(self.board)))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

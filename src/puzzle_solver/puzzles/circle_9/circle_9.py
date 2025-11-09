import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.N = max(self.V, self.H)

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            if get_char(self.board, pos).strip():
                self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for v in range(1, self.N + 1):  # each digit is circled once
            self.model.AddExactlyOne([self.model_vars[pos] for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos) == str(v)])
        for row in range(self.V):  # each row contains 1 circle
            self.model.AddExactlyOne([self.model_vars[pos] for pos in get_row_pos(row, self.H) if pos in self.model_vars])
        for col in range(self.H):  # each column contains 1 circle
            self.model.AddExactlyOne([self.model_vars[pos] for pos in get_col_pos(col, self.V) if pos in self.model_vars])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                cell_flags=lambda r, c: 'ULRD' if single_res.assignment.get(get_pos(x=c, y=r), 0) == 1 else '',
                center_char=lambda r, c: self.board[r, c].strip() if self.board[r, c].strip() else '.',
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

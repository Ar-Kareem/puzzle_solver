import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, get_row_pos, get_col_pos, get_char, get_neighbors8
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, goal: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.goal = goal
        self.V, self.H = board.shape
        assert goal.shape == (self.H, ), 'goal must be 1d and equal to board width'

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, int], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for v in range(0, 10):
                self.model_vars[(pos, v)] = self.model.NewBoolVar(f'{pos}:{v}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # every pos has exactly one digit
            self.model.AddExactlyOne([self.model_vars[(pos, v)] for v in range(0, 10)])
            c = str(get_char(self.board, pos)).strip()
            if c:
                self.model.Add(self.model_vars[(pos, int(c))] == 1)
        for row in range(self.V):  # every row contains once of every digit
            for v in range(0, 10):
                self.model.AddExactlyOne([self.model_vars[(pos, v)] for pos in get_row_pos(row, self.H)])
        for col in range(self.H):  # every column sums to the goal
            self.model.Add(lxp.sum([v * self.model_vars[(pos, v)] for pos in get_col_pos(col, self.V) for v in range(0, 10)]) == int(self.goal[col]))
        for pos in get_all_pos(self.V, self.H):  # same number cannot touch
            for v in range(0, 10):
                for neighbor in get_neighbors8(pos, self.V, self.H):
                    self.model.Add(self.model_vars[(neighbor, v)] == 0).OnlyEnforceIf(self.model_vars[(pos, v)])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: v for (pos, v), var in board.model_vars.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            arr = np.array([[single_res.assignment.get(get_pos(x=c, y=r), ' ') for c in range(self.H)] for r in range(self.V)])
            combined = np.concatenate((arr, self.goal.reshape(1, -1)), axis=0).astype(str)
            print(combined_function(self.V+1, self.H, cell_flags=lambda r, c: 'ULRD' if r == self.V else ('LRU' if r == 0 else 'LR'), center_char=lambda r, c: str(combined[r, c]).strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=9)

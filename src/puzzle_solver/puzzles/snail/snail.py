import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def spiral_from_topleft(matrix, N: int):
    res = []
    top, bottom = 0, N - 1
    left, right = 0, N - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):  # go right
            res.append(matrix[get_pos(x=c, y=top)])
        top += 1
        if top > bottom:
            break
        for r in range(top, bottom + 1):  # go down
            res.append(matrix[get_pos(x=right, y=r)])
        right -= 1
        if left > right:
            break
        for c in range(right, left - 1, -1):  # go left
            res.append(matrix[get_pos(x=c, y=bottom)])
        bottom -= 1
        if top > bottom:
            break
        for r in range(bottom, top - 1, -1):  # go up
            res.append(matrix[get_pos(x=left, y=r)])
        left += 1
    return res


def get_eq_val(model: cp_model.CpModel, int_var: cp_model.IntVar, val: int) -> cp_model.IntVar:
    eq_var = model.NewBoolVar(f'{int_var}:{val}:eq')
    model.Add(int_var == val).OnlyEnforceIf(eq_var)
    model.Add(int_var != val).OnlyEnforceIf(eq_var.Not())
    return eq_var


class Board:
    def __init__(self, board: np.array):
        self.V, self.H = board.shape
        assert self.V == self.H and self.V >= 3, f'board must be square, got {self.V}x{self.H}'
        self.board = board

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(0, 4, f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            c = get_char(self.board, pos).strip()
            if c:
                self.model.Add(self.model_vars[pos] == int(c))
        for v in [1, 2, 3]:
            for row in range(self.V):
                self.model.AddExactlyOne([get_eq_val(self.model, self.model_vars[pos], v) for pos in get_row_pos(row, self.H)])
            for col in range(self.H):
                self.model.AddExactlyOne([get_eq_val(self.model, self.model_vars[pos], v) for pos in get_col_pos(col, self.V)])
        vars_ = spiral_from_topleft(self.model_vars, self.V)
        self.add_snail_pattern(vars_)

    def add_snail_pattern(self, vars_):
        """Enforce on vars_ (each in {0,1,2,3}) that, ignoring 0s, the nonzero values must follow the repeating pattern 1 -> 2 -> 3 -> 1 -> 2 -> 3 -> ..."""
        # States: 0 = expect 1, 1 = expect 2, 2 = expect 3
        start = 0
        accept = [3]  # we can stop after expecting 1 or 2 or 3
        transitions = [ #  (*tail*, *transition*, *head*)
            # zeros don't change the state
            (0, 0, 0),
            (1, 0, 1),
            (2, 0, 2),
            (3, 0, 3),
            # pattern 1 -> 2 -> 3 -> 1 ...
            (0, 1, 1),  # State 0: saw "1" -> Go to state 1 (which will expect 2)
            (1, 2, 2),  # State 1: saw "2" -> Go to state 2 (which will expect 3)
            (2, 3, 3),  # State 2: saw "3" -> Go to state 3 (which will expect 1)
            (3, 1, 1),  # State 3: saw "1" -> Go to state 1 (which will expect 2)
        ]
        self.model.AddAutomaton(vars_, start, accept, transitions)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(v) for pos, v in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)]).replace('0', ' '),
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

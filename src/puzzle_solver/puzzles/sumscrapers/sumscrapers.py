import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def bool_from_greater_than(model, a, b, name):
    res = model.NewBoolVar(name)
    model.add(a > b).OnlyEnforceIf(res)
    model.add(a <= b).OnlyEnforceIf(res.Not())
    return res


class Board:
    def __init__(self, board: np.array, top: np.array, bottom: np.array, right: np.array, left: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((str(c.item()).strip() == '') or str(c.item()).strip().isdecimal() for c in np.nditer(board)), 'board must contain space or digits'
        self.board = board
        self.V, self.H = board.shape
        assert top.shape == (self.H,) and bottom.shape == (self.H,) and right.shape == (self.V,) and left.shape == (self.V,), 'top, bottom, right, and left must be 1d arrays of length board width and height'
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, max(self.V, self.H), f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force board clues
            v = get_char(self.board, pos)
            if str(v).isdecimal():
                self.model.Add(self.model_vars[pos] == int(v))
        for row_i in range(self.V):  # all different for rows
            self.model.AddAllDifferent([self.model_vars[pos] for pos in get_row_pos(row_i, self.H)])
        for col_i in range(self.H):  # all different for cols
            self.model.AddAllDifferent([self.model_vars[pos] for pos in get_col_pos(col_i, self.V)])
        for x in range(self.H):  # top
            self.tower_constraints(real=self.top[x], pos_list=[get_pos(x=x, y=y) for y in range(self.V)], name=f'top:{x}')
        for x in range(self.H):  # bottom
            self.tower_constraints(real=self.bottom[x], pos_list=[get_pos(x=x, y=y) for y in range(self.V-1, -1, -1)], name=f'bottom:{x}')
        for y in range(self.V):  # left
            self.tower_constraints(real=self.left[y], pos_list=[get_pos(x=x, y=y) for x in range(self.H)], name=f'left:{y}')
        for y in range(self.H):  # right
            self.tower_constraints(real=self.right[y], pos_list=[get_pos(x=x, y=y) for x in range(self.V-1, -1, -1)], name=f'right:{y}')

    def tower_constraints(self, real: int, pos_list: list[Pos], name: str):
        if str(real).strip() == '' or int(real) == -1:
            return
        real = int(real)
        can_see_variables = []
        previous_towers: list[cp_model.IntVar] = []
        for pos in pos_list:
            current_tower = self.model_vars[pos]
            can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'{name}:{pos}'))
            previous_towers.append(current_tower)
        self.model.add(lxp.sum(can_see_variables) == real)

    def can_see_tower(self, blocks: list[cp_model.IntVar], tower: cp_model.IntVar, name: str) -> cp_model.IntVar:
        """Returns a boolean variable of whether a position BEFORE the blocks can see the "tower" parameter."""
        if len(blocks) == 0:
            return tower
        # I can see "tower" if it's larger that all the blocks before it, lits is a list of [(tower > b0), (tower > b1), ..., (tower > bi)]
        can_see = self.model.NewBoolVar(name)
        and_constraint(self.model, target=can_see, cs=[bool_from_greater_than(self.model, tower, block, f'{name}:lits:{block}') for block in blocks])
        res = self.model.NewIntVar(0, max(self.V, self.H), f'{name}:res')
        self.model.Add(res == tower).OnlyEnforceIf(can_see)
        self.model.Add(res == 0).OnlyEnforceIf(can_see.Not())
        return res

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.value(board.model_vars[pos]) for pos in get_all_pos(board.V, board.H)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)]).strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

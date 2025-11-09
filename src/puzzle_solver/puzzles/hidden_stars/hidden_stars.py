import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos, Direction8, in_bounds, get_next_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def get_ray(pos: Pos, direction: Direction8, V: int, H: int) -> list[Pos]:
    out = []
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
        out.append(pos)
    return out


class Board:
    def __init__(self, board: np.array, side: np.array, top: np.array):
        assert (len(side), len(top)) == board.shape, 'side and top must be the same shape as board'
        assert all(c.item().strip() in ['', 'Q', 'W', 'E', 'A', 'D', 'Z', 'X', 'C'] for c in np.nditer(board)), 'board must contain only space or Q, W, E, A, D, Z, X, C'
        self.board = board
        self.side = side
        self.top = top
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            if not get_char(self.board, pos).strip():
                self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for row in range(self.V):  # force side counts
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in get_row_pos(row, self.H) if pos in self.model_vars]) == self.side[row])
        for col in range(self.H):  # force top counts
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in get_col_pos(col, self.V) if pos in self.model_vars]) == self.top[col])
        pos_hit_by_ray = set()
        for pos in get_all_pos(self.V, self.H):  # every arrow must point to a star
            c = get_char(self.board, pos).strip()
            if not c:
                continue
            d = {'Q': Direction8.UP_LEFT, 'W': Direction8.UP, 'E': Direction8.UP_RIGHT, 'A': Direction8.LEFT, 'D': Direction8.RIGHT, 'Z': Direction8.DOWN_LEFT, 'X': Direction8.DOWN, 'C': Direction8.DOWN_RIGHT}[c]
            ray = get_ray(pos, d, self.V, self.H)
            pos_hit_by_ray.update(ray)
            self.model.AddAtLeastOne([self.model_vars[pos] for pos in ray if pos in self.model_vars])
        for pos in get_all_pos(self.V, self.H):  # every star must have an arrow pointing to it
            if pos not in pos_hit_by_ray and pos in self.model_vars:
                self.model.Add(self.model_vars[pos] == 0)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), 0) == 1, center_char=lambda r, c: str(self.board[r, c]), text_on_shaded_cells=False))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

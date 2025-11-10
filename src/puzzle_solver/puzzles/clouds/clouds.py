from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


@dataclass(frozen=True)
class ShapeOnBoard:
    body: frozenset[Pos]
    is_active: cp_model.IntVar
    disallow: frozenset[Pos]


class Board:
    def __init__(self, side: np.array, top: np.array):
        self.V = side.shape[0]
        self.H = top.shape[0]
        self.side = side
        self.top = top

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.shapes_on_board: set[ShapeOnBoard] = set()
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for x in range(0, self.H):
            for end_x in range(x, self.H + 1):
                if (end_x - x) < 2:
                    continue
                max_allowed_height = np.min(self.top[x:end_x])
                for y in range(0, self.V):
                    for end_y in range(y, self.V + 1):
                        if (end_y - y) < 2 or (end_y - y) > max_allowed_height:
                            continue
                        max_allowed_width = np.min(self.side[y:end_y])
                        if (end_x - x) > max_allowed_width:
                            continue
                        body = frozenset(get_pos(x=i, y=j) for i in range(x, end_x) for j in range(y, end_y))
                        disallow = frozenset(get_pos(x=i, y=j) for i in range(x-1, end_x+1) for j in range(y-1, end_y+1)) - body
                        self.shapes_on_board.add(ShapeOnBoard(
                            body=body,
                            is_active=self.model.NewBoolVar(f'{x}-{y}-{end_x}-{end_y}-is_active'),
                            disallow=disallow
                        ))
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        # if a piece is active then all its body is active and the disallow is inactive
        for shape in self.shapes_on_board:
            for pos in shape.body:
                self.model.Add(self.model_vars[pos] == 1).OnlyEnforceIf(shape.is_active)
            for pos in shape.disallow:
                if pos not in self.model_vars:
                    continue
                self.model.Add(self.model_vars[pos] == 0).OnlyEnforceIf(shape.is_active)
        # if a spot is active then exactly one piece (with a body there) is active
        for pos in get_all_pos(self.V, self.H):
            pieces_on_pos = [shape for shape in self.shapes_on_board if pos in shape.body]
            # if pos is on then exactly one shape is active. if pos is off then 0 shapes are active.
            self.model.Add(lxp.Sum([shape.is_active for shape in pieces_on_pos]) == self.model_vars[pos])
        for row in range(self.V):  # force side counts
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in get_row_pos(row, self.H)]) == self.side[row])
        for col in range(self.H):  # force top counts
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in get_col_pos(col, self.V)]) == self.top[col])


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

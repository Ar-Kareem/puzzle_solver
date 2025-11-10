from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos, get_next_pos, Direction, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


class Board:
    def __init__(self, board: np.array, id_board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.id_board = id_board
        self.V, self.H = board.shape
        self.pos_to_id: dict[Pos, int] = {pos: int(get_char(id_board, pos)) for pos in get_all_pos(self.V, self.H)}
        self.id_to_pos: dict[int, set[Pos]] = defaultdict(set)
        for pos in get_all_pos(self.V, self.H):
            self.id_to_pos[self.pos_to_id[pos]].add(pos)
        id_lens = set([len(v) for v in self.id_to_pos.values()])
        assert len(id_lens) == 1, f'all tatamis must have the same size, got {id_lens}'
        self.N = list(id_lens)[0]

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, int], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for n in range(1, self.N + 1):
                self.model_vars[(pos, n)] = self.model.NewBoolVar(f'{pos}:{n}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # every pos has exactly one number
            self.model.AddExactlyOne([self.model_vars[(pos, n)] for n in range(1, self.N + 1)])
            c = get_char(self.board, pos).strip()
            if c:  # force clues
                self.model.Add(self.model_vars[(pos, int(c))] == 1)
        for v in range(1, self.N + 1):
            for (_, pos_set) in self.id_to_pos.items():  # a tatami cannot have a repeating number
                self.model.AddExactlyOne([self.model_vars[(pos, v)] for pos in pos_set])
            for row in range(self.V):  # numbers repeat X times horizontally
                self.model.Add(lxp.Sum([self.model_vars[(pos, v)] for pos in get_row_pos(row, self.H)]) == int(np.ceil(self.V / self.N)))
            for col in range(self.H):  # numbers repeat X times vertically
                self.model.Add(lxp.Sum([self.model_vars[(pos, v)] for pos in get_col_pos(col, self.V)]) == int(np.ceil(self.H / self.N)))
            for pos in get_all_pos(self.V, self.H):  # numbers cannot touch horizontally or vertically
                right_pos = get_next_pos(pos, Direction.RIGHT)
                down_pos = get_next_pos(pos, Direction.DOWN)
                if in_bounds(right_pos, self.V, self.H):
                    self.model.Add(self.model_vars[(right_pos, v)] == 0).OnlyEnforceIf(self.model_vars[(pos, v)])
                if in_bounds(down_pos, self.V, self.H):
                    self.model.Add(self.model_vars[(down_pos, v)] == 0).OnlyEnforceIf(self.model_vars[(pos, v)])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: v for (pos, v), var in board.model_vars.items() if solver.Value(var)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, cell_flags=id_board_to_wall_fn(self.id_board), center_char=lambda r, c: str(single_res.assignment.get(get_pos(x=c, y=r), ''))))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

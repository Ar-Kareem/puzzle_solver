from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_next_pos, Direction, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


@dataclass(frozen=True)
class MagnetOnBoard:
    uid: str
    is_active: cp_model.IntVar
    str_rep: tuple[tuple[Pos, str], ...]


class Board:
    def __init__(self, board: np.array, top_pos: np.array, top_neg: np.array, side_pos: np.array, side_neg: np.array):
        assert (len(side_pos), len(top_pos)) == board.shape, 'side_pos and top_pos must be the same shape as the board'
        assert (len(side_neg), len(top_neg)) == board.shape, 'side_neg and top_neg must be the same shape as the board'
        self.board = board
        self.top_pos, self.top_neg = top_pos, top_neg
        self.side_pos, self.side_neg = side_pos, side_neg

        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.magnets: set[MagnetOnBoard] = set()
        self.pos_vars: dict[tuple[Pos, str], MagnetOnBoard] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for col_i in range(self.H):  # vertical magnets
            row_i = 0
            while row_i < self.V - 1:
                pos_1 = get_pos(x=col_i, y=row_i)
                if get_char(self.board, pos_1) != 'V':
                    row_i += 1
                    continue
                pos_2 = get_next_pos(pos_1, Direction.DOWN)
                self.add_magnet(pos_1, pos_2)
                row_i += 2  # skip next cell since it's already covered by this magnet
        for row_i in range(self.V):  # horizontal magnets
            col_i = 0
            while col_i < self.H - 1:
                pos_1 = get_pos(x=col_i, y=row_i)
                if get_char(self.board, pos_1) != 'H':
                    col_i += 1
                    continue
                pos_2 = get_next_pos(pos_1, Direction.RIGHT)
                self.add_magnet(pos_1, pos_2)
                col_i += 2  # skip next cell since it's already covered by this magnet

    def add_magnet(self, pos1: Pos, pos2: Pos):
        for v1, v2 in [('+', '-'), ('-', '+'), ('x', 'x')]:
            magnet = MagnetOnBoard(uid=f'{pos1}:{pos2}:{v1}{v2}', is_active=self.model.NewBoolVar(f'{pos1}:{pos2}:{v1}{v2}'), str_rep=((pos1, v1), (pos2, v2)))
            self.pos_vars[(pos1, v1)] = magnet
            self.pos_vars[(pos2, v2)] = magnet
            self.magnets.add(magnet)

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # each position has exactly one magnet
            self.model.AddExactlyOne([self.pos_vars[(pos, v)].is_active for v in ['+', '-', 'x']])
        for pos in get_all_pos(self.V, self.H):  # orthogonal positions can't both be + or -
            for v in ['+', '-']:
                magnet = self.pos_vars.get((pos, v))
                if magnet is None:
                    continue
                for direction in [Direction.DOWN, Direction.RIGHT]:
                    next_magnet = self.pos_vars.get((get_next_pos(pos, direction), v))
                    if next_magnet is None:
                        continue
                    self.model.AddBoolOr([magnet.is_active.Not(), next_magnet.is_active.Not()])  # ~magnet ∨ ~next_magnet
        for row in range(self.V):  # force side counts
            if self.side_pos[row] != -1:
                self.model.Add(lxp.Sum([self.pos_vars[(pos, '+')].is_active for pos in get_row_pos(row, self.H) if (pos, '+') in self.pos_vars]) == self.side_pos[row])
            if self.side_neg[row] != -1:
                self.model.Add(lxp.Sum([self.pos_vars[(pos, '-')].is_active for pos in get_row_pos(row, self.H) if (pos, '-') in self.pos_vars]) == self.side_neg[row])
        for col in range(self.H):  # force top counts
            if self.top_pos[col] != -1:
                self.model.Add(lxp.Sum([self.pos_vars[(pos, '+')].is_active for pos in get_col_pos(col, self.V) if (pos, '+') in self.pos_vars]) == self.top_pos[col])
            if self.top_neg[col] != -1:
                self.model.Add(lxp.Sum([self.pos_vars[(pos, '-')].is_active for pos in get_col_pos(col, self.V) if (pos, '-') in self.pos_vars]) == self.top_neg[col])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: (magnet.uid, s) for magnet in board.magnets for (pos, s) in magnet.str_rep if solver.BooleanValue(magnet.is_active)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(V=self.V, H=self.H,
                center_char=lambda r, c: single_res.assignment[get_pos(x=c, y=r)][1],
                cell_flags=id_board_to_wall_fn(np.array([[single_res.assignment.get(get_pos(x=c, y=r), (None, ' '))[0] for c in range(self.H)] for r in range(self.V)])),
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

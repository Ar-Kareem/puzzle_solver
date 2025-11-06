from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors8, get_pos, Direction, get_next_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def get_orthogonals_with_dist(pos: Pos, V: int, H: int) -> list[tuple[Pos, int]]:
    out = []
    for direction in Direction:
        current_pos = pos
        current_dist = 0
        while True:
            current_pos = get_next_pos(current_pos, direction)
            current_dist += 1
            if not in_bounds(current_pos, V, H):
                break
            out.append((current_pos, current_dist))
    return out


class Board:
    def __init__(self, board: np.array, id_board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert id_board.shape == board.shape, f'id_board and board must have the same shape, got {id_board.shape} and {board.shape}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        assert all(str(c.item()).isdecimal() for c in np.nditer(id_board)), 'id_board must contain only digits'
        self.board = board
        self.id_board = id_board
        self.V, self.H = board.shape
        self.id_to_pos: dict[int, set[Pos]] = defaultdict(set)
        for pos in get_all_pos(self.V, self.H):
            self.id_to_pos[int(get_char(self.id_board, pos))].add(pos)
        self.id_to_max_val: dict[int, int] = {id_: len(self.id_to_pos[id_]) for id_ in self.id_to_pos}
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, int], cp_model.IntVar] = {}
        self.pos_vars: dict[Pos, set[cp_model.IntVar]] = defaultdict(set)
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            id_ = int(get_char(self.id_board, pos))
            max_val = self.id_to_max_val[id_]
            for n in range(1, max_val + 1):
                self.model_vars[(pos, n)] = self.model.NewBoolVar(f'{pos}:{n}')
                self.pos_vars[pos].add(self.model_vars[(pos, n)])

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            self.model.AddExactlyOne(self.pos_vars[pos])  # each position has exactly one number
            c = get_char(self.board, pos).strip()  # force clues
            if c != '':
                self.model.Add(self.model_vars[(pos, int(c))] == 1)
        for id_ in self.id_to_pos:  # each group has at most one number
            max_val = self.id_to_max_val[id_]
            for n in range(1, max_val + 1):
                self.model.AddExactlyOne([self.model_vars[(pos, n)] for pos in self.id_to_pos[id_]])
        for pos in get_all_pos(self.V, self.H):
            # if pos is X then neighbors within X cant be X
            orthogonals = get_orthogonals_with_dist(pos, self.V, self.H)
            for neighbor, dist in orthogonals:
                cur_n = dist
                while True:
                    if (pos, cur_n) not in self.model_vars:  # current position cant be as high as "cur_n"
                        break
                    if (neighbor, cur_n) not in self.model_vars:  # neighbor position cant be as high as "cur_n"
                        break
                    self.model.Add(self.model_vars[(neighbor, cur_n)] == 0).OnlyEnforceIf(self.model_vars[(pos, cur_n)])
                    cur_n += 1

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: n for (pos, n), var in board.model_vars.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

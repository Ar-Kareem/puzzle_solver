from typing import Optional

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, Direction, in_bounds, get_next_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, or_constraint
from puzzle_solver.core.utils_visualizer import combined_function


def get_eq_var(model: cp_model.CpModel, a: cp_model.IntVar, b: cp_model.IntVar) -> cp_model.IntVar:
    eq_var = model.NewBoolVar(f'{a}:{b}:eq')
    model.Add(a == b).OnlyEnforceIf(eq_var)
    model.Add(a != b).OnlyEnforceIf(eq_var.Not())
    return eq_var


class Board:
    def __init__(self, board: np.array, horiz_board: np.array, vert_board: np.array, digits: Optional[list[int]] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((str(c.item()).strip() == '') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        assert horiz_board.shape == (self.V, self.H - 1), f'horiz_board must be {(self.V, self.H - 1)}, got {horiz_board.shape}'
        assert all((str(c.item()).strip() == '') or str(c.item()).strip() in ['B', 'W'] for c in np.nditer(horiz_board)), 'horiz_board must contain only space or digits'
        assert vert_board.shape == (self.V - 1, self.H), f'vert_board must be {(self.V - 1, self.H)}, got {vert_board.shape}'
        assert all((str(c.item()).strip() == '') or str(c.item()).strip() in ['B', 'W'] for c in np.nditer(vert_board)), 'vert_board must contain only space or digits'
        self.horiz_board = horiz_board
        self.vert_board = vert_board
        if digits is None:
            digits = list(range(1, max(self.V, self.H) + 1))
        assert len(digits) >= max(self.V, self.H), 'digits must be at least as long as the board'
        self.digits = digits

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.digits_2_1_ratio: dict[tuple[Pos, Pos], cp_model.IntVar] = {}
        self.digits_consecutive: dict[tuple[Pos, Pos], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        allowed_values = cp_model.Domain.FromValues(self.digits)
        for pos in get_all_pos(self.V, self.H):  # force clues
            self.model_vars[pos] = self.model.NewIntVarFromDomain(allowed_values, f'{pos}')
            for direction in [Direction.RIGHT, Direction.DOWN]:
                neighbor = get_next_pos(pos, direction)
                if not in_bounds(neighbor, self.V, self.H):
                    continue
                self.digits_2_1_ratio[(pos, neighbor)] = self.model.NewBoolVar(f'{pos}:{neighbor}:2_1')
                self.digits_consecutive[(pos, neighbor)] = self.model.NewBoolVar(f'{pos}:{neighbor}:consecutive')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            c = get_char(self.board, pos)
            if not str(c).isdecimal():
                continue
            self.model.Add(self.model_vars[pos] == int(c))
        # all columns and rows are unique
        for row in range(self.V):
            self.model.AddAllDifferent([self.model_vars[get_pos(x=c, y=row)] for c in range(self.H)])
        for col in range(self.H):
            self.model.AddAllDifferent([self.model_vars[get_pos(x=col, y=r)] for r in range(self.V)])
        for p in get_all_pos(self.V, self.H):  # force horiz and vert relationships between digits
            for direction in [Direction.RIGHT, Direction.DOWN]:
                neighbor = get_next_pos(p, direction)
                if not in_bounds(neighbor, self.V, self.H):
                    continue
                self.setup_aux(p, direction)
                c = get_char(self.horiz_board if direction == Direction.RIGHT else self.vert_board, p)
                if c == 'B':  # 2:1 ratio
                    self.model.Add(self.digits_2_1_ratio[(p, neighbor)] == 1)
                elif c == 'W':  # consecutive
                    self.model.Add(self.digits_consecutive[(p, neighbor)] == 1)
                else:  # neither
                    self.model.Add(self.digits_2_1_ratio[(p, neighbor)] == 0)
                    self.model.Add(self.digits_consecutive[(p, neighbor)] == 0)

    def setup_aux(self, pos: Pos, direction: Direction):
        neighbor = get_next_pos(pos, direction)
        a_plus_one_b = get_eq_var(self.model, self.model_vars[pos] + 1, self.model_vars[neighbor])
        b_plus_one_a = get_eq_var(self.model, self.model_vars[neighbor] + 1, self.model_vars[pos])
        or_constraint(self.model, self.digits_consecutive[(pos, neighbor)], [a_plus_one_b, b_plus_one_a])  # consecutive aux
        a_twice_b = get_eq_var(self.model, self.model_vars[pos], 2 * self.model_vars[neighbor])
        b_twice_a = get_eq_var(self.model, self.model_vars[neighbor], 2 * self.model_vars[pos])
        or_constraint(self.model, self.digits_2_1_ratio[(pos, neighbor)], [a_twice_b, b_twice_a])  # 2:1 ratio aux

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=1)

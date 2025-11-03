import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, get_next_pos, get_pos, Direction, in_bounds, get_char
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item().strip() == '') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.N = self.V * self.H

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.step_up: dict[tuple[Pos, Direction], cp_model.IntVar] = {}
        self.is_max: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}:num')
            self.is_max[pos] = self.model.NewBoolVar(f'{pos}:is_max')
            for direction in Direction8:
                next_pos = get_next_pos(pos, direction)
                if not in_bounds(next_pos, self.V, self.H):
                    continue
                self.step_up[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}:step_up')

    def add_all_constraints(self):
        self.model.AddAllDifferent(list(self.model_vars.values()))  # all numbers are unique
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos).strip()
            if c:
                self.model.Add(self.model_vars[pos] == int(c))
            self.model.Add(self.model_vars[pos] == self.N).OnlyEnforceIf(self.is_max[pos])
            self.model.Add(self.model_vars[pos] != self.N).OnlyEnforceIf(self.is_max[pos].Not())
            for direction in Direction8:
                next_pos = get_next_pos(pos, direction)
                if not in_bounds(next_pos, self.V, self.H):
                    continue
                self.model.Add(self.model_vars[pos] + 1 == self.model_vars[next_pos]).OnlyEnforceIf(self.step_up[(pos, direction)])
                self.model.Add(self.model_vars[pos] + 1 != self.model_vars[next_pos]).OnlyEnforceIf(self.step_up[(pos, direction)].Not())
        # each position has a direction that is +1 and a direction that is -1
        for pos in get_all_pos(self.V, self.H):
            s_plus_one = [self.step_up[(pos, direction)] for direction in Direction8 if (pos, direction) in self.step_up]
            self.model.AddBoolOr(s_plus_one + [self.is_max[pos]])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, in_bounds, get_next_pos, get_neighbors4, Direction, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def laser_out(board: np.array, init_pos: Pos) -> list[Pos]:
    'laser out in all 4 directions until we hit a wall or out of bounds'
    V, H = board.shape
    result = []
    for direction in Direction:
        cur_pos = init_pos
        while True:
            cur_pos = get_next_pos(cur_pos, direction)
            if not in_bounds(cur_pos, V, H) or get_char(board, cur_pos).strip() != '':
                break
            result.append(cur_pos)
    return result


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item().strip() in ['', 'W']) or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or W or numbers'
        self.board = board
        self.V, self.H = board.shape

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force N lights touching the number N
            c = get_char(self.board, pos).strip()
            if c not in ['', 'W']:
                self.model.Add(self.model_vars[pos] == 0)
                self.model.Add(lxp.Sum([self.model_vars[p] for p in get_neighbors4(pos, self.V, self.H)]) == int(c))
            else:  # not numbered, must be lit
                orthoginals = laser_out(self.board, pos)
                self.model.AddAtLeastOne([self.model_vars[p] for p in orthoginals] + [self.model_vars[pos]])
                for ortho in orthoginals:
                    self.model.Add(self.model_vars[ortho] == 0).OnlyEnforceIf(self.model_vars[pos])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1, center_char=lambda r, c: str(self.board[r, c]).strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

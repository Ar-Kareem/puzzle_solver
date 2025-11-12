import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, Direction, get_pos, get_ray
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.horiz_vars: dict[Pos, cp_model.IntVar] = {}
        self.vert_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.horiz_vars[pos] = self.model.NewBoolVar(f'{pos}:horiz')
            self.vert_vars[pos] = self.model.NewBoolVar(f'{pos}:vert')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if not str(c).isdecimal():
                self.model.AddExactlyOne([self.horiz_vars[pos], self.vert_vars[pos]])
                continue
            self.model.Add(self.horiz_vars[pos] + self.vert_vars[pos] == 0)  # spot with number has to be blank
            self.range_clue(pos, int(c))

    def range_clue(self, pos: Pos, k: int):
        vis_vars: list[cp_model.IntVar] = []
        d_to_var = {Direction.UP: self.vert_vars, Direction.DOWN: self.vert_vars, Direction.LEFT: self.horiz_vars, Direction.RIGHT: self.horiz_vars}
        for direction in Direction:  # Build visibility chains in four direction
            ray = get_ray(pos, direction, self.V, self.H)  # cells outward
            for idx in range(len(ray)):
                v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                and_constraint(self.model, target=v, cs=[d_to_var[direction][p] for p in ray[:idx+1]])
                vis_vars.append(v)
        self.model.Add(sum(vis_vars) == int(k))  # Sum of visible whites = 1 (itself) + sum(chains) == k

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: 'LR'*solver.Value(board.horiz_vars[pos]) + 'UD'*solver.Value(board.vert_vars[pos]) for pos in get_all_pos(board.V, board.H)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(self.board[r, c]).strip(), special_content=lambda r, c: single_res.assignment[get_pos(x=c, y=r)].strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

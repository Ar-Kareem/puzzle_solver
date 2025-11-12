from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, Direction, get_next_pos, get_opposite_direction, get_pos, get_ray, in_bounds
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, Direction], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                next_pos = get_next_pos(pos, direction)
                opposite_direction = get_opposite_direction(direction)
                if (next_pos, opposite_direction) in self.model_vars:
                    self.model_vars[(pos, direction)] = self.model_vars[(next_pos, opposite_direction)]
                elif not in_bounds(next_pos, self.V, self.H):
                    self.model_vars[(pos, direction)] = self.model.NewConstant(1)
                else:
                    self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if not str(c).isdecimal():
                continue
            self.range_clue(pos, int(c))
        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if d1 is None or d2 is None:  # cell center, only neighbor to its own walls
                return p1 == p2
            if p1 == p2 and d1 != d2:  # same position, different direction, is neighbor
                return True
            if get_next_pos(p1, d1) == p2 and d2 == get_opposite_direction(d1):
                return True
            return False
        not_walls = {k: v.Not() for k, v in self.model_vars.items()}
        cell_centers = {(k, None): self.model.NewConstant(1) for k in get_all_pos(self.V, self.H)}
        force_connected_component(self.model, {**not_walls, **cell_centers}, is_neighbor=is_neighbor)

    def range_clue(self, pos: Pos, k: int):
        vis_vars: list[cp_model.IntVar] = []
        for direction in Direction:  # Build visibility chains in four direction
            ray = get_ray(pos, direction, self.V, self.H, include_self=True)  # cells outward
            for idx in range(len(ray)):
                v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                and_constraint(self.model, target=v, cs=[self.model_vars[(p, direction)].Not() for p in ray[:idx+1]])
                vis_vars.append(v)
        self.model.Add(sum(vis_vars) == int(k))  # Sum of visible whites = 1 (itself) + sum(chains) == k

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = defaultdict(str)
            for pos in get_all_pos(self.V, self.H):
                for direction in Direction:
                    if (pos, direction) in board.model_vars and solver.Value(board.model_vars[(pos, direction)]) == 1:
                        assignment[pos] += direction.name[0]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, cell_flags=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), ''), center_char=lambda r, c: str(self.board[r, c]).strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=4)

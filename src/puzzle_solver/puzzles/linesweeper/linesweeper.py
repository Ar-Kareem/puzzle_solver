from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors8, get_pos, Direction, get_next_pos, get_opposite_direction, in_bounds
from puzzle_solver.core.utils_ortools import force_connected_component, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape

        self.model = cp_model.CpModel()
        self.cell_active: dict[Pos, cp_model.IntVar] = {}
        self.cell_direction: dict[tuple[Pos, Direction], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.cell_active[pos] = self.model.NewBoolVar(f'{pos}')
            for direction in Direction:
                next_pos = get_next_pos(pos, direction)
                opposite_direction = get_opposite_direction(direction)
                if (next_pos, opposite_direction) in self.cell_direction:
                    self.cell_direction[(pos, direction)] = self.cell_direction[(next_pos, opposite_direction)]
                elif not in_bounds(next_pos, self.V, self.H):
                    self.cell_direction[(pos, direction)] = self.model.NewConstant(0)
                else:
                    self.cell_direction[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force state
            sum_directions = lxp.Sum([self.cell_direction[(pos, direction)] for direction in Direction])
            self.model.Add(sum_directions == 2).OnlyEnforceIf(self.cell_active[pos])
            self.model.Add(sum_directions == 0).OnlyEnforceIf(self.cell_active[pos].Not())
            c = get_char(self.board, pos).strip()  # force clues
            if c:
                self.model.Add(self.cell_active[pos] == 0)
                self.model.Add(lxp.Sum([self.cell_active[n] for n in get_neighbors8(pos, self.V, self.H, include_self=False)]) == int(c))
        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if p1 == p2 and d1 != d2:  # same position, different direction, is neighbor
                return True
            if get_next_pos(p1, d1) == p2 and d2 == get_opposite_direction(d1):
                return True
            return False
        force_connected_component(self.model, self.cell_direction, is_neighbor=is_neighbor)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = defaultdict(str)
            for pos in get_all_pos(self.V, self.H):
                for direction in Direction:
                    if (pos, direction) in board.cell_direction and solver.Value(board.cell_direction[(pos, direction)]) == 1:
                        assignment[pos] += direction.name[0]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, show_grid=False,
                special_content=lambda r, c: single_res.assignment[get_pos(x=c, y=r)],
                center_char=lambda r, c: str(self.board[r, c]).strip())
            )
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

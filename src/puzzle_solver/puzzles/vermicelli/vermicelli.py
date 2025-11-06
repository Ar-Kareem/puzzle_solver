from collections import defaultdict
import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, Direction, get_next_pos, get_opposite_direction, get_pos, in_bounds
from puzzle_solver.core.utils_ortools import force_connected_component, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, walls: np.array):
        assert walls.ndim == 2, f'walls must be 2d, got {walls.ndim}'
        assert all((len(c.item().strip()) <= 2) and all(ch in ['U', 'L', 'D', 'R'] for ch in c.item().strip()) for c in np.nditer(walls)), 'walls must contain only U, L, D, R'
        self.walls = walls
        self.V, self.H = walls.shape

        self.model = cp_model.CpModel()
        self.cell_active: dict[Pos, cp_model.IntVar] = {}
        self.cell_direction: dict[tuple[Pos, Direction], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                next_pos = get_next_pos(pos, direction)
                opposite_direction = get_opposite_direction(direction)
                if (next_pos, opposite_direction) in self.cell_direction:
                    self.cell_direction[(pos, direction)] = self.cell_direction[(next_pos, opposite_direction)]
                else:
                    self.cell_direction[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        # force the already given walls
        str_to_direction = {'U': Direction.UP, 'L': Direction.LEFT, 'D': Direction.DOWN, 'R': Direction.RIGHT}
        for pos in get_all_pos(self.V, self.H):
            for char in get_char(self.walls, pos).strip():
                self.model.Add(self.cell_direction[(pos, str_to_direction[char])] == 0)

        # all cells have exactly 2 directions
        for pos in get_all_pos(self.V, self.H):
            s = sum([self.cell_direction[(pos, direction)] for direction in Direction])
            self.model.Add(s == 2)

        # cant point to border
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                next_pos = get_next_pos(pos, direction)
                if not in_bounds(next_pos, self.V, self.H):
                    self.model.Add(self.cell_direction[(pos, direction)] == 0)

        # force single connected component
        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if p1 == p2:  # same position, different direction, is neighbor
                return True
            if get_next_pos(p1, d1) == p2 and d2 == get_opposite_direction(d1):
                return True
            return False
        force_connected_component(self.model, self.cell_direction, is_neighbor=is_neighbor)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = defaultdict(str)
            for (pos, direction), var in board.cell_direction.items():
                assignment[pos] += direction.name[0] if solver.BooleanValue(var) else ''
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, cell_flags=lambda r, c: self.walls[r, c],
            special_content=lambda r, c: single_res.assignment[get_pos(x=c, y=r)].strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=20)

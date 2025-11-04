from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_char, get_next_pos, get_opposite_direction, get_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() in [' ', '#']) or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        number_set = set(int(c.item()) for c in np.nditer(board) if str(c.item()).isdecimal())
        self.N = max(number_set)
        assert number_set == set(range(1, self.N + 1)), 'numbers must be consecutive integers starting from 1'
        self.board = board
        self.V, self.H = board.shape
        self.fixed_pos: dict[Pos, int] = {pos: int(get_char(self.board, pos).strip()) for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos).strip() not in ['', '#']}
        self.board_char: dict[Pos, str] = {pos: get_char(self.board, pos).strip() for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos).strip() != '#'}

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, int], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.board_char:
            for direction in Direction:
                next_pos = get_next_pos(pos, direction)
                opposite_direction = get_opposite_direction(direction)
                if not in_bounds(next_pos, self.V, self.H):
                    continue
                if get_char(self.board, next_pos).strip() == '#':
                    continue
                if (next_pos, opposite_direction) in self.model_vars:
                    self.model_vars[(pos, direction)] = self.model_vars[(next_pos, opposite_direction)]
                else:
                    self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def is_neighbor(self, pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
        p1, d1 = pd1
        p2, d2 = pd2
        if p1 == p2:
            return True
        p1_pointing_to_p2 = get_next_pos(p1, d1) == p2
        if not p1_pointing_to_p2:
            return False
        is_fixed = d2 == 'FIXED_NODE'  # pointing to a fixed node
        return is_fixed or d2 == get_opposite_direction(d1)

    def add_all_constraints(self):
        for pos, c in self.fixed_pos.items():
            target = 1 if (c == self.N) or (c == 1) else 2
            self.model.Add(lxp.Sum([var for (p, _), var in self.model_vars.items() if p == pos]) == target)
        for pos in self.board_char:
            if pos in self.fixed_pos:
                continue
            self.model.Add(lxp.Sum([var for (p, _), var in self.model_vars.items() if p == pos]) == 2)
        force_connected_component(self.model, self.model_vars, is_neighbor=self.is_neighbor)
        self.implement_height_constraints()

    def implement_height_constraints(self):
        """Every node has a height equal to every other non-fixed node that is connected to it. or equal to (+0 or +1) of the height of a fixed node it is connected to"""
        nodes = [(k, v) for k, v in self.model_vars.items() if k[0] not in self.fixed_pos]  # filter out fixed positions
        fixed_nodes = [(pos, 'FIXED_NODE') for pos in self.fixed_pos]
        node_heights = {(pos, 'FIXED_NODE'): self.model.NewConstant(c) for pos, c in self.fixed_pos.items()}
        for k, v in nodes:
            node_heights[k] = self.model.NewIntVar(0, self.N, f'node_height[{k}]')
            self.model.Add(node_heights[k] == 0).OnlyEnforceIf(v.Not())
        for (k, v) in nodes:
            h = node_heights[k]
            connected_nodes = [(k2, v2) for k2, v2 in nodes if self.is_neighbor(k, k2)]
            for (k2, v2) in connected_nodes:  # all pairs of non-fixed nodes that are connected to each other must have the same height
                self.model.Add(h == node_heights[k2]).OnlyEnforceIf([v, v2])
            connected_fixed_nodes = [node_heights[k2] for k2 in fixed_nodes if self.is_neighbor(k, k2)]
            for h2 in connected_fixed_nodes:  # connected to fixed node must have height of fixed node or 1 higher
                zero_or_one = self.model.NewBoolVar(f'zero_or_one[{k}]')  # node with height h can be connected to fixed node with height h or h+1
                self.model.Add(zero_or_one == 0).OnlyEnforceIf([v.Not()])
                self.model.Add(h == h2 + zero_or_one).OnlyEnforceIf([v])

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
            print(combined_function(self.V, self.H, show_border_only=True, is_shaded=lambda r, c: get_char(self.board, get_pos(x=c, y=r)).strip() == '#',
                special_content=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] if get_pos(x=c, y=r) in single_res.assignment else None,
                center_char=lambda r, c: get_char(self.board, get_pos(x=c, y=r)).strip().replace('#', '')))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, Direction, in_bounds, get_next_pos, get_opposite_direction, get_pos, get_neighbors4
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function


def get_ray(pos: Pos, direction: Direction, V: int, H: int) -> list[Pos]:
    out = []
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
        out.append(pos)
    return out


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, Direction], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[(pos, 'FILLED')] = self.model.NewBoolVar(f'{pos}:FILLED')
            self.model_vars[(pos, 'NUMBER')] = self.model.NewBoolVar(f'{pos}:NUMBER')
            for direction in Direction:
                next_pos = get_next_pos(pos, direction)
                opposite_direction = get_opposite_direction(direction)
                if (next_pos, opposite_direction) in self.model_vars:
                    self.model_vars[(pos, direction)] = self.model_vars[(next_pos, opposite_direction)]
                elif not in_bounds(next_pos, self.V, self.H):
                    self.model_vars[(pos, direction)] = self.model.NewConstant(0)
                else:
                    self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        pos_in_ray = set()  # keep track of all positions that are hit by rays; if a position has no ray then it cannot be filled
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos).strip()
            if c:
                d, num = c[0], int(c[1:])
                d = {'U': Direction.UP, 'D': Direction.DOWN, 'L': Direction.LEFT, 'R': Direction.RIGHT}[d]
                ray = get_ray(pos, d, self.V, self.H)
                pos_in_ray.update(ray)
                self.model.Add(self.model_vars[(pos, 'NUMBER')] == 1)
                self.model.Add(lxp.Sum([self.model_vars[(p, 'FILLED')] for p in ray]) == num)
            else:
                self.model.Add(self.model_vars[(pos, 'NUMBER')] == 0)
            lxp_sum = lxp.Sum([self.model_vars[(pos, direction)] for direction in Direction])
            self.model.Add(lxp_sum == 0).OnlyEnforceIf(self.model_vars[(pos, 'NUMBER')])
            self.model.Add(lxp_sum == 0).OnlyEnforceIf(self.model_vars[(pos, 'FILLED')])
            self.model.Add(lxp_sum == 2).OnlyEnforceIf([self.model_vars[(pos, 'NUMBER')].Not(), self.model_vars[(pos, 'FILLED')].Not()])
            for n in get_neighbors4(pos, self.V, self.H):  # filled cannot be adjacent to another filled cell
                self.model.Add(self.model_vars[(n, 'FILLED')] == 0).OnlyEnforceIf(self.model_vars[(pos, 'FILLED')])
                self.model.Add(self.model_vars[(pos, 'FILLED')] == 0).OnlyEnforceIf(self.model_vars[(n, 'FILLED')])

        for pos in get_all_pos(self.V, self.H):  # if a position has not been hit by any ray then it cannot be filled
            if pos not in pos_in_ray:
                self.model.Add(self.model_vars[(pos, 'FILLED')] == 0)

        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            return (p1 == p2) or (get_next_pos(p1, d1) == p2 and d2 == get_opposite_direction(d1))
        direction_vars = {k: v for k, v in self.model_vars.items() if isinstance(k[1], Direction)}
        force_connected_component(self.model, direction_vars, is_neighbor=is_neighbor)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = defaultdict(str)
            for (pos, aux), var in board.model_vars.items():
                if solver.BooleanValue(var):
                    assignment[pos] += aux.name[0] if isinstance(aux, Direction) else aux[0]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            answer = np.array([[single_res.assignment.get(get_pos(c, r), '') for c in range(self.H)] for r in range(self.V)])
            d = {'U': '↑', 'D': '↓', 'L': '←', 'R': '→'}
            num_arrow = np.array([[self.board[r, c][1:].strip() + d.get(self.board[r, c][0], '') for c in range(self.H)] for r in range(self.V)])
            print(combined_function(self.V, self.H,
                show_border_only=True,
                is_shaded=lambda r, c: answer[r, c] == 'F',
                special_content=lambda r, c: answer[r, c] if answer[r, c] not in ['N', 'F'] else None,
                center_char=lambda r, c: num_arrow[r, c],
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

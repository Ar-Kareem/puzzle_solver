from dataclasses import dataclass
from collections import defaultdict
from typing import Optional

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, Direction, get_next_pos, in_bounds, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


@dataclass(frozen=True)
class ShapeOnBoard:
    uid: str
    is_active: cp_model.IntVar


class Board:
    def __init__(self, board: np.array, target_pairs: Optional[list[tuple[int, int]]] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(str(i.item()).isdecimal() for i in np.nditer(board)), 'board must contain only digits'
        self.board = board
        self.V, self.H = board.shape
        self.target_pairs = target_pairs
        if target_pairs is None:
            nums = [int(i.item()) for i in np.nditer(board)]
            assert min(nums) == 0, 'expected board to start from 0'
            self.target_pairs = [(i, j) for i in range(max(nums) + 1) for j in range(i, max(nums) + 1)]

        self.model = cp_model.CpModel()
        self.pair_to_shapes: dict[tuple[int, int], set[ShapeOnBoard]] = defaultdict(set)
        self.pos_to_shapes: dict[Pos, set[ShapeOnBoard]] = defaultdict(set)
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in [Direction.RIGHT, Direction.DOWN]:
                next_pos = get_next_pos(pos, direction)
                if not in_bounds(next_pos, self.V, self.H):
                    continue
                c1 = int(get_char(self.board, pos))
                c2 = int(get_char(self.board, next_pos))
                pair = tuple(sorted((c1, c2)))
                uid = f'{pos.x}-{pos.y}-{direction.name[0]}'
                s = ShapeOnBoard(uid=uid, is_active=self.model.NewBoolVar(uid))
                self.pair_to_shapes[pair].add(s)
                self.pos_to_shapes[pos].add(s)
                self.pos_to_shapes[next_pos].add(s)

    def add_all_constraints(self):
        for pair in self.target_pairs:  # exactly one shape active for each pair
            self.model.AddExactlyOne(s.is_active for s in self.pair_to_shapes[pair])
        for pos in get_all_pos(self.V, self.H):  # at most one shape active at each position
            self.model.AddAtMostOne(s.is_active for s in self.pos_to_shapes[pos])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: s.uid for pos in get_all_pos(self.V, self.H) for s in self.pos_to_shapes[pos] if solver.Value(s.is_active) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(np.array([[single_res.assignment[get_pos(x=c, y=r)] for c in range(self.H)] for r in range(self.V)])),
                center_char=lambda r, c: str(self.board[r, c])
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

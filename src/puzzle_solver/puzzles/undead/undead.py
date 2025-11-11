from typing import Optional
from enum import Enum
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, get_next_pos, in_bounds, get_char, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Monster(Enum):
    VAMPIRE = "VAMPIRE"
    ZOMBIE = "ZOMBIE"
    GHOST = "GHOST"


@dataclass
class SingleBeamResult:
    position: Pos
    reflect_count: int


def can_see(reflect_count: int, monster: Monster) -> bool:
    if monster == Monster.ZOMBIE:
        return True
    elif monster == Monster.VAMPIRE:
        return reflect_count == 0
    elif monster == Monster.GHOST:
        return reflect_count > 0


def beam(board, start_pos: Pos, direction: Direction) -> list[SingleBeamResult]:
    V, H = board.shape
    cur_result: list[SingleBeamResult] = []
    reflect_count = 0
    cur_pos = start_pos
    while True:
        if not in_bounds(cur_pos, V, H):
            break
        cur_pos_char = get_char(board, cur_pos)
        if cur_pos_char == '//':
            direction = {
                Direction.RIGHT: Direction.UP,
                Direction.UP: Direction.RIGHT,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.DOWN
            }[direction]
            reflect_count += 1
        elif cur_pos_char == '\\':
            direction = {
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.RIGHT,
                Direction.UP: Direction.LEFT,
                Direction.LEFT: Direction.UP
            }[direction]
            reflect_count += 1
        else:  # not a mirror
            cur_result.append(SingleBeamResult(cur_pos, reflect_count))
        cur_pos = get_next_pos(cur_pos, direction)
    return cur_result


class Board:
    def __init__(self, board: np.array, sides: dict[str, np.array], monster_count: Optional[dict[Monster, int]] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert set(sides.keys()) == set(['right', 'left', 'top', 'bottom'])
        self.board = board
        self.V, self.H = board.shape
        assert sides['top'].shape == (self.H,) and sides['bottom'].shape == (self.H,) and sides['right'].shape == (self.V,) and sides['left'].shape == (self.V,), 'all sides must be equal to board size'
        self.sides = sides
        self.monster_count = monster_count or {}

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, str], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for monster in Monster:
                self.model_vars[(pos, monster)] = self.model.NewBoolVar(f"{pos}_is_{monster}")

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            if get_char(self.board, pos).strip():
                self.model.Add(lxp.Sum([self.model_vars[(pos, monster)] for monster in Monster]) == 0)
                continue
            self.model.AddExactlyOne([self.model_vars[(pos, monster)] for monster in Monster])
        for i, ground in enumerate(self.sides['top']):  # top edge
            if ground == -1:
                continue
            beam_result = beam(self.board, get_pos(x=i, y=0), Direction.DOWN)
            self.model.add(self.get_var(beam_result) == ground)
        for i, ground in enumerate(self.sides['left']):  # left edge
            if ground == -1:
                continue
            beam_result = beam(self.board, get_pos(x=0, y=i), Direction.RIGHT)
            self.model.add(self.get_var(beam_result) == ground)
        for i, ground in enumerate(self.sides['right']):  # right edge
            if ground == -1:
                continue
            beam_result = beam(self.board, get_pos(x=self.H-1, y=i), Direction.LEFT)
            self.model.add(self.get_var(beam_result) == ground)
        for i, ground in enumerate(self.sides['bottom']):  # bottom edge
            if ground == -1:
                continue
            beam_result = beam(self.board, get_pos(x=i, y=self.V-1), Direction.UP)
            self.model.add(self.get_var(beam_result) == ground)
        for monster, count in self.monster_count.items():
            self.model.add(lxp.Sum([self.model_vars.get((pos, monster), 0) for pos in get_all_pos(self.V, self.H)]) == count)

    def get_var(self, path: list[SingleBeamResult]) -> lxp:
        path_vars = []
        for square in path:
            assert get_char(self.board, square.position).strip() == '', f'square {square.position} is not a star position'
            for monster in Monster:
                if can_see(square.reflect_count, monster):
                    path_vars.append(self.model_vars[(square.position, monster)])
        return lxp.Sum(path_vars) if path_vars else 0

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: monster.name[0] for (pos, monster), var in board.model_vars.items() if solver.BooleanValue(var)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), self.board[r, c].replace('//', '/')).strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

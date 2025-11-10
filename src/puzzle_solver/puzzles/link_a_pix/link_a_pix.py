from dataclasses import dataclass
from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, shapes_between, Shape
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


@dataclass(frozen=True)
class ShapeOnBoard:
    uid: int
    is_active: cp_model.IntVar
    size: int
    shape: Shape


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        self.pos_to_char: dict[Pos, str] = {p: get_char(board, p).strip() for p in get_all_pos(self.V, self.H) if get_char(board, p).strip() != ''}

        self.model = cp_model.CpModel()
        self.all_shapes: list[ShapeOnBoard] = []
        self.pos_to_shapes: dict[Pos, set[ShapeOnBoard]] = defaultdict(set)
        self.create_shapes()
        self.add_all_constraints()

    def create_shapes(self):
        num_to_pos: dict[tuple[str, int], list[Pos]] = defaultdict(list)
        single_to_pos: list[tuple[str, Pos]] = []
        for p, s in self.pos_to_char.items():  # all cells that arent empty
            if s.isdecimal():  # black cell
                color = 'black'
                N = int(s)
            else:  # colored cell
                color = s.split('_')[0]
                N = int(s.split('_')[1])
            if N == 1:  # cell with a 1
                single_to_pos.append((color, p))
            else:  # cell with a number >= 2
                num_to_pos[(color, N)].append(p)

        for color, p in single_to_pos:  # all cells with a 1
            s = ShapeOnBoard(uid=len(self.all_shapes), is_active=self.model.NewBoolVar(f'{color}_{p}'), size=1, shape=frozenset([p]))
            self.all_shapes.append(s)
            self.pos_to_shapes[p].add(s)

        for (_, N), plist in num_to_pos.items():  # all cells with a number >= 2
            assert len(plist) % 2 == 0, f'{s} has {len(plist)} positions, must be even'
            for i, pi in enumerate(plist):
                for _j, pj in enumerate(plist[i+1:]):  # don't double count
                    self.populate_pair(pi, pj, N)

    def populate_pair(self, pos1: Pos, pos2: Pos, N: int):
        for shape in shapes_between(pos1, pos2, N):
            number_cells_hit = {p for p in shape if p in self.pos_to_char}
            assert number_cells_hit.issuperset({pos1, pos2}), f'Not possible! shape {shape} should always hit pos1 and pos2; this error means there\'s a bug in shapes_between'
            if number_cells_hit != {pos1, pos2}:  # shape hit some numbered cells other than pos1 and pos2
                continue
            s = ShapeOnBoard(uid=len(self.all_shapes), is_active=self.model.NewBoolVar(f'{shape}'), size=N, shape=shape)
            self.all_shapes.append(s)
            self.pos_to_shapes[pos1].add(s)
            self.pos_to_shapes[pos2].add(s)

    def add_all_constraints(self):
        for pos in self.pos_to_char.keys():  # every numbered cell must have exactly one shape active touch it
            shapes_on_pos = [s.is_active for s in self.pos_to_shapes[pos]]
            assert len(shapes_on_pos) >= 1, f'pos {pos} has no shapes on it. No solution possible!!!'
            self.model.AddExactlyOne(shapes_on_pos)
        for s1 in self.all_shapes:  # active shapes can't collide
            for s2 in self.all_shapes:
                if s1.uid != s2.uid and s1.shape.intersection(s2.shape):
                    self.model.Add(s1.is_active + s2.is_active <= 1)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: (s.uid, s.size) for s in self.all_shapes for pos in s.shape if solver.Value(s.is_active) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            arr_dict = {k: v[0] for k, v in single_res.assignment.items()}
            arr_size = {k: v[1] for k, v in single_res.assignment.items()}
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(np.array([[arr_dict.get(get_pos(x=c, y=r), "") for c in range(self.H)] for r in range(self.V)])),
                center_char=lambda r, c: f'{arr_size.get(get_pos(x=c, y=r), "")}'
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=99)

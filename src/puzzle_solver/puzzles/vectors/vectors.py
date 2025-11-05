from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_char, get_next_pos, get_pos, Shape, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


Block = tuple[Pos, int]  # a block has a position and a number


@dataclass(frozen=True)
class ShapeOnBoard:
    is_active: cp_model.IntVar
    uid: str
    number: int
    shape: Shape


def get_unblocked_ray(block: Block, direction: Direction, board: np.array) -> tuple[Pos, ...]:
    out = []
    pos = block[0]
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, board.shape[0], board.shape[1]):
            break
        if get_char(board, pos).strip() != '':
            break
        out.append(pos)
    return tuple(out)


def find_quadruplets(target: int, limits: tuple[int, int, int, int]):
    """
    Find all quadruplets (a, b, c, d) such that a + b + c + d = target and a, b, c, d are in the given limits.
    This is used to get all possible lengths for the four vectors coming out of a block and the limits are the maximum length of the vectors in each direction.
    """
    for a in range(limits[0] + 1):
        for b in range(limits[1] + 1):
            for c in range(limits[2] + 1):
                d = target - (a + b + c)
                if 0 <= d <= limits[3]:
                    yield (a, b, c, d)


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item().strip() in ['', '#']) or str(c.item()).strip().isdecimal() for c in np.nditer(board)), 'board must contain only space, #, or digits'
        self.board = board
        self.V, self.H = board.shape

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.blocks: list[Block] = [(pos, int(get_char(self.board, pos).strip())) for pos in get_all_pos(self.V, self.H) if str(get_char(self.board, pos).strip()).isdecimal()]
        self.blocks_to_shapes: dict[Block, set[ShapeOnBoard]] = {b: set() for b in self.blocks}
        self.pos_to_shapes: dict[Pos, set[ShapeOnBoard]] = {p: set() for p in get_all_pos(self.V, self.H)}
        self.init_shapes()
        self.add_all_constraints()

    def init_shapes(self):
        for block in self.blocks:
            direction_rays = [get_unblocked_ray(block, direction, self.board) for direction in Direction]
            num = block[1]
            for quadruplet in find_quadruplets(num, tuple(len(ray) for ray in direction_rays)):
                flat_pos_set = set(p for i in range(4) for p in direction_rays[i][:quadruplet[i]])
                shape = frozenset(flat_pos_set | {block[0]})
                uid = f'{block[0]}:{len(self.blocks_to_shapes[block])}'
                shape_on_board = ShapeOnBoard(is_active=self.model.NewBoolVar(f'{uid}:is_active'), shape=shape, uid=uid, number=num)
                self.blocks_to_shapes[block].add(shape_on_board)
                for p in shape:
                    self.pos_to_shapes[p].add(shape_on_board)

    def add_all_constraints(self):
        for block in self.blocks:  # every block has exactly one shape active
            self.model.AddExactlyOne(shape.is_active for shape in self.blocks_to_shapes[block])
        for pos in get_all_pos(self.V, self.H):  # every position has at most one shape active
            self.model.AddAtMostOne(shape.is_active for shape in self.pos_to_shapes[pos])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: (s.uid, s.number) for pos in get_all_pos(board.V, board.H) for s in board.pos_to_shapes[pos] if solver.Value(s.is_active) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            arr = np.array([[single_res.assignment.get(get_pos(x=c, y=r), (' ', ))[0] for c in range(self.H)] for r in range(self.V)])
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(arr),
                # center_char=lambda r, c: str(single_res.assignment.get(get_pos(x=c, y=r), (None, '#'))[1]),  # display number on every filled position
                center_char=lambda r, c: str(self.board[r, c]).strip(),  # only display the block number
                text_on_shaded_cells=False
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

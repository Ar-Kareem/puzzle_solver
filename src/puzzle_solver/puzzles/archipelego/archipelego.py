from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, get_pos, in_bounds, get_char, Direction, get_next_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function, id_assignment_to_wall_fn


@dataclass(frozen=True)
class Rectangle:
    id_: int
    active: cp_model.IntVar
    N: int
    clue_id: int
    width: int
    height: int
    body: frozenset[Pos]
    disallow: frozenset[Pos]
    perimeter: frozenset[Pos]


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.clue_pos: list[Pos] = [pos for pos in get_all_pos(self.V, self.H) if str(get_char(self.board, pos)).isdecimal()]
        self.clue_pos_to_id: dict[Pos, int] = {pos: i for i, pos in enumerate(self.clue_pos)}
        self.clue_pos_to_value: dict[Pos, int] = {pos: int(get_char(self.board, pos)) for pos in self.clue_pos}

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.rectangles: list[Rectangle] = []
        print('creating vars')
        self.create_vars()
        print(f'done, {len(self.rectangles)} rectangles created')
        self.add_all_constraints()
        print('done, adding constraints')

    def create_vars(self):
        self.fixed_pos: set[Pos] = set(self.clue_pos)
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')
            for width in range(1, self.H - pos.x + 1):
                for height in range(1, self.V - pos.y + 1):
                    body = frozenset({Pos(x=pos.x + i, y=pos.y + j) for i in range(width) for j in range(height)})
                    collides_with = body & self.fixed_pos
                    collide_N = None
                    collide_clue_id = None
                    if len(collides_with) > 1:
                        continue
                    if len(collides_with) == 1:
                        collide_N = self.clue_pos_to_value[list(collides_with)[0]]
                        collide_clue_id = self.clue_pos_to_id[list(collides_with)[0]]
                        if collide_N != width * height:
                            continue
                    disallow = frozenset({get_next_pos(p, direction) for p in body for direction in Direction} - body)  # disallow touching orthoginal
                    perimeter = frozenset({get_next_pos(p, direction) for p in body for direction in Direction8} - body - disallow)  # perimeter is diagonals
                    self.rectangles.append(Rectangle(id_=len(self.rectangles), active=self.model.NewBoolVar(f'{len(self.rectangles)}'), N=collide_N, clue_id=collide_clue_id, width=width, height=height, body=body, disallow=disallow, perimeter=perimeter))

    def add_all_constraints(self):
        for pos in get_all_pos(self.V-1, self.H-1):  # disallow 2x2 black squares
            block = [pos, get_next_pos(pos, Direction.RIGHT), get_next_pos(pos, Direction.DOWN), get_next_pos(pos, Direction8.DOWN_RIGHT)]
            self.model.AddBoolOr([self.model_vars[p] for p in block])
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(lxp.Sum([rectangle.active for rectangle in self.rectangles if pos in rectangle.body]) == self.model_vars[pos])
        for clue_id in self.clue_pos_to_id.values():  # each clue_id must have 1 rectangle active
            self.model.AddExactlyOne(rectangle.active for rectangle in self.rectangles if rectangle.clue_id == clue_id)
        for rectangle in self.rectangles:  # a rectangle being active means all its body ponts to the clue
            for pos in rectangle.body:
                self.model.Add(self.model_vars[pos] == 1).OnlyEnforceIf(rectangle.active)
            for pos in rectangle.disallow & self.model_vars.keys():
                self.model.Add(self.model_vars[pos] == 0).OnlyEnforceIf(rectangle.active)
        def is_neighbor(rect1: Rectangle, rect2: Rectangle) -> bool:
            return rect1.body & rect2.perimeter
        force_connected_component(self.model, {rectangle: rectangle.active for rectangle in self.rectangles}, is_neighbor=is_neighbor)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: rectangle.id_ for rectangle in self.rectangles for pos in rectangle.body if solver.Value(rectangle.active) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(
                self.V, self.H,
                cell_flags=id_assignment_to_wall_fn(single_res.assignment, self.V, self.H),
                # center_char=lambda r, c: self.board[r, c].strip(),
                center_char=lambda r, c: str(single_res.assignment.get(get_pos(x=c, y=r), '')),
                is_shaded=lambda r, c: get_pos(x=c, y=r) not in single_res.assignment,
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=99)

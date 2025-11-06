import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_next_pos, get_pos, in_bounds, Direction8, get_opposite_direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, start: Pos, end: Pos):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        assert in_bounds(start, self.V, self.H) and in_bounds(end, self.V, self.H), 'start and end must be within the board'
        self.numbers = sorted(set(int(c.item()) for c in np.nditer(board)))
        self.numbers_to_next: dict[int, int] = {}
        for i in range(len(self.numbers) - 1):
            self.numbers_to_next[self.numbers[i]] = self.numbers[i + 1]
        self.numbers_to_next[self.numbers[-1]] = self.numbers[0]
        self.start = start
        self.end = end

        self.model = cp_model.CpModel()
        self.from_to: dict[tuple[Pos, Direction8], cp_model.IntVar] = {}
        self.to_from: dict[tuple[Pos, Direction8], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            if pos == self.end:  # end shouldn't point
                continue
            target = self.numbers_to_next[int(get_char(self.board, pos))]
            for direction in Direction8:
                next_pos = get_next_pos(pos, direction)
                if not in_bounds(next_pos, self.V, self.H):
                    continue
                if next_pos == self.start:  # nothing should point at the start
                    continue
                if int(get_char(self.board, next_pos)) != target:
                    continue
                self.from_to[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')
                self.to_from[(next_pos, get_opposite_direction(direction))] = self.from_to[(pos, direction)]

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            if pos == self.end:  # end shouldn't point
                continue
            all_dirs = [self.from_to[(pos, direction)] for direction in Direction8 if (pos, direction) in self.from_to]
            assert len(all_dirs) > 0, f'no directions found for pos {pos}'
            self.model.Add(lxp.Sum(all_dirs) == 1)
        for pos in get_all_pos(self.V, self.H):
            if pos == self.start:  # start shouldn't be pointed at
                continue
            all_dirs = [self.to_from[(pos, direction)] for direction in Direction8 if (pos, direction) in self.to_from]
            assert len(all_dirs) > 0, f'no directions found for pos {pos}'
            self.model.Add(lxp.Sum(all_dirs) == 1)

        def is_neighbor(pd1: tuple[Pos, Direction8], pd2: tuple[Pos, Direction8]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if get_next_pos(p1, d1) == p2 or p1 == p2 or get_next_pos(p2, d2) == p1:
                return True
            return False
        force_connected_component(self.model, self.from_to, is_neighbor=is_neighbor)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: direction.name for (pos, direction), var in board.from_to.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            arrows = {Direction8.UP.name: '↑', Direction8.DOWN.name: '↓', Direction8.LEFT.name: '←', Direction8.RIGHT.name: '→', Direction8.UP_LEFT.name: '↖', Direction8.UP_RIGHT.name: '↗', Direction8.DOWN_LEFT.name: '↙', Direction8.DOWN_RIGHT.name: '↘', ' ': ' '}
            print(combined_function(self.V, self.H, center_char=lambda r, c: arrows[single_res.assignment.get(get_pos(x=c, y=r), ' ')]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

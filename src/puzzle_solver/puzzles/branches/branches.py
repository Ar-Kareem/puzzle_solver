import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, Direction, get_next_pos, in_bounds, get_opposite_direction, set_char
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def get_ray(pos: Pos, V: int, H: int, direction: Direction) -> list[Pos]:
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
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, Direction], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            dir_vars = [self.model_vars[(pos, direction)] for direction in Direction]
            c = get_char(self.board, pos)
            if not str(c).isdecimal():
                self.model.AddAtMostOne(dir_vars)
                continue
            self.model.Add(lxp.Sum(dir_vars) == 0)  # spot with number has to be blank
            self.range_clue(pos, int(c))

    def range_clue(self, pos: Pos, k: int):
        vis_vars: list[cp_model.IntVar] = []
        for direction in Direction:  # Build visibility chains in four direction
            branch_direction = get_opposite_direction(direction)
            ray = get_ray(pos, self.V, self.H, direction)  # cells outward
            for idx in range(len(ray)):
                v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                and_constraint(self.model, target=v, cs=[self.model_vars[(p, branch_direction)] for p in ray[:idx+1]])
                vis_vars.append(v)
        self.model.Add(sum(vis_vars) == int(k))  # Sum of visible whites = 1 (itself) + sum(chains) == k

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: direction.name[0] for (pos, direction), var in board.model_vars.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            d = {'U': Direction.UP, 'D': Direction.DOWN, 'L': Direction.LEFT, 'R': Direction.RIGHT}
            opp_d_char = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
            arr = np.full((self.V, self.H), '', dtype=object)
            center_char = np.full((self.V, self.H), '', dtype=object)
            for pos, direction in single_res.assignment.items():
                opp_direction = get_opposite_direction(d[direction])
                if single_res.assignment.get(get_next_pos(pos, opp_direction), '') == direction:
                    set_char(arr, pos, direction + opp_d_char[direction])
                else:
                    set_char(arr, pos, direction)
                    set_char(center_char, pos, '*')
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(self.board[r, c]).strip() or center_char[r, c].strip(), special_content=lambda r, c: arr[r, c]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

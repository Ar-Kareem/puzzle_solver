import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, in_bounds, Direction, get_next_pos, get_char
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


def get_ray(pos: Pos, V: int, H: int, direction: Direction) -> list[Pos]:
    out = []
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
        out.append(pos)
    return out


class Board:
    def __init__(self, board: np.ndarray):
        assert board.ndim == 2 and board.shape[0] > 0 and board.shape[1] > 0, f'board must be 2d, got {board.ndim}'
        assert all(str(i.item()).strip() in ['', 'W', 'P'] or str(i.item()).strip().isdecimal() for i in np.nditer(board)), f'board must be empty or a W or a P or a number, got {list(np.nditer(board))}'
        self.V, self.H = board.shape
        self.board = board

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.outside_fence: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f"{pos}")
            self.outside_fence[pos] = self.model_vars[pos].Not()

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            c = str(get_char(self.board, pos)).strip()
            if c == '':
                continue
            elif c in ['W', 'P']:  # cow or cactus
                self.model.Add(self.model_vars[pos] == (c == 'W'))
            else:
                self.range_clue(pos, int(c))
        force_connected_component(self.model, self.model_vars)
        def is_outside_neighbor(p1: Pos, p2: Pos) -> bool:
            if abs(p1.x - p2.x) + abs(p1.y - p2.y) == 1:  # manhattan distance is 1
                return True
            # both are on the border
            p1_on_border = p1.x == 0 or p1.x == self.V - 1 or p1.y == 0 or p1.y == self.H - 1
            p2_on_border = p2.x == 0 or p2.x == self.V - 1 or p2.y == 0 or p2.y == self.H - 1
            return p1_on_border and p2_on_border
        force_connected_component(self.model, self.outside_fence, is_neighbor=is_outside_neighbor)

    def range_clue(self, pos: Pos, c: int):
        self.model.Add(self.model_vars[pos] == 1)  # Force it white
        vis_vars: list[cp_model.IntVar] = []
        for direction in Direction:  # Build visibility chains in four direction
            ray = get_ray(pos, self.V, self.H, direction)  # cells outward
            for idx in range(len(ray)):
                v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                and_constraint(self.model, target=v, cs=[self.model_vars[p] for p in ray[:idx+1]])
                vis_vars.append(v)
        self.model.Add(1 + sum(vis_vars) == int(c))  # Sum of visible whites = 1 (itself) + sum(chains) == k

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(board.model_vars[pos]) for pos in get_all_pos(board.V, board.H)})
        def callback(single_res: SingleSolution):
            print("Solution:")
            print(combined_function(self.V, self.H,
            cell_flags=id_board_to_wall_fn(np.array([[single_res.assignment[get_pos(x=c, y=r)] for c in range(self.H)] for r in range(self.V)])),
            center_char=lambda r, c: self.board[r, c].strip(),
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

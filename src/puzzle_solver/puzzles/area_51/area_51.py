import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, get_char, get_pos, in_bounds, Direction, get_next_pos, get_neighbors4
from puzzle_solver.core.utils_ortools import and_constraint, force_connected_component, generic_solve_all, SingleSolution, or_constraint
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


def get_ray(pos: Pos, V: int, H: int, direction: Direction) -> list[Pos]:
    out = []
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
        out.append(pos)
    return out

def get_eq_var(model: cp_model.CpModel, a: cp_model.IntVar, b: cp_model.IntVar) -> cp_model.IntVar:
    eq_var = model.NewBoolVar(f'{a}:{b}:eq')
    model.Add(a == b).OnlyEnforceIf(eq_var)
    model.Add(a != b).OnlyEnforceIf(eq_var.Not())
    return eq_var

def enforce_groups_opposite_when(model: cp_model.CpModel, group_a: list[cp_model.IntVar], group_b: list[cp_model.IntVar]):
    gate = model.NewBoolVar(f"gate_opposite_when_b[{group_a}]:{group_b}")
    a0 = group_a[0]
    b0 = group_b[0]
    for v in group_a[1:]:  # all A equal
        model.Add(v == a0).OnlyEnforceIf(gate)
    for v in group_b[1:]:  # all B equal
        model.Add(v == b0).OnlyEnforceIf(gate)
    model.Add(a0 != b0).OnlyEnforceIf(gate)  # A different from B
    return gate

class Board:
    def __init__(self, board: np.array, dots: dict[Pos, str]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        chars = [c.item().strip() for c in np.nditer(board)]
        assert all(c in ['', 'A', 'C'] or c.isdecimal() or (c[0] == 'O' and c[1:].isdecimal()) for c in chars), 'board must contain only space or A or C or digits or O followed by a number'
        self.board = board
        self.V, self.H = board.shape
        assert all(in_bounds(pos, self.V+1, self.H+1) and v.strip() in ['B', 'W'] for pos, v in dots.items()), 'dots must be a dictionary of Pos to B or W'
        self.dots = dots

        self.model = cp_model.CpModel()
        self.b: dict[Pos, cp_model.IntVar] = {}
        self.w: dict[Pos, cp_model.IntVar] = {}
        self.debug = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.b[pos] = self.model.NewBoolVar(f"b[{pos}]")
            self.w[pos] = self.b[pos].Not()

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # For each numbered cell c with value k
            k = str(get_char(self.board, pos)).strip()
            if not k:
                continue
            if k[0] == 'O':
                k = int(k[1:])
                self.range_clues(pos, k)
            elif k.isdecimal():
                sum_white_neighbors = lxp.Sum([self.w[p] for p in get_neighbors4(pos, self.V, self.H)])
                sum_black_neighbors = 4 - sum_white_neighbors  # cells outside of border are black by default
                self.model.Add(sum_white_neighbors == int(k)).OnlyEnforceIf(self.b[pos])
                self.model.Add(sum_black_neighbors == int(k)).OnlyEnforceIf(self.w[pos])
            elif k == 'A':  # aliens must be inside fence
                self.model.Add(self.w[pos] == 1)
            elif k == 'C':  # cactus must be outside fence
                self.model.Add(self.b[pos] == 1)
        for pos, color in self.dots.items():
            if color == 'W':
                self.add_white_dot_constraints(pos)
            elif color == 'B':
                self.add_black_dot_constraints(pos)
                pass
            else:
                raise ValueError(f'Invalid color: {color}')
        force_connected_component(self.model, self.w)
        def is_outside_neighbor(p1: Pos, p2: Pos) -> bool:
            if abs(p1.x - p2.x) + abs(p1.y - p2.y) == 1:  # manhattan distance is 1
                return True
            # both are on the border
            p1_on_border = p1.x == 0 or p1.x == self.H - 1 or p1.y == 0 or p1.y == self.V - 1
            p2_on_border = p2.x == 0 or p2.x == self.H - 1 or p2.y == 0 or p2.y == self.V - 1
            return p1_on_border and p2_on_border
        force_connected_component(self.model, self.b, is_neighbor=is_outside_neighbor)

    def range_clues(self, pos: Pos, k: int):
        self.model.Add(self.w[pos] == 1)  # Force it white
        vis_vars: list[cp_model.IntVar] = []
        for direction in Direction:  # Build visibility chains in four direction
            ray = get_ray(pos, self.V, self.H, direction)  # cells outward
            for idx in range(len(ray)):
                v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                and_constraint(self.model, target=v, cs=[self.w[p] for p in ray[:idx+1]])
                vis_vars.append(v)
        self.model.Add(1 + sum(vis_vars) == int(k))  # Sum of visible whites = 1 (itself) + sum(chains) == k

    def get_2_by_2_block_vars(self, pos: Pos) -> tuple[cp_model.IntVar, ...]:
        # returns: the following 2x2 Y's along with the 8 X's
        # . X X .
        # X Y Y X
        # X Y Y X
        # . X X .
        br = pos
        bl = get_next_pos(br, Direction.LEFT)
        tr = get_next_pos(br, Direction.UP)
        tl = get_next_pos(tr, Direction.LEFT)
        tl_v = self.b.get(tl, self.model.NewConstant(1))
        tr_v = self.b.get(tr, self.model.NewConstant(1))
        bl_v = self.b.get(bl, self.model.NewConstant(1))
        br_v = self.b.get(br, self.model.NewConstant(1))
        tl_u_v = self.b.get(get_next_pos(tl, Direction.UP), self.model.NewConstant(1))
        tl_l_v = self.b.get(get_next_pos(tl, Direction.LEFT), self.model.NewConstant(1))
        tr_u_v = self.b.get(get_next_pos(tr, Direction.UP), self.model.NewConstant(1))
        tr_r_v = self.b.get(get_next_pos(tr, Direction.RIGHT), self.model.NewConstant(1))
        bl_l_v = self.b.get(get_next_pos(bl, Direction.LEFT), self.model.NewConstant(1))
        bl_d_v = self.b.get(get_next_pos(bl, Direction.DOWN), self.model.NewConstant(1))
        br_d_v = self.b.get(get_next_pos(br, Direction.DOWN), self.model.NewConstant(1))
        br_r_v = self.b.get(get_next_pos(br, Direction.RIGHT), self.model.NewConstant(1))
        return tl_v, tr_v, bl_v, br_v, tl_u_v, tl_l_v, tr_u_v, tr_r_v, bl_l_v, bl_d_v, br_d_v, br_r_v

    def add_white_dot_constraints(self, pos: Pos):
        # either  1x2 X over 1x2 ~X (horizontal variant)
        # or      2x1 X next to 2x1 ~X (vertical variant)
        tl, tr, bl, br, tl_u, tl_l, tr_u, tr_r, bl_l, bl_d, br_d, br_r = self.get_2_by_2_block_vars(pos)
        # 8 possibilities:
        # . X X .
        # X Y Y X
        # X Y Y X
        # . X X .
        # if the horizontal variant, then at least one of the X's on the left/right must be different
        # if the vertical variant, then at least one of the X's on the top/bottom must be different

        # horizontal variant will need at least one of these to be active
        tl_l_different = get_eq_var(self.model, tl, tl_l).Not()
        tr_r_different = get_eq_var(self.model, tr, tr_r).Not()
        bl_l_different = get_eq_var(self.model, bl, bl_l).Not()
        br_r_different = get_eq_var(self.model, br, br_r).Not()
        # vertical variant will need at least one of these to be active
        tl_u_different = get_eq_var(self.model, tl, tl_u).Not()
        tr_u_different = get_eq_var(self.model, tr, tr_u).Not()
        bl_d_different = get_eq_var(self.model, bl, bl_d).Not()
        br_d_different = get_eq_var(self.model, br, br_d).Not()

        horiz_variant_gate = self.model.NewBoolVar(f"horiz_variant_gate_w[{pos}]")
        self.model.Add(tl == tr).OnlyEnforceIf(horiz_variant_gate)
        self.model.Add(bl == br).OnlyEnforceIf(horiz_variant_gate)
        self.model.Add(tl != bl).OnlyEnforceIf(horiz_variant_gate)
        self.model.Add(tr != br).OnlyEnforceIf(horiz_variant_gate)
        self.model.Add(tl_l_different + tr_r_different + bl_l_different + br_r_different >= 1).OnlyEnforceIf(horiz_variant_gate)
        vert_variant_gate = self.model.NewBoolVar(f"vert_variant_gate_w[{pos}]")
        self.model.Add(tl == bl).OnlyEnforceIf(vert_variant_gate)
        self.model.Add(tr == br).OnlyEnforceIf(vert_variant_gate)
        self.model.Add(tl != tr).OnlyEnforceIf(vert_variant_gate)
        self.model.Add(bl != br).OnlyEnforceIf(vert_variant_gate)
        self.model.Add(tl_u_different + tr_u_different + bl_d_different + br_d_different >= 1).OnlyEnforceIf(vert_variant_gate)
        self.model.AddBoolOr([horiz_variant_gate, vert_variant_gate])
        self.debug[(pos, 'horiz_variant_gate')] = horiz_variant_gate
        self.debug[(pos, 'vert_variant_gate')] = vert_variant_gate

    def add_black_dot_constraints(self, pos: Pos):
        # in the 2x2 block, one block is X and the other 3 are ~X
        tl, tr, bl, br, tl_u, tl_l, tr_u, tr_r, bl_l, bl_d, br_d, br_r = self.get_2_by_2_block_vars(pos)
        # that one the is X must also have it's 2 corresponding outward neighbors also be X
        # V1: block tl is the one that is different from the other 3
        gate_1 = enforce_groups_opposite_when(self.model, [tl, tl_u, tl_l], [tr, bl, br, bl_l, tr_u])
        # V2: block tr is the one that is different from the other 3
        gate_2 = enforce_groups_opposite_when(self.model, [tr, tr_u, tr_r], [tl, bl, br, tl_u, br_r])
        # V3: block bl is the one that is different from the other 3
        gate_3 = enforce_groups_opposite_when(self.model, [bl, bl_l, bl_d], [tl, tr, br, tl_l, br_d])
        # V4: block br is the one that is different from the other 3
        gate_4 = enforce_groups_opposite_when(self.model, [br, br_d, br_r], [tl, tr, bl, bl_d, tr_r])
        self.debug[(pos, 'gate_1')] = gate_1
        self.debug[(pos, 'gate_2')] = gate_2
        self.debug[(pos, 'gate_3')] = gate_3
        self.debug[(pos, 'gate_4')] = gate_4
        self.model.AddBoolOr([gate_1, gate_2, gate_3, gate_4])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            for k, v in board.debug.items():
                print(f'{k}: {solver.Value(v)}')
            return SingleSolution(assignment={pos: solver.Value(board.w[pos]) for pos in get_all_pos(board.V, board.H)})
        def callback(single_res: SingleSolution):
            print("Solution:")
            print(np.array([[single_res.assignment[get_pos(x=c, y=r)] for c in range(self.H)] for r in range(self.V)]))
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(np.array([[single_res.assignment[get_pos(x=c, y=r)] for c in range(self.H)] for r in range(self.V)]), border_is_wall=False, border_is=1),
                center_char=lambda r, c: self.board[r, c].strip(),
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

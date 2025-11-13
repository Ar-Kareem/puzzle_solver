from typing import Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.util.python import sorted_interval_list

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, get_char, Direction, get_col_pos, get_next_pos, get_pos, get_row_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def add_opcode_constraint(model: cp_model.CpModel, vlist: list[cp_model.IntVar], opcode: str, result: int):
    assert opcode in ['+', '-', '*', '/'], "Invalid opcode"
    assert opcode not in ['-', '/'] or len(vlist) == 2, f"Opcode '{opcode}' requires exactly 2 variables"
    if opcode == '+':
        model.Add(sum(vlist) == result)
    elif opcode == '*':
        model.AddMultiplicationEquality(result, vlist)
    elif opcode == '-':
        # either vlist[0] - vlist[1] == result OR vlist[1] - vlist[0] == result
        b = model.NewBoolVar('sub_gate')
        model.Add(vlist[0] - vlist[1] == result).OnlyEnforceIf(b)
        model.Add(vlist[1] - vlist[0] == result).OnlyEnforceIf(b.Not())
    elif opcode == '/':
        # either v0 / v1 == result or v1 / v0 == result
        b = model.NewBoolVar('div_gate')
        # Ensure no division by zero
        model.Add(vlist[0] != 0)
        model.Add(vlist[1] != 0)
        # case 1: v0 / v1 == result → v0 == v1 * result
        model.Add(vlist[0] == vlist[1] * result).OnlyEnforceIf(b)
        # case 2: v1 / v0 == result → v1 == v0 * result
        model.Add(vlist[1] == vlist[0] * result).OnlyEnforceIf(b.Not())


class Board:
    def __init__(self, circle_board: np.array, board: Optional[np.array] = None):
        assert circle_board.ndim == 2, f'circle_board must be 2d, got {circle_board.ndim}'
        self.circle_board = circle_board
        self.board = board
        self.V, self.H = circle_board.shape
        self.V += 1
        self.H += 1
        assert board is None or board.shape == (self.V, self.H), f'board must be {(self.V, self.H)}, got {board.shape}'
        self.N = max(self.V, self.H)

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V-1, self.H-1):  # enforce circles
            tl = self.model_vars[pos]
            tr = self.model_vars[get_next_pos(pos, Direction.RIGHT)]
            bl = self.model_vars[get_next_pos(pos, Direction.DOWN)]
            br = self.model_vars[get_next_pos(pos, Direction8.DOWN_RIGHT)]
            c = get_char(self.circle_board, pos).strip()
            if c == 'E':  # all are even
                domain = sorted_interval_list.Domain.FromValues(list(range(2, self.N+1, 2)))
                for v in [tl, tr, bl, br]:
                    self.model.AddLinearExpressionInDomain(v, domain)
            elif c == 'O':  # all are odd
                domain = sorted_interval_list.Domain.FromValues(list(range(1, self.N+1, 2)))
                for v in [tl, tr, bl, br]:
                    self.model.AddLinearExpressionInDomain(v, domain)
            elif c:
                result, opcode = c[:-1], c[-1]
                opcode = opcode.replace('x', '*')
                add_opcode_constraint(self.model, [tl, br], opcode, int(result))
                add_opcode_constraint(self.model, [tr, bl], opcode, int(result))
        for row in range(self.V):  # every row is unique
            self.model.AddAllDifferent([self.model_vars[p] for p in get_row_pos(row, self.H)])
        for col in range(self.H):  # every column is unique
            self.model.AddAllDifferent([self.model_vars[p] for p in get_col_pos(col, self.V)])
        if self.board is not None:
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos).strip()
                if c:
                    self.model.Add(self.model_vars[pos] == int(c))


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(board.model_vars[pos]) for pos in get_all_pos(board.V, board.H)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)]).strip()))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)

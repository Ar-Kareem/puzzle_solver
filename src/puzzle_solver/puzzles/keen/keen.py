from typing import Optional

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos
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
    def __init__(self, board: np.ndarray, block_results: dict[str, tuple[str, int]], clues: Optional[np.ndarray] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert clues is None or clues.shape == board.shape, f'clues must be 2d, got {clues.shape}'
        assert all((c.item().startswith('d') and c.item()[1:].isdecimal()) for c in np.nditer(board)), "board must contain 'd' prefixed digits"
        block_names = set(c.item() for c in np.nditer(board))
        assert set(block_results.keys()).issubset(block_names), f'block results must contain all block names, {block_names - set(block_results.keys())}'
        self.board = board
        self.clues = clues
        self.V, self.H = board.shape
        self.block_results = {block: (op, result) for block, (op, result) in block_results.items()}

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, max(self.V, self.H), f'{pos}')
        if self.clues is not None:
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.clues, pos).strip()
                if int(c) >= 1:
                    self.model.Add(self.model_vars[pos] == int(c))

    def add_all_constraints(self):
        for row in range(self.V):  # 1 number per row
            self.model.AddAllDifferent([self.model_vars[pos] for pos in get_row_pos(row, self.H)])
        for col in range(self.H):  # 1 number per column
            self.model.AddAllDifferent([self.model_vars[pos] for pos in get_col_pos(col, self.V)])
        for block, (op, result) in self.block_results.items():  # cage op code
            block_vars = [self.model_vars[p] for p in get_all_pos(self.V, self.H) if get_char(self.board, p) == block]
            add_opcode_constraint(self.model, vlist=block_vars, opcode=op, result=result)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(board.model_vars[pos]) for pos in get_all_pos(board.V, board.H)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment[get_pos(x=c, y=r)]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=10)

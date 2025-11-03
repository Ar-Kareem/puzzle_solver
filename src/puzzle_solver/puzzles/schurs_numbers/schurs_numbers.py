from dataclasses import dataclass
import json

from ortools.sat.python import cp_model

from puzzle_solver.core.utils_ortools import generic_solve_all


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[int, str]

    def get_hashable_solution(self) -> str:
        return json.dumps(self.assignment, sort_keys=True)


def all_pairs(lst: list[int]) -> list[tuple[int, int]]:
    for i, ni in enumerate(lst):
        for j, nj in enumerate(lst[i:]):
            yield ni, nj


class SchurNumbers:
    def __init__(self, colors: list[str], n: int):
        self.N = n
        self.num_colors = len(colors)
        self.int_to_color: dict[int, str] = {i+1: c for i, c in enumerate(colors)}

        self.model = cp_model.CpModel()
        self.model_vars: dict[int, cp_model.IntVar] = {}
        self.eq_vars: dict[tuple[int, int], cp_model.BoolVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for number in range(1, self.N + 1):
            self.model_vars[number] = self.model.NewIntVar(1, self.num_colors, f'{number}:color')
            for other_number in range(number + 1, self.N + 1):
                self.eq_vars[(number, other_number)] = self.model.NewBoolVar(f'{number} == {other_number}')

    def add_all_constraints(self):
        numbers = list(self.model_vars.keys())
        for (number, other_number) in self.eq_vars.keys():  # enforce auxiliary variables
            v = self.eq_vars[(number, other_number)]
            self.model.Add(self.model_vars[number] == self.model_vars[other_number]).OnlyEnforceIf(v)
            self.model.Add(self.model_vars[number] != self.model_vars[other_number]).OnlyEnforceIf(v.Not())

        for ni, nj in all_pairs(numbers):
            if ni + nj not in numbers:
                continue
            nk = ni + nj
            self.model.AddBoolOr([self.eq_vars[(ni, nk)].Not(), self.eq_vars[(nj, nk)].Not()])

    def count_num_ways(self) -> int:
        def board_to_solution(board: SchurNumbers, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={number: board.int_to_color[solver.Value(var)] for number, var in board.model_vars.items()})
        solutions = generic_solve_all(self, board_to_solution, callback=None, verbose=False)
        return len(solutions), solutions

    def is_feasible(self) -> bool:
        solver = cp_model.CpSolver()
        solver.solve(self.model)
        return solver.StatusName() in ['OPTIMAL', 'FEASIBLE']


def find_max_n(colors: list[str], n=1) -> int:
    while True:
        print(f'checking n = {n}')
        solver = SchurNumbers(colors=colors, n=n)
        if not solver.is_feasible():
            return n
        n += 1
    return n

import numpy as np

from puzzle_solver import archipelego_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '6', ' ', ' ', ' ', '9', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '8', ' ', ' '],
        [' ', ' ', '6', ' ', ' ', ' ', ' ', ' ', ' ', '2'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment


def test_toy():
    board = np.array([
        [' ', ' ', ' ', ' ', ' '],
        [' ', '6', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '4'],
        [' ', ' ', '1', ' ', ' '],
        [' ', '2', ' ', ' ', '2'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment


if __name__ == '__main__':
    test_toy()
    test_ground()

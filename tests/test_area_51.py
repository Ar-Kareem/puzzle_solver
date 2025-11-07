import numpy as np

from puzzle_solver import area_51_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
    board = np.array([
        ['  ', 'A ', '  ', '  ', '  ', '  ', '  ', 'O4'],
        ['  ', '  ', '  ', '2 ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '1 ', '  ', '1 ', '3 ', 'C '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  '],
        ['  ', '  ', '2 ', '1 ', '2 ', '1 ', '  ', '  '],
        ['  ', '  ', '  ', '2 ', '3 ', '  ', '2 ', '  '],
        ['  ', '  ', '1 ', '  ', '  ', '  ', '3 ', '  '],
        ['  ', '  ', '  ', '  ', '1 ', '  ', '  ', '  '],
        ['  ', '  ', '1 ', '  ', '  ', '  ', '  ', '2 '],
        ['3 ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ])
    dots = {
        get_pos(x=1, y=1): 'B', 
        get_pos(x=5, y=7): 'B',
        get_pos(x=5, y=1): 'W', get_pos(x=0, y=5): 'W', get_pos(x=1, y=6): 'W', get_pos(x=1, y=7): 'W',
        get_pos(x=7, y=7): 'W', 
        get_pos(x=6, y=8): 'W', 
        get_pos(x=6, y=9): 'W', 
        get_pos(x=2, y=10): 'W',
    }
    binst = solver.Board(board=board, dots=dots)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['1', '1', '1', '1', '0', '1', '1', '1'],
        ['1', '0', '0', '1', '0', '1', '1', '1'],
        ['1', '0', '1', '1', '1', '1', '0', '0'],
        ['0', '0', '0', '0', '0', '1', '1', '1'],
        ['1', '0', '1', '1', '1', '1', '0', '0'],
        ['1', '1', '1', '1', '0', '1', '1', '1'],
        ['0', '0', '0', '0', '0', '1', '0', '0'],
        ['1', '1', '0', '1', '1', '1', '1', '1'],
        ['0', '1', '1', '1', '1', '0', '0', '0'],
        ['1', '1', '1', '0', '1', '1', '1', '1']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_black_completely_surrounded_isnt_valid():
    # only one solution unless the black is completely surrounded by white (WHICH IS INVALID)
    board = np.array([
        ['2 ', '2 ', 'A '],
        ['2 ', '  ', '2 '],
        ['2 ', '2 ', '2 '],
    ])
    dots = {}
    binst = solver.Board(board=board, dots=dots)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'


if __name__ == "__main__":
    test_ground()
    test_black_completely_surrounded_isnt_valid()

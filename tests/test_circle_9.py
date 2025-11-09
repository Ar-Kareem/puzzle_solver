import numpy as np

from puzzle_solver import circle_9_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
    # https://files.krazydad.com/circle9/sfiles/circle9-classic-V2-B48.pdf
    board = np.array([
        ['7', '6', '9',  ' ', ' ', ' ',  '5', '4', '2'],
        [' ', ' ', ' ',  ' ', '9', '4',  ' ', '7', ' '],
        [' ', ' ', '8',  ' ', '8', ' ',  ' ', '6', '6'],

        [' ', ' ', ' ',  ' ', '3', ' ',  '7', ' ', ' '],
        ['2', '5', ' ',  '7', ' ', '8',  ' ', '7', '8'],
        [' ', ' ', '4',  ' ', '9', ' ',  ' ', ' ', ' '],

        ['3', '4', ' ',  ' ', '8', ' ',  '3', ' ', ' '],
        [' ', '2', ' ',  '6', '2', ' ',  ' ', ' ', ' '],
        ['8', '2', '7',  ' ', ' ', ' ',  '9', '1', '3'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['0', '0', '0', '', '', '', '0', '0', '1'],
        ['', '', '', '', '0', '1', '', '0', ''],
        ['', '', '1', '', '0', '', '', '0', '0'],
        ['', '', '', '', '0', '', '1', '', ''],
        ['0', '1', '', '0', '', '0', '', '0', '0'],
        ['', '', '0', '', '1', '', '', '', ''],
        ['1', '0', '', '', '0', '', '0', '', ''],
        ['', '0', '', '1', '0', '', '', '', ''],
        ['0', '0', '0', '', '', '', '0', '1', '0']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground2():
    board = np.array([
        ['6', ' ', '1',  ' ', ' ', ' ',  '1', ' ', '2'],
        [' ', ' ', ' ',  '2', ' ', '2',  ' ', ' ', ' '],
        [' ', '3', ' ',  ' ', '8', ' ',  ' ', '9', ' '],

        ['8', ' ', '9',  ' ', ' ', ' ',  '2', ' ', '9'],
        [' ', ' ', ' ',  ' ', '3', ' ',  ' ', ' ', ' '],
        ['6', ' ', '1',  ' ', ' ', ' ',  '4', ' ', '8'],

        [' ', '5', ' ',  ' ', '2', ' ',  ' ', '7', ' '],
        [' ', ' ', ' ',  '9', ' ', '7',  ' ', ' ', ' '],
        ['3', ' ', '8',  ' ', ' ', ' ',  '1', ' ', '6'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'


if __name__ == '__main__':
    test_ground()
    test_ground2()

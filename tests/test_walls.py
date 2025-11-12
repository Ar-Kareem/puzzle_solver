import numpy as np

from puzzle_solver import walls_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    board = np.array([
        [' ', ' ', '7', ' ', ' ', ' ', ' ', '1', ' '],
        ['4', ' ', ' ', ' ', ' ', '4', ' ', ' ', ' '],
        [' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', '4'],
        [' ', '1', ' ', ' ', ' ', ' ', '4', ' ', ' '],
        [' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' '],
        [' ', ' ', '8', ' ', ' ', ' ', ' ', '5', ' '],
        ['6', ' ', ' ', ' ', ' ', '6', ' ', ' ', ' '],
        [' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', '5'],
        [' ', '4', ' ', ' ', ' ', ' ', '3', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['UD', 'LR', '', 'LR', 'LR', 'UD', 'UD', '', 'UD'],
        ['', 'LR', 'UD', 'UD', 'LR', '', 'UD', 'UD', 'UD'],
        ['UD', 'UD', 'UD', '', 'UD', 'UD', 'UD', 'LR', ''],
        ['UD', '', 'UD', 'UD', 'UD', 'UD', '', 'LR', 'UD'],
        ['LR', 'LR', 'UD', 'LR', '', 'LR', 'LR', 'LR', 'LR'],
        ['UD', 'UD', '', 'LR', 'LR', 'LR', 'LR', '', 'LR'],
        ['', 'LR', 'LR', 'LR', 'LR', '', 'LR', 'LR', 'UD'],
        ['UD', 'UD', 'LR', '', 'LR', 'LR', 'LR', 'LR', ''],
        ['LR', '', 'LR', 'LR', 'UD', 'LR', '', 'LR', 'LR']], dtype='<U2')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground2():
    board = np.array([
        [' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', '2', ' '],
        [' ', ' ', '1', ' ', ' ', '2', ' ', ' ', ' ', '2'],
        ['5', ' ', ' ', ' ', '4', ' ', ' ', '4', ' ', ' '],
        [' ', ' ', '3', ' ', ' ', '4', ' ', ' ', ' ', ' '],
        ['7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6', '6'],
        [' ', '2', ' ', ' ', '5', ' ', '6', ' ', ' ', ' '],
        [' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' '],
        ['4', ' ', '2', ' ', ' ', '4', ' ', '4', ' ', ' '],
        [' ', ' ', '4', ' ', ' ', ' ', ' ', ' ', ' ', '6'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['LR', 'LR', 'LR', '', 'LR', 'UD', 'UD', 'UD', '', 'LR'],
        ['UD', 'LR', '', 'UD', 'UD', '', 'UD', 'UD', 'UD', ''],
        ['', 'LR', 'LR', 'LR', '', 'UD', 'UD', '', 'LR', 'UD'],
        ['UD', 'LR', '', 'LR', 'LR', '', 'UD', 'UD', 'UD', 'UD'],
        ['', 'LR', 'LR', 'LR', 'UD', 'UD', 'UD', 'LR', '', ''],
        ['UD', '', 'LR', 'LR', '', 'LR', '', 'UD', 'UD', 'UD'],
        ['UD', 'LR', '', 'UD', 'UD', 'UD', '', 'UD', 'UD', 'UD'],
        ['UD', 'LR', 'LR', 'LR', '', 'UD', 'UD', 'UD', 'UD', 'UD'],
        ['', 'LR', '', 'LR', 'UD', '', 'LR', '', 'UD', 'UD'],
        ['LR', 'LR', '', 'LR', 'LR', 'UD', 'UD', 'LR', 'LR', '']],
        dtype='<U2')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()
    test_ground2()

import numpy as np

from puzzle_solver import linesweeper_solver as solver
from puzzle_solver.core.utils import get_pos


def test_toy():
    board = np.array([
        [' ', '3', ' ', ' ', '3', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        ['5', ' ', '3', ' ', ' ', '5'],
        [' ', ' ', ' ', '5', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['', '', '', '', '', ''],
        ['DR', 'LR', 'LR', 'LR', 'LR', 'DL'],
        ['UR', 'DL', '', '', 'DR', 'UL'],
        ['', 'UD', '', '', 'UD', ''],
        ['DR', 'UL', '', '', 'UR', 'DL'],
        ['UR', 'LR', 'LR', 'LR', 'LR', 'UL']], dtype='<U2')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    board = np.array([
        [' ', '3', ' ', ' ', ' ', ' ', '5', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '6', ' ', '5', ' ', ' ', ' ', ' ', ' ', '5'],
        [' ', ' ', '5', ' ', ' ', '7', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '6', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '7', '6', ' ', ' ', ' ', '7', ' ', '5'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '7', ' ', ' ', '8', ' ', '8', ' ', '8', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['3', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['', '', '', 'DR', 'LR', 'DL', '', 'DR', 'LR', 'DL'],
        ['DR', 'LR', 'LR', 'UL', '', 'UR', 'LR', 'UL', 'DR', 'UL'],
        ['UD', '', '', '', 'DR', 'LR', 'DL', '', 'UD', ''],
        ['UR', 'DL', '', 'DR', 'UL', '', 'UR', 'DL', 'UR', 'DL'],
        ['', 'UR', 'LR', 'UL', '', 'DR', 'LR', 'UL', 'DR', 'UL'],
        ['DR', 'DL', '', '', 'DR', 'UL', '', '', 'UD', ''],
        ['UD', 'UR', 'DL', 'DR', 'UL', 'DR', 'LR', 'DL', 'UR', 'DL'],
        ['UD', '', 'UR', 'UL', '', 'UD', '', 'UD', '', 'UD'],
        ['UR', 'DL', '', 'DR', 'DL', 'UR', 'DL', 'UR', 'DL', 'UD'],
        ['', 'UR', 'LR', 'UL', 'UR', 'LR', 'UL', '', 'UR', 'UL']],
        dtype='<U2')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()

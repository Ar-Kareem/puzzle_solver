import numpy as np

from puzzle_solver import yajilin_solver as solver
from puzzle_solver.core.utils import get_pos

def test_easy():
    # https://puzzlemadness.co.uk/yajilin/easy/2025/11/3
    board = np.array([
        ['R1', '  ', '  ', '  ', '  ', 'L1'],
        ['  ', '  ', 'R0', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', 'R0', '  '],
        ['  ', '  ', 'L0', '  ', '  ', '  '],
        ['  ', '  ', '  ', 'D1', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(repr(np.array([[solution.get(get_pos(c, r), ' ') for c in range(binst.H)] for r in range(binst.V)]).astype(str)))
    ground = np.array([
        ['N', 'DR', 'LR', 'DL', 'F', 'N'],
        ['DR', 'UL', 'N', 'UR', 'LR', 'DL'],
        ['UD', 'DR', 'LR', 'DL', 'N', 'UD'],
        ['UD', 'UD', 'N', 'UR', 'DL', 'UD'],
        ['UD', 'UR', 'DL', 'N', 'UD', 'UD'],
        ['UR', 'LR', 'UL', 'F', 'UR', 'UL']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    board = np.array([
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'D1'],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['D1', '  ', '  ', '  ', '  ', 'D1', '  ', '  ', '  '],
        ['  ', '  ', '  ', 'R2', '  ', '  ', '  ', 'L1', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', 'U1', '  ', '  '],
        ['  ', 'U0', '  ', 'D0', '  ', '  ', '  ', '  ', '  '],
        ['R2', '  ', 'U2', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', 'U0', '  ', '  ', 'D0', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(repr(np.array([[solution.get(get_pos(c, r), ' ') for c in range(binst.H)] for r in range(binst.V)]).astype(str)))
    ground = np.array([['DR', 'LR', 'LR', 'LR', 'LR', 'LR', 'LR', 'DL', 'N'],
        ['UR', 'DL', 'F', 'DR', 'LR', 'LR', 'DL', 'UR', 'DL'],
        ['N', 'UR', 'DL', 'UR', 'DL', 'N', 'UR', 'LR', 'UL'],
        ['DR', 'LR', 'UL', 'N', 'UR', 'DL', 'F', 'N', 'F'],
        ['UR', 'LR', 'LR', 'LR', 'DL', 'UD', 'N', 'DR', 'DL'],
        ['F', 'N', 'F', 'N', 'UD', 'UR', 'DL', 'UD', 'UD'],
        ['N', 'F', 'N', 'DR', 'UL', 'F', 'UR', 'UL', 'UD'],
        ['DR', 'LR', 'LR', 'UL', 'N', 'DR', 'DL', 'N', 'UD'],
        ['UR', 'LR', 'LR', 'LR', 'LR', 'UL', 'UR', 'LR', 'UL']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_easy()
    test_ground()

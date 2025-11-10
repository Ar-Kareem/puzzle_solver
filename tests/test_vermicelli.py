import numpy as np

from puzzle_solver import vermicelli_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    walls = np.array([
        ['  ', '  ', '  ', '  '],
        ['  ', '  ', 'UR', '  '],
        ['  ', '  ', '  ', '  '],
    ])
    binst = solver.Board(walls=walls)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(walls.shape[1])] for y in range(walls.shape[0])]).astype(str)))
    ground = np.array([['DR', 'LR', 'LR', 'DL'],
       ['UD', 'DR', 'DL', 'UD'],
       ['UR', 'UL', 'UR', 'UL']], dtype='<U2')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    walls = np.array([
        ['  ', '  ', '  ', '  ', 'D ', '  '],
        ['  ', '  ', '  ', 'DR', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['R ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', 'R ', '  '],
        ['  ', '  ', 'R ', '  ', '  ', '  '],
    ])
    binst = solver.Board(walls=walls)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(walls.shape[1])] for y in range(walls.shape[0])]).astype(str)))
    ground = np.array([['DR', 'LR', 'DL', 'DR', 'LR', 'DL'],
        ['UR', 'DL', 'UR', 'UL', 'DR', 'UL'],
        ['DR', 'UL', 'DR', 'DL', 'UR', 'DL'],
        ['UD', 'DR', 'UL', 'UR', 'DL', 'UD'],
        ['UD', 'UR', 'DL', 'DR', 'UL', 'UD'],
        ['UR', 'LR', 'UL', 'UR', 'LR', 'UL']], dtype='<U2')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground2():
    walls = np.array([
        ['  ', '  ', '  ', 'D ', '  ', '  ', 'R ', '  ', '  ', '  '],
        ['  ', 'D ', '  ', '  ', '  ', 'R ', 'D ', '  ', '  ', '  '],
        ['R ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', 'D ', '  ', '  ', '  ', '  ', '  ', 'R ', '  '],
        ['D ', '  ', 'R ', 'D ', '  ', 'DR', '  ', 'R ', 'D ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', 'D ', 'R ', 'D ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', 'R ', '  ', '  ', 'U ', '  '],
    ])
    binst = solver.Board(walls=walls)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(walls.shape[1])] for y in range(walls.shape[0])]).astype(str)))
    ground = np.array([['DR', 'DL', 'DR', 'LR', 'DL', 'DR', 'DL', 'DR', 'LR', 'DL'],
        ['UD', 'UR', 'UL', 'DR', 'UL', 'UD', 'UR', 'UL', 'DR', 'UL'],
        ['UD', 'DR', 'LR', 'UL', 'DR', 'UL', 'DR', 'DL', 'UR', 'DL'],
        ['UD', 'UR', 'LR', 'DL', 'UR', 'DL', 'UD', 'UR', 'DL', 'UD'],
        ['UR', 'LR', 'DL', 'UR', 'LR', 'UL', 'UR', 'DL', 'UR', 'UL'],
        ['DR', 'DL', 'UD', 'DR', 'LR', 'LR', 'DL', 'UD', 'DR', 'DL'],
        ['UD', 'UR', 'UL', 'UR', 'LR', 'DL', 'UD', 'UR', 'UL', 'UD'],
        ['UR', 'LR', 'LR', 'LR', 'LR', 'UL', 'UR', 'LR', 'LR', 'UL']],
        dtype='<U2')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()
    test_ground2()

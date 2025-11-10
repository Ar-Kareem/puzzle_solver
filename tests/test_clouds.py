import numpy as np

from puzzle_solver import clouds_solver as solver
from puzzle_solver.core.utils import get_pos


def test_toy():
    side = np.array([2, 2])
    top = np.array([2, 2])
    binst = solver.Board(side=side, top=top)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(top.shape[0])] for y in range(side.shape[0])]).astype(str)))
    ground = np.array([['1', '1'], ['1', '1']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground():
    side = np.array([2, 9, 9, 0, 4, 4, 3, 6, 6, 3])
    top = np.array([7, 7, 7, 4, 2, 5, 5, 3, 3, 3])
    binst = solver.Board(side=side, top=top)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(top.shape[0])] for y in range(side.shape[0])]).astype(str)))
    ground = np.array([['0', '0', '0', '0', '0', '0', '0', '0', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['1', '1', '1', '1', '0', '0', '0', '0', '0', '0'],
        ['1', '1', '1', '1', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '1', '1', '1', '0', '0'],
        ['1', '1', '1', '0', '0', '1', '1', '1', '0', '0'],
        ['1', '1', '1', '0', '0', '1', '1', '1', '0', '0'],
        ['1', '1', '1', '0', '0', '0', '0', '0', '0', '0']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground2():
    side = np.array([5, 7, 7, 4, 2, 7, 5, 7, 2, 2, 2, 10, 8, 3])
    top = np.array([6, 6, 3, 5, 4, 4, 5, 8, 6, 3, 3, 6, 6, 6])
    binst = solver.Board(side=side, top=top)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(top.shape[0])] for y in range(side.shape[0])]).astype(str)))
    ground = np.array([['1', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0'],
        ['1', '1', '0', '0', '1', '1', '0', '1', '1', '1', '0', '0', '0', '0'],
        ['1', '1', '0', '0', '1', '1', '0', '1', '1', '1', '0', '0', '0', '0'],
        ['1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1'],
        ['0', '0', '1', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1'],
        ['0', '0', '1', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0'],
        ['0', '0', '1', '1', '0', '0', '1', '1', '1', '0', '1', '1', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
        ['1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['1', '1', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1'],
        ['0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()
    test_ground2()

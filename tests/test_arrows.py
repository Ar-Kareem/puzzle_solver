import numpy as np

from puzzle_solver import arrows_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    board = np.array([
        [4, 4, 4],
        [4, 4, 4],
        [4, 4, 4],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(-1, board.shape[1]+1)] for y in range(-1, board.shape[0]+1)]).astype(str)))
    ground = np.array([['', 'DOWN', 'DOWN', 'DOWN', ''],
        ['RIGHT', '', '', '', 'LEFT'],
        ['RIGHT', '', '', '', 'LEFT'],
        ['RIGHT', '', '', '', 'LEFT'],
        ['', 'UP', 'UP', 'UP', '']], dtype='<U5')
    ground_assignment = {get_pos(x=x-1, y=y-1): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    board = np.array([
        [3, 1, 4, 1, 3, 2, 3, 2],
        [5, 2, 4, 4, 2, 3, 4, 4],
        [5, 5, 4, 3, 6, 2, 5, 6],
        [5, 2, 4, 2, 3, 4, 3, 3],
        [3, 1, 2, 2, 2, 2, 3, 2],
        [3, 2, 3, 2, 5, 1, 4, 4],
        [5, 1, 3, 3, 2, 4, 2, 3],
        [2, 2, 2, 0, 3, 0, 3, 1],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(-1, board.shape[1]+1)] for y in range(-1, board.shape[0]+1)]).astype(str)))
    ground = np.array([['', 'DOWN', 'DOWN_RIGHT', 'DOWN', 'DOWN_LEFT', 'DOWN_RIGHT', 'DOWN_RIGHT', 'DOWN_RIGHT', 'DOWN', ''],
        ['DOWN_RIGHT', '', '', '', '', '', '', '', '', 'DOWN_LEFT'],
        ['UP_RIGHT', '', '', '', '', '', '', '', '', 'LEFT'],
        ['RIGHT', '', '', '', '', '', '', '', '', 'LEFT'],
        ['RIGHT', '', '', '', '', '', '', '', '', 'UP_LEFT'],
        ['UP_RIGHT', '', '', '', '', '', '', '', '', 'UP_LEFT'],
        ['UP_RIGHT', '', '', '', '', '', '', '', '', 'LEFT'],
        ['RIGHT', '', '', '', '', '', '', '', '', 'UP_LEFT'],
        ['UP_RIGHT', '', '', '', '', '', '', '', '', 'UP_LEFT'],
        ['', 'UP', 'UP_RIGHT', 'UP_LEFT', 'UP_RIGHT', 'UP', 'UP_LEFT','UP', 'UP_LEFT', '']], dtype='<U10')
    ground_assignment = {get_pos(x=x-1, y=y-1): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
    test_toy()
    test_ground()

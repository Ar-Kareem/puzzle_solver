import numpy as np

from puzzle_solver import branches_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', '2'],
        ['5', ' ', '7', ' ', ' ', ' '],
        [' ', ' ', ' ', '3', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', '2'],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '7', ' ', ' ', '3', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['D', 'D', 'D', 'R', 'R', ' '],
        [' ', 'D', ' ', 'L', 'L', 'L'],
        ['U', 'D', 'U', ' ', 'L', 'D'],
        ['U', 'D', 'U', 'U', 'D', ' '],
        ['U', 'D', 'U', 'U', 'D', 'U'],
        ['U', ' ', 'L', 'L', ' ', 'L']], dtype='<U1')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()

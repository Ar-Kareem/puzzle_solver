import numpy as np

from puzzle_solver import hidden_stars_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    # Q = up-left, W = up, E = up-right, A = left, D = right, Z = down-left, X = down, C = down-right
    board = np.array([
        [' ', 'C', 'A', ' ', 'X', ' ', 'X'],
        ['C', ' ', 'Z', 'C', ' ', 'Z', ' '],
        ['D', ' ', ' ', ' ', 'W', ' ', ' '],
        [' ', ' ', 'X', ' ', ' ', ' ', ' '],
        [' ', ' ', 'A', ' ', ' ', ' ', ' '],
        ['W', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'W', ' ', ' ', 'A', 'Q', ' '],
    ])
    side = np.array([1, 2, 2, 1, 1, 3, 1])
    top = np.array([1, 3, 2, 1, 2, 1, 1])
    binst = solver.Board(board=board, side=side, top=top)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['1', ' ', ' ', '0', ' ', '0', ' '],
       [' ', '0', ' ', ' ', '1', ' ', '1'],
       [' ', '1', '0', '1', ' ', '0', '0'],
       ['0', '0', ' ', '0', '0', '1', '0'],
       ['0', '1', ' ', '0', '0', '0', '0'],
       [' ', '1', '1', '0', '1', '0', '0'],
       ['0', ' ', '1', '0', ' ', ' ', '0']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()

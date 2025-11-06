import numpy as np

from puzzle_solver import cow_and_cactus_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    board = np.array([
        ['  ', '  ', '15', '  ', '11', '9 ', '8 ', '11'],
        ['  ', '  ', '  ', 'P ', '  ', '  ', '  ', '  '],
        ['W ', '3 ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['W ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['W ', '  ', '  ', '  ', '  ', 'W ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '4 ', '  '],
        ['W ', '  ', '  ', '  ', 'W ', 'W ', 'P ', 'W '],
        ['P ', 'W ', '  ', '  ', 'W ', 'W ', '  ', 'P '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=c, y=r), ' ') for c in range(board.shape[1])] for r in range(board.shape[0])]).astype(str)))
    ground = np.array([['1', '1', '1', '1', '1', '1', '1', '1'],
        ['0', '0', '1', '0', '1', '1', '0', '1'],
        ['1', '1', '1', '0', '1', '0', '0', '1'],
        ['1', '0', '1', '0', '1', '1', '0', '1'],
        ['1', '0', '1', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '0', '1'],
        ['0', '1', '1', '0', '1', '1', '0', '0']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()

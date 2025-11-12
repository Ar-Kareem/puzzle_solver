import numpy as np

from puzzle_solver import rooms_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    board = np.array([
        ['1', '6', ' ', '2', ' ', '3', '2', ' ', '3', ' '],
        ['2', ' ', '2', '2', '9', ' ', '8', '5', ' ', '7'],
        ['4', '8', ' ', '1', '8', '3', ' ', '5', '6', ' '],
        [' ', ' ', '3', '2', ' ', '3', ' ', ' ', '6', '6'],
        ['2', '7', '3', ' ', '9', ' ', '5', '3', '1', ' '],
        [' ', '6', '5', '3', ' ', '7', ' ', '3', '2', '5'],
        ['3', '7', ' ', ' ', '11',' ', '5', '4', ' ', ' '],
        [' ', '2', '2', ' ', '9', '5', '2', ' ', '2', '6'],
        ['5', ' ', '3', '2', ' ', '6', '4', '3', ' ', '6'],
        [' ', '2', ' ', '1', '13',' ', '5', ' ', '5', '10'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['ULR', 'ULR', 'UL', 'UD', 'UDR', 'UL', 'UD', 'UR', 'ULR', 'ULR'],
        ['DL', 'R', 'LR', 'UL', 'UR', 'DL', 'U', 'D', ' ', 'R'],
        ['UL', ' ', 'DR', 'DLR', 'LR', 'UDL', ' ', 'U', 'R', 'LR'],
        ['LR', 'L', 'UR', 'UDL', ' ', 'UR', 'L', ' ', 'D', 'DR'],
        ['DLR', 'L', 'R', 'UDL', 'R', 'DL', 'R', 'DL', 'UDR', 'ULR'],
        ['ULR', 'LR', 'DL', 'UD', ' ', 'UR', 'DLR', 'UL', 'UR', 'LR'],
        ['LR', 'DL', 'UR', 'UL', ' ', ' ', 'UR', 'L', 'D', 'R'],
        ['LR', 'UL', 'DR', 'DLR', 'L', 'R', 'LR', 'DLR', 'UL', 'R'],
        ['DL', 'D', 'UR', 'UL', 'R', 'L', 'D', 'UR', 'DL', 'R'],
        ['UDL', 'UD', 'DR', 'DLR', 'DL', 'D', 'UD', 'D', 'UD', 'DR']],
        dtype='<U3')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()

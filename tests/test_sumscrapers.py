import numpy as np

from puzzle_solver import sumscrapers_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '2', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '3', ' ', '2'],
        [' ', ' ', ' ', '3', ' ', ' ', ' '],
        [' ', '4', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '5', ' ', ' '],
    ])
    top = np.array([' ', '13', '19', '7', ' ', '18', ' '])
    left = np.array(['15', '7', '12', '13', ' ', '16', '16'])
    right = np.array(['15', '18', '15', ' ', '13', ' ', ' '])
    bottom = np.array([' ', ' ', ' ', ' ', ' ', '7', '17'])
    binst = solver.Board(board=board, top=top, left=left, right=right, bottom=bottom)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['2', '6', '1', '7', '4', '5', '3'],
        ['7', '3', '2', '4', '6', '1', '5'],
        ['5', '7', '4', '1', '3', '6', '2'],
        ['6', '2', '5', '3', '1', '4', '7'],
        ['1', '4', '3', '5', '7', '2', '6'],
        ['4', '5', '7', '6', '2', '3', '1'],
        ['3', '1', '6', '2', '5', '7', '4']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()

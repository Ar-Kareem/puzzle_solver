import numpy as np

from puzzle_solver import mathrax_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    circle_board = np.array([
        [' ',  ' ',  ' ',  '3-', ' ',  ' '],
        [' ',  'O',  ' ',  '2-', ' ',  ' '],
        [' ',  ' ',  ' ',  ' ',  '5+', ' '],
        ['2-', ' ',  '1-',  ' ',  ' ',  ' '],
        [' ',  '1-', ' ',  ' ',  ' ',  '6x'],
        ['4x',  ' ',  ' ',  ' ',  ' ',  ' '],
    ])
    binst = solver.Board(circle_board=circle_board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1]+1)] for y in range(board.shape[0]+1)]).astype(str)))
    ground = np.array([['3', '5', '2', '6', '7', '1', '4'],
        ['6', '1', '5', '4', '3', '7', '2'],
        ['7', '3', '1', '5', '2', '4', '6'],
        ['4', '7', '6', '2', '1', '3', '5'],
        ['5', '6', '3', '7', '4', '2', '1'],
        ['2', '4', '7', '1', '5', '6', '3'],
        ['1', '2', '4', '3', '6', '5', '7']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground2():
    circle_board = np.array([
        [' ',  ' ',  '1-', '9+', ' ',  ' '],
        [' ',  '2-', ' ',  ' ',  ' ',  ' '],
        [' ',  ' ',  '1-', ' ',  'O',  ' '],
        [' ',  ' ',  ' ',  '4-', ' ',  ' '],
        [' ',  ' ',  ' ',  ' ',  ' ',  ' '],
        [' ',  ' ',  ' ',  ' ',  ' ',  ' '],
    ])
    board = np.array([
        [' ',  ' ',  ' ',  ' ',  ' ',  ' ', ' '],
        [' ',  ' ',  ' ',  ' ',  ' ',  '2', ' '],
        [' ',  ' ',  ' ',  ' ',  ' ',  '1', ' '],
        ['2',  ' ',  ' ',  '5',  ' ',  ' ', ' '],
        [' ',  ' ',  ' ',  ' ',  ' ',  ' ', ' '],
        ['3',  ' ',  ' ',  ' ',  ' ',  ' ', ' '],
        ['1',  ' ',  ' ',  ' ',  ' ',  '5', ' '],
    ])
    binst = solver.Board(circle_board=circle_board, board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(circle_board.shape[1]+1)] for y in range(circle_board.shape[0]+1)]).astype(str)))
    ground = np.array([['5', '1', '6', '4', '2', '7', '3'],
        ['4', '6', '3', '7', '5', '2', '1'],
        ['6', '5', '4', '2', '3', '1', '7'],
        ['2', '4', '1', '5', '7', '3', '6'],
        ['7', '2', '5', '3', '1', '6', '4'],
        ['3', '7', '2', '1', '6', '4', '5'],
        ['1', '3', '7', '6', '4', '5', '2']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
    test_ground()
    test_ground2()

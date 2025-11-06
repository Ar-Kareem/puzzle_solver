import numpy as np

from puzzle_solver import kropki_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    board = np.array([
        ['1', ' ', '2'],
        [' ', ' ', ' '],
        [' ', ' ', ' '],
    ])
    horiz_board = np.array([
        [' ', 'W'],
        ['W', ' '],
        ['W', 'W'],
    ])
    vert_board = np.array([
        ['W', ' ', 'W'],
        ['W', 'W', ' '],
    ])
    binst = solver.Board(board=board, horiz_board=horiz_board, vert_board=vert_board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['1', '3', '2'],
       ['2', '1', '3'],
       ['3', '2', '1']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '2', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '4', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
    ])
    horiz_board = np.array([
        [' ', ' ', ' ', ' ', 'W'],
        [' ', ' ', ' ', ' ', ' '],
        ['B', ' ', 'B', ' ', ' '],
        ['B', 'W', ' ', 'W', ' '],
        ['B', 'W', ' ', ' ', 'W'],
        [' ', 'W', ' ', 'W', 'W'],
    ])
    vert_board = np.array([
        [' ', ' ', ' ', ' ', ' ', 'W'],
        ['W', ' ', ' ', 'W', ' ', ' '],
        [' ', 'W', ' ', ' ', ' ', ' '],
        [' ', 'W', 'W', ' ', 'W', ' '],
        ['W', ' ', ' ', 'W', ' ', ' '],
    ])
    binst = solver.Board(board=board, horiz_board=horiz_board, vert_board=vert_board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['5', '1', '4', '6', '2', '3'],
       ['3', '5', '1', '4', '6', '2'],
       ['4', '2', '6', '3', '1', '5'],
       ['6', '3', '2', '5', '4', '1'],
       ['2', '4', '3', '1', '5', '6'],
       ['1', '6', '5', '2', '3', '4']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()

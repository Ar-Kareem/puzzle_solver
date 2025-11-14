import numpy as np

from puzzle_solver import archipelego_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '6', ' ', ' ', ' ', '9', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '8', ' ', ' '],
        [' ', ' ', '6', ' ', ' ', ' ', ' ', ' ', ' ', '2'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['', '7', '7', '', '22', '22', '22', '', '2', '2'],
        ['', '7', '7', '', '22', '22', '22', '', '2', '2'],
        ['', '7', '7', '', '22', '22', '22', '', '2', '2'],
        ['174', '', '', '26', '', '', '', '194', '', ''],
        ['', '36', '', '26', '', '226', '226', '', '41', ''],
        ['', '36', '', '26', '', '226', '226', '', '41', ''],
        ['', '36', '', '26', '', '226', '226', '', '41', ''],
        ['', '', '', '26', '', '', '', '', '41', ''],
        ['65', '65', '65', '', '55', '55', '55', '55', '', '66'],
        ['65', '65', '65', '', '55', '55', '55', '55', '', '66']],
        dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_toy():
    board = np.array([
        [' ', ' ', ' ', ' ', ' '],
        [' ', '6', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '4'],
        [' ', ' ', '1', ' ', ' '],
        [' ', '2', ' ', ' ', '2'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['2', '2', '', '', ''],
       ['2', '2', '', '10', '10'],
       ['2', '2', '', '10', '10'],
       ['', '', '11', '', ''],
       ['14', '14', '', '16', '16']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()

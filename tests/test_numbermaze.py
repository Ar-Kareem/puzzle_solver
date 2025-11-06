import numpy as np
from puzzle_solver import numbermaze_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
    board = np.array([
        ['#', ' ', ' ', ' ', ' '],
        ['1', ' ', ' ', ' ', ' '],
        [' ', ' ', '3', ' ', '#'],
        [' ', ' ', '#', ' ', '#'],
        [' ', ' ', '2', ' ', '#'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([
        ['', 'DR', 'LR', 'LR', 'DL'],
        ['D', 'UR', 'DL', 'DR', 'UL'],
        ['UR', 'DL', 'U', 'UD', ''],
        ['DR', 'UL', '', 'UD', ''],
        ['UR', 'LR', 'LR', 'UL', '']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_toy2():
    board = np.array([
        [' ', '1', '#'],
        ['2', ' ', ' '],
        [' ', ' ', '3'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([
        ['DR', 'L', ''],
        ['UD', 'DR', 'DL'],
        ['UR', 'UL', 'U']])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_toy3():
    board = np.array([
        ['#', ' ', ' ', '#'],
        ['1', ' ', ' ', ' '],
        ['#', '#', '#', ' '],
        ['#', '3', ' ', ' '],
        ['#', '#', ' ', '2'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([
        ['', 'DR', 'DL', ''],
        ['R', 'UL', 'UR', 'DL'],
        ['', '', '', 'UD'],
        ['', 'R', 'DL', 'UD'],
        ['', '', 'UR', 'UL']])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground2():
    # https://puzzlemadness.co.uk/numbermaze/hard/2025/11/4
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '3', ' ', '5', ' ', ' ', '4', ' ', '7'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '#', ' ', ' ', '#', ' ', '6', '8', ' '],
        ['2', ' ', '#', '#', ' ', ' ', ' ', ' ', ' '],
        ['#', ' ', '1', ' ', ' ', '#', ' ', '#', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['9', ' ', '10', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', ' ', ' ', '11', '#', ' ', ' ', ' ', '#'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([
        ['DR', 'LR', 'LR', 'LR', 'LR', 'LR', 'DL', 'DR', 'DL'],
        ['UR', 'DL', 'DR', 'LR', 'LR', 'LR', 'UL', 'UD', 'UD'],
        ['DR', 'UL', 'UD', 'DR', 'LR', 'DL', 'DR', 'UL', 'UD'],
        ['UD', '', 'UR', 'UL', '', 'UR', 'UL', 'DR', 'UL'],
        ['UR', 'DL', '', '', 'DR', 'LR', 'DL', 'UR', 'DL'],
        ['', 'UR', 'L', 'DR', 'UL', '', 'UD', '', 'UD'],
        ['DR', 'LR', 'LR', 'UL', 'DR', 'LR', 'UL', 'DR', 'UL'],
        ['UR', 'DL', 'DR', 'DL', 'UR', 'DL', '', 'UD', ''],
        ['', 'UR', 'UL', 'U', '', 'UR', 'LR', 'UL', '']])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground3():
    board = np.array([
        ['7', ' ', '#', ' ', '2', ' '],
        [' ', ' ', '#', ' ', ' ', ' '],
        [' ', ' ', '1', ' ', '3', '9'],
        [' ', ' ', ' ', ' ', '4', ' '],
        [' ', '6', ' ', '5', ' ', ' '],
        [' ', ' ', ' ', '8', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 2, f'unique solutions != 1, == {len(solutions)}'


if __name__ == '__main__':
    test_ground()
    test_toy2()
    test_toy3()
    test_ground2()
    test_ground3()

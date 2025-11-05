import numpy as np
from puzzle_solver import trees_logic_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    board = np.array([
        ['01', '01', '02', '02', '02'],
        ['01', '02', '02', '05', '05'],
        ['03', '03', '03', '05', '05'],
        ['04', '03', '04', '05', '05'],
        ['04', '04', '04', '05', '05'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['0', '0', '0', '1', '0'],
       ['1', '0', '0', '0', '0'],
       ['0', '0', '1', '0', '0'],
       ['0', '0', '0', '0', '1'],
       ['0', '1', '0', '0', '0']])
    ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # https://www.sporcle.com/games/Katie_Wandering/trees-logic-puzzle-xxx
    board = np.array([
        ['01', '01', '02', '02', '02', '03', '03', '03'],
        ['04', '01', '01', '02', '08', '03', '08', '08'],
        ['04', '01', '01', '02', '08', '08', '08', '08'],
        ['04', '01', '01', '02', '02', '05', '05', '05'],
        ['04', '01', '01', '01', '02', '02', '05', '05'],
        ['04', '04', '01', '01', '02', '06', '06', '06'],
        ['04', '04', '04', '04', '07', '07', '07', '06'],
        ['04', '04', '07', '07', '07', '06', '06', '06'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['0', '0', '0', '0', '0', '0', '1', '0'],
        ['0', '0', '0', '0', '1', '0', '0', '0'],
        ['0', '1', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '1', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '1'],
        ['0', '0', '0', '0', '0', '1', '0', '0'],
        ['1', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '1', '0', '0', '0', '0', '0']])
    ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()

import numpy as np
from puzzle_solver import number_path_solver as solver
from puzzle_solver.core.utils import Pos, Direction8, get_pos

def test_toy():
    board = np.array([
        ['1', '2', '3'],
        ['4', '3', '4'],
        ['1', '2', '1'],
    ])
    start = Pos(x=0, y=0)
    end = Pos(x=0, y=2)
    binst = solver.Board(board=board, start=start, end=end)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['R', 'R', 'D'],
        ['D', 'L', 'D'],
        [' ', 'U', 'L'],
    ])
    d = {'R': Direction8.RIGHT.name, 'D': Direction8.DOWN.name, 'L': Direction8.LEFT.name, 'U': Direction8.UP.name, 'UL': Direction8.UP_LEFT.name, 'UR': Direction8.UP_RIGHT.name, 'DL': Direction8.DOWN_LEFT.name, 'DR': Direction8.DOWN_RIGHT.name}
    ground_assignment = {get_pos(x=x, y=y): d[ground[y][x]] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground():
    board = np.array([
        ['3', '2', '4', '1', '2', '3', '1', '2'],
        ['4', '3', '1', '4', '3', '1', '4', '3'],
        ['2', '1', '2', '4', '2', '4', '4', '1'],
        ['3', '1', '3', '1', '2', '3', '2', '4'],
        ['4', '1', '2', '3', '2', '1', '3', '1'],
        ['2', '3', '4', '4', '1', '4', '3', '2'],
        ['3', '1', '4', '3', '3', '4', '1', '4'],
        ['2', '4', '1', '2', '1', '2', '3', '2'],
    ])
    start = Pos(x=6, y=6)
    end = Pos(x=7, y=6)
    binst = solver.Board(board=board, start=start, end=end)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment


if __name__ == '__main__':
    test_toy()
    test_ground()

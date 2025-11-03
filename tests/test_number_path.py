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
    # print(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str))
    ground = np.array([['DOWN', 'LEFT', 'RIGHT', 'RIGHT', 'RIGHT', 'DOWN_RIGHT', 'RIGHT', 'DOWN'],
        ['DOWN_RIGHT', 'UP_RIGHT', 'UP_LEFT', 'LEFT', 'LEFT', 'DOWN_LEFT', 'UP', 'DOWN_LEFT'],
        ['DOWN', 'LEFT', 'UP_LEFT', 'DOWN', 'UP', 'UP', 'RIGHT', 'DOWN_LEFT'],
        ['DOWN', 'DOWN_RIGHT', 'UP_RIGHT', 'UP_LEFT', 'DOWN_LEFT', 'UP', 'DOWN', 'DOWN'],
        ['UP_RIGHT', 'DOWN_LEFT', 'UP', 'DOWN_LEFT', 'UP_RIGHT', 'UP_LEFT', 'UP_RIGHT', 'DOWN'],
        ['RIGHT', 'DOWN_RIGHT', 'UP_LEFT', 'RIGHT', 'UP', 'UP', 'DOWN_RIGHT', 'LEFT'],
        ['DOWN_RIGHT', 'DOWN_LEFT', 'LEFT', 'UP', 'UP_RIGHT', 'DOWN_LEFT', 'DOWN_RIGHT', ''],
        ['UP', 'RIGHT', 'RIGHT', 'UP', 'RIGHT', 'UP_LEFT', 'UP_LEFT', 'LEFT']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()

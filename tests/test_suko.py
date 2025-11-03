import numpy as np
from puzzle_solver import suko_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    board = np.array([
        ['R', 'B', 'G'],
        ['R', 'B', 'G'],
        ['R', 'R', 'G'],
    ])
    quadrant = np.array([
        [21, 23],
        [17, 15],
    ])
    color_sums = {'R': 19, 'G': 17, 'B': 9}
    binst = solver.Board(board=board, quadrant=quadrant, color_sums=color_sums)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print([[solution[get_pos(x=x, y=y)] for x in range(board.shape[1])] for y in range(board.shape[0])])
    ground = np.array([[4, 7, 5], [8, 2, 9], [6, 1, 3]])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()

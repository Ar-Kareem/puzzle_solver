import numpy as np
from puzzle_solver import troix_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
    board = np.array([
        ['O', 'I', 'O', ' ', 'I', ' ', 'X', 'O', 'I'],
        [' ', 'O', ' ', 'I', ' ', 'X', ' ', 'X', ' '],
        ['I', ' ', 'X', ' ', 'I', ' ', 'I', ' ', 'X'],
        ['X', 'I', ' ', ' ', ' ', ' ', ' ', 'X', 'X'],
        [' ', ' ', 'O', 'I', ' ', 'X', 'X', ' ', ' '],
        ['I', 'O', ' ', ' ', ' ', ' ', ' ', 'I', 'I'],
        ['O', ' ', 'O', ' ', 'O', ' ', 'I', ' ', 'X'],
        [' ', 'X', ' ', 'I', ' ', 'O', ' ', 'O', ' '],
        ['X', 'O', 'X', ' ', 'O', ' ', 'O', 'I', 'I'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(np.array([[solution[get_pos(x=x, y=y)] for x in range(board.shape[1])] for y in range(board.shape[0])]))
    ground = np.array([
        ['O', 'I', 'O', 'X', 'I', 'X', 'X', 'O', 'I'],
        ['I', 'O', 'I', 'I', 'X', 'X', 'O', 'X', 'O'],
        ['I', 'X', 'X', 'O', 'I', 'O', 'I', 'O', 'X'],
        ['X', 'I', 'I', 'O', 'O', 'I', 'O', 'X', 'X'],
        ['O', 'X', 'O', 'I', 'I', 'X', 'X', 'I', 'O'],
        ['I', 'O', 'X', 'O', 'X', 'O', 'X', 'I', 'I'],
        ['O', 'I', 'O', 'X', 'O', 'I', 'I', 'X', 'X'],
        ['X', 'X', 'I', 'I', 'X', 'O', 'I', 'O', 'O'],
        ['X', 'O', 'X', 'X', 'O', 'I', 'O', 'I', 'I'],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()

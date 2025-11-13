import numpy as np

from puzzle_solver import tenner_grid_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', '0', '9', '1', '5'],
        [' ', '8', ' ', ' ', ' ', '5', ' ', ' ', '7', ' '],
        [' ', '5', ' ', '2', ' ', ' ', ' ', '1', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', '6', ' ', '9', '5', '7'],
        ['8', ' ', '0', ' ', '9', ' ', '5', ' ', ' ', ' '],
        ['7', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ])
    goal = np.array(['33', '22', '13', '34', '26', '41', '22', '29', '32', '18'])
    binst = solver.Board(board=board, goal=goal)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=c, y=r), ' ') for c in range(board.shape[1])] for r in range(board.shape[0])]).astype(str)))
    ground = np.array([['7', '3', '2', '4', '6', '8', '0', '9', '1', '5'],
        ['4', '8', '0', '9', '1', '5', '6', '2', '7', '3'],
        ['7', '5', '3', '2', '4', '9', '8', '1', '6', '0'],
        ['0', '2', '4', '8', '1', '6', '3', '9', '5', '7'],
        ['8', '1', '0', '3', '9', '7', '5', '6', '4', '2'],
        ['7', '3', '4', '8', '5', '6', '0', '2', '9', '1']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()

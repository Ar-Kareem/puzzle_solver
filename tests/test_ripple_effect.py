import numpy as np

from puzzle_solver import ripple_effect_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    id_board = np.array([
        ['00', '01', '02', '02', '03', '03', '04'],
        ['00', '05', '05', '02', '03', '06', '06'],
        ['07', '07', '05', '08', '03', '03', '06'],
        ['09', '07', '07', '07', '03', '10', '10'],
        ['11', '11', '12', '12', '13', '13', '10'],
        ['14', '11', '14', '12', '13', '15', '15'],
        ['14', '14', '14', '16', '13', '13', '15']
    ])
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', '5', ' '],
        [' ', ' ', '4', ' ', '6', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '1'],
        [' ', ' ', '1', ' ', ' ', ' ', ' '],
        [' ', '4', ' ', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board, id_board=id_board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['2', '1', '3', '1', '4', '2', '1'],
        ['1', '3', '1', '2', '1', '3', '2'],
        ['3', '1', '2', '1', '3', '5', '1'],
        ['1', '2', '4', '5', '6', '2', '3'],
        ['2', '1', '3', '1', '5', '4', '1'],
        ['5', '3', '1', '2', '1', '3', '2'],
        ['3', '4', '2', '1', '3', '2', '1']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()

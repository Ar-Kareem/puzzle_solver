import numpy as np

from puzzle_solver import tatami_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
    id_board = np.array([
        ['00', '01', '01', '01', '01', '01', '02', '03', '04', '05'],
        ['00', '06', '06', '06', '06', '06', '02', '03', '04', '05'],
        ['00', '07', '07', '07', '07', '07', '02', '03', '04', '05'],
        ['00', '08', '08', '08', '08', '08', '02', '03', '04', '05'],
        ['00', '09', '09', '09', '09', '09', '02', '03', '04', '05'],
        ['10', '10', '10', '10', '10', '11', '11', '11', '11', '11'],
        ['12', '12', '12', '12', '12', '13', '13', '13', '13', '13'],
        ['14', '14', '14', '14', '14', '15', '15', '15', '15', '15'],
        ['16', '16', '16', '16', '16', '17', '17', '17', '17', '17'],
        ['18', '18', '18', '18', '18', '19', '19', '19', '19', '19'],
    ])
    board = np.array([
        [' ', ' ', ' ', ' ', '2', '3', ' ', '4', ' ', ' '],
        [' ', '1', ' ', '5', '4', '2', '3', ' ', ' ', ' '],
        [' ', ' ', ' ', '4', ' ', '1', ' ', ' ', ' ', ' '],
        ['2', '1', ' ', ' ', '2', ' ', ' ', ' ', '5', ' '],
        ['3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5'],
        [' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '2', '5', ' ', '1', ' ', ' ', ' '],
        [' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' '],
        [' ', ' ', '4', '5', ' ', '2', ' ', '3', '5', ' '],
        [' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', '4'],
    ])
    binst = solver.Board(board=board, id_board=id_board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ' ') for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['1', '5', '1', '4', '2', '3', '5', '4', '2', '3'],
        ['5', '1', '3', '5', '4', '2', '3', '1', '4', '2'],
        ['4', '5', '2', '4', '3', '1', '2', '5', '3', '1'],
        ['2', '1', '5', '3', '2', '4', '1', '3', '5', '4'],
        ['3', '4', '3', '2', '1', '5', '4', '2', '1', '5'],
        ['5', '2', '1', '3', '4', '1', '5', '4', '2', '3'],
        ['1', '3', '4', '2', '5', '4', '1', '2', '3', '5'],
        ['4', '2', '5', '1', '3', '5', '3', '1', '4', '2'],
        ['2', '3', '4', '5', '1', '2', '4', '3', '5', '1'],
        ['3', '4', '2', '1', '5', '3', '2', '5', '1', '4']], dtype='<U11')
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
    test_ground()

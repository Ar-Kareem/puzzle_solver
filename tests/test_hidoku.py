import numpy as np
from puzzle_solver import hidoku_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    board = np.array([
        ['9', ' ', '1'],
        [' ', '4', ' '],
        ['6', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['9', '8', '1'],
        ['7', '4', '2'],
        ['6', '5', '3']
    ])
    ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    board = np.array([
        ['  ', '  ', '24', '  ', '  ', '  ', '  '],
        ['  ', '25', '  ', '  ', '22', '39', '40'],
        ['  ', '27', '  ', '  ', '  ', '20', '  '],
        ['  ', '03', '  ', '01', '  ', '  ', '  '],
        ['  ', '05', '06', '17', '16', '  ', '  '],
        ['  ', '08', '  ', '49', '  ', '46', '  '],
        ['09', '  ', '  ', '  ', '  ', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(np.array([[solution[get_pos(x=x, y=y)] for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str))
    ground = np.array([
        ['31', '32', '24', '23', '36', '37', '38'],
        ['30', '25', '33', '35', '22', '39', '40'],
        ['29', '27', '26', '34', '21', '20', '41'],
        ['28', '3', '2', '1', '18', '19', '42'],
        ['4', '5', '6', '17', '16', '15', '43'],
        ['10', '8', '7', '49', '14', '46', '44'],
        ['9', '11', '12', '13', '48', '47', '45']
    ])
    ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()

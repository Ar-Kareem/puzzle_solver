import numpy as np
from puzzle_solver import vectors_solver as solver
from puzzle_solver.core.utils import get_pos


def test_toy():
    board = np.array([
        ['3', ' ', ' ', '1'],
        [' ', '1', ' ', ' '],
        ['2', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=c, y=r), ('', ))[0] for c in range(board.shape[1])] for r in range(board.shape[0])])))
    ground = np.array([
        ['Pos(x=0, y=0):0', 'Pos(x=0, y=0):0', 'Pos(x=0, y=0):0', 'Pos(x=3, y=0):1'],
        ['Pos(x=0, y=0):0', 'Pos(x=1, y=1):0', 'Pos(x=1, y=1):0', 'Pos(x=3, y=0):1'],
        ['Pos(x=0, y=2):0', 'Pos(x=0, y=2):0', 'Pos(x=0, y=2):0', '']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos][0] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    board = np.array([
        ['  ', '  ', '  ', '  ', '  ', '5 ', '  ', '  ', '  ', '  ', '4 ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '12', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '4 ', '  ', '  ', '5 ', '  ', '  ', '  '],
        ['  ', '  ', '12', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5 '],
        ['4 ', '  ', '  ', '9 ', '  ', '7 ', '  ', '  ', '  ', '  ', '  ', '2 ', '  ', '  ', '  '],
        ['  ', '  ', '2 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '15', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  ', '4 ', '  ', '  ', '10'],
        ['  ', '  ', '  ', '  ', '4 ', '  ', '  ', '  ', '  ', '  ', '5 ', '  ', '  ', '4 ', '  '],
        ['  ', '  ', '1 ', '  ', '  ', '4 ', '  ', '  ', '8 ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '3 ', '  ', '  ', '1 ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '13', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '1 ', '  ', '  ', '  ', '  ', '3 ', '  ', '  ', '6 ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  ', '2 ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '14', '  ', '  ', '5 ', '  ', '  ', '  ', '  ', '  '],
        ['14', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print("ground = np." + repr(np.array([[solution.get(get_pos(x=c, y=r), ('', ))[0] for c in range(board.shape[1])] for r in range(board.shape[0])])))
    ground = np.array([['Pos(x=0, y=4):11', 'Pos(x=1, y=10):103', 'Pos(x=2, y=3):20', 'Pos(x=3, y=1):15', 'Pos(x=5, y=0):0', 'Pos(x=5, y=0):0', 'Pos(x=5, y=0):0', 'Pos(x=5, y=0):0', 'Pos(x=5, y=0):0', 'Pos(x=5, y=0):0', 'Pos(x=10, y=0):0', 'Pos(x=10, y=0):0', 'Pos(x=10, y=0):0', 'Pos(x=10, y=0):0', 'Pos(x=10, y=0):0'],
        ['Pos(x=0, y=4):11', 'Pos(x=1, y=10):103', 'Pos(x=2, y=3):20', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=3, y=1):15', 'Pos(x=14, y=3):7'],
        ['Pos(x=0, y=4):11', 'Pos(x=1, y=10):103', 'Pos(x=2, y=3):20', 'Pos(x=3, y=1):15', 'Pos(x=8, y=2):2', 'Pos(x=8, y=2):2', 'Pos(x=8, y=2):2', 'Pos(x=8, y=2):2', 'Pos(x=8, y=2):2', 'Pos(x=11, y=2):2', 'Pos(x=11, y=2):2', 'Pos(x=11, y=2):2', 'Pos(x=11, y=2):2', 'Pos(x=11, y=2):2', 'Pos(x=14, y=3):7'],
        ['Pos(x=0, y=4):11', 'Pos(x=1, y=10):103', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=2, y=3):20', 'Pos(x=11, y=2):2', 'Pos(x=14, y=3):7', 'Pos(x=14, y=3):7', 'Pos(x=14, y=3):7'],
        ['Pos(x=0, y=4):11', 'Pos(x=1, y=10):103', 'Pos(x=2, y=3):20', 'Pos(x=3, y=4):3', 'Pos(x=3, y=4):3', 'Pos(x=5, y=4):1', 'Pos(x=5, y=4):1', 'Pos(x=5, y=4):1', 'Pos(x=5, y=4):1', 'Pos(x=5, y=4):1', 'Pos(x=5, y=4):1', 'Pos(x=11, y=4):0', 'Pos(x=11, y=4):0', 'Pos(x=11, y=4):0', 'Pos(x=14, y=3):7'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=2, y=5):5', 'Pos(x=3, y=4):3', 'Pos(x=4, y=7):19', 'Pos(x=5, y=4):1', 'Pos(x=6, y=13):14', 'Pos(x=12, y=5):13', 'Pos(x=12, y=5):13', 'Pos(x=12, y=5):13', 'Pos(x=12, y=5):13', 'Pos(x=12, y=5):13', 'Pos(x=12, y=5):13', 'Pos(x=12, y=5):13', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=2, y=5):5', 'Pos(x=3, y=4):3', 'Pos(x=4, y=7):19', 'Pos(x=5, y=4):1', 'Pos(x=6, y=13):14', 'Pos(x=9, y=6):1', 'Pos(x=9, y=6):1', 'Pos(x=9, y=6):1', 'Pos(x=10, y=7):17', 'Pos(x=11, y=6):5', 'Pos(x=12, y=5):13', 'Pos(x=14, y=6):2', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=2, y=5):5', 'Pos(x=3, y=4):3', 'Pos(x=4, y=7):19', 'Pos(x=4, y=7):19', 'Pos(x=6, y=13):14', 'Pos(x=10, y=7):17', 'Pos(x=10, y=7):17', 'Pos(x=10, y=7):17', 'Pos(x=10, y=7):17', 'Pos(x=11, y=6):5', 'Pos(x=12, y=5):13', 'Pos(x=13, y=7):5', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=2, y=8):2', 'Pos(x=3, y=4):3', 'Pos(x=4, y=7):19', 'Pos(x=5, y=8):8', 'Pos(x=6, y=13):14', 'Pos(x=8, y=8):16', 'Pos(x=8, y=8):16', 'Pos(x=8, y=8):16', 'Pos(x=10, y=7):17', 'Pos(x=11, y=6):5', 'Pos(x=12, y=5):13', 'Pos(x=13, y=7):5', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=2, y=8):2', 'Pos(x=3, y=4):3', 'Pos(x=4, y=9):8', 'Pos(x=5, y=8):8', 'Pos(x=6, y=13):14', 'Pos(x=7, y=9):2', 'Pos(x=8, y=8):16', 'Pos(x=9, y=13):25', 'Pos(x=10, y=11):29', 'Pos(x=11, y=6):5', 'Pos(x=12, y=5):13', 'Pos(x=13, y=7):5', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=1, y=10):103', 'Pos(x=3, y=4):3', 'Pos(x=4, y=9):8', 'Pos(x=5, y=8):8', 'Pos(x=6, y=13):14', 'Pos(x=7, y=9):2', 'Pos(x=8, y=8):16', 'Pos(x=9, y=13):25', 'Pos(x=10, y=11):29', 'Pos(x=11, y=6):5', 'Pos(x=12, y=5):13', 'Pos(x=13, y=7):5', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=2, y=11):2', 'Pos(x=3, y=4):3', 'Pos(x=4, y=9):8', 'Pos(x=5, y=8):8', 'Pos(x=6, y=13):14', 'Pos(x=7, y=11):8', 'Pos(x=8, y=8):16', 'Pos(x=9, y=13):25', 'Pos(x=10, y=11):29', 'Pos(x=10, y=11):29', 'Pos(x=12, y=5):13', 'Pos(x=13, y=7):5', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=1, y=10):103', 'Pos(x=2, y=11):2', 'Pos(x=3, y=4):3', 'Pos(x=4, y=9):8', 'Pos(x=5, y=8):8', 'Pos(x=6, y=13):14', 'Pos(x=7, y=11):8', 'Pos(x=8, y=8):16', 'Pos(x=9, y=13):25', 'Pos(x=10, y=11):29', 'Pos(x=11, y=12):4', 'Pos(x=12, y=5):13', 'Pos(x=13, y=12):3', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=6, y=13):14', 'Pos(x=6, y=13):14', 'Pos(x=6, y=13):14', 'Pos(x=6, y=13):14', 'Pos(x=6, y=13):14', 'Pos(x=6, y=13):14', 'Pos(x=7, y=11):8', 'Pos(x=8, y=8):16', 'Pos(x=9, y=13):25', 'Pos(x=10, y=11):29', 'Pos(x=11, y=12):4', 'Pos(x=12, y=5):13', 'Pos(x=13, y=12):3', 'Pos(x=14, y=6):2'],
        ['Pos(x=0, y=14):9', 'Pos(x=0, y=14):9', 'Pos(x=0, y=14):9', 'Pos(x=0, y=14):9', 'Pos(x=0, y=14):9', 'Pos(x=0, y=14):9', 'Pos(x=6, y=13):14', 'Pos(x=7, y=11):8', 'Pos(x=8, y=8):16', 'Pos(x=9, y=13):25', 'Pos(x=10, y=11):29', 'Pos(x=11, y=12):4', 'Pos(x=12, y=5):13', 'Pos(x=13, y=12):3', 'Pos(x=14, y=6):2']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos][0] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground2():
    board = np.array([
        ['  ', '  ', '  ', '  ', '  ', '  ', '11', '  ', '  ', '  ', '  ', '  ', '  ', '1 ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '6 ', '  ', '  '],
        ['5 ', '  ', '  ', '1 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5 ', '  ', '1 ', '  '],
        ['  ', '  ', '5 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '11'],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5 ', '  ', '  ', '9 ', '  '],
        ['  ', '  ', '2 ', '  ', '  ', '13', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['1 ', '  ', '  ', '  ', '  ', '  ', '  ', '12', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  ', '  ', '  ', '  '],
        ['2 ', '  ', '  ', '5 ', '  ', '5 ', '  ', '  ', '  ', '2 ', '  ', '6 ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  ', '6 ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '2 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5 ', '  ', '  ', '  ', '  '],
        ['3 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '1 ', '  ', '  ', '  ', '  ', '6 '],
        ['  ', '15', '  ', '4 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '3 ', '  ', '  ', '2 ', '  ', '  ', '  ', '  ', '1 '],
        ['  ', '  ', '1 ', '  ', '15', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '13', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment


if __name__ == '__main__':
    test_toy()
    test_ground()
    test_ground2()

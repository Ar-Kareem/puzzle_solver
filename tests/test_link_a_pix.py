import numpy as np
from puzzle_solver import link_a_pix_solver as solver
from puzzle_solver.core.utils import get_pos, shapes_between, Pos


def debug_shapes_between():
    r = shapes_between(Pos(0, 1), Pos(2, 1), 7)
    print(r)
    print(len(r))
    r = shapes_between(Pos(0, 1), Pos(2, 1), 3)
    print(r)
    print(len(r))
    r = shapes_between(Pos(0, 1), Pos(2, 1), 4)
    print(r)
    print(len(r))
    r = shapes_between(Pos(2, 0), Pos(1, 1), 2)
    print(r)
    print(len(r))


def test_toy():
    board = np.array([
        ['1', ' ', '3'],
        [' ', '3', '1'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ('', ''))[0] for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['0', '2', '2'],
        ['', '2', '1']])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos][0]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos][0]} != {ground_assignment[pos]}'


def test_easy():
    # https://en.grandgames.net/filippinskie/id474664
    board = np.array([
        [' ', ' ', ' ', ' ', '5', '4', ' '],
        [' ', ' ', '1', ' ', '1', ' ', ' '],
        [' ', '2', '5', ' ', '4', ' ', ' '],
        ['1', '2', '1', '3', '1', '1', '1'],
        [' ', '1', '3', ' ', '1', '1', ' '],
        [' ', 'R_4', 'G_4', ' ', ' ', '6', ' '],
        [' ', ' ', ' ', '6', 'G_4', ' ', ' '],
        [' ', '1', 'R_4', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ('', ''))[0] for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['', '', '', '11', '11', '12', ''],
       ['', '', '0', '11', '1', '12', ''],
       ['', '13', '11', '11', '12', '12', ''],
       ['2', '13', '3', '14', '4', '5', '6'],
       ['', '7', '14', '14', '8', '9', ''],
       ['', '15', '16', '16', '16', '17', ''],
       ['', '15', '15', '17', '16', '17', ''],
       ['', '10', '15', '17', '17', '17', '']])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos][0]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos][0]} != {ground_assignment[pos]}'


def test_ground():
    # https://en.grandgames.net/filippinskie/id467770
    board = np.array([
        [ ''    , ''    , ''    , ''    , ''    , ''    , ''    , 'B_7' , ''    , ''    , ''    , ''    , ''    , 'B_7' , ''    , ''    , ''    , ''    , ''    , ''    , ''     ],
        [ ''    , ''    , ''    , ''    , ''    , ''    , 'B_1' , ''    , 'K_10', 'K_3' , 'K_1' , ''    , ''    , 'K_6' , 'B_1' , ''    , ''    , ''    , ''    , ''    , ''     ],
        [ ''    , ''    , ''    , ''    , ''    , 'B_1' , ''    , ''    , 'K_3' , ''    , ''    , ''    , 'K_5' , ''    , ''    , 'B_1' , ''    , ''    , ''    , ''    , ''     ],
        [ ''    , ''    , ''    , 'B_8' , ''    , ''    , ''    , 'B_3' , ''    , 'B_3' , 'K_6' , 'B_3' , ''    , 'B_3' , ''    , 'K_5' , ''    , 'B_8' , ''    , ''    , ''     ],
        [ ''    , ''    , 'B_1' , 'K_7' , ''    , ''    , 'B_2' , ''    , ''    , ''    , 'B_2' , ''    , ''    , ''    , 'B_3' , 'K_5' , ''    , 'K_6' , 'B_1' , ''    , ''     ],
        [ ''    , 'B_1' , ''    , ''    , ''    , ''    , 'B_2' , ''    , 'B_3' , ''    , 'B_2' , ''    , 'B_3' , ''    , ''    , ''    , ''    , ''    , 'K_7' , 'B_1' , ''     ],
        [ 'B_11', 'K_7' , ''    , 'K_6' , ''    , ''    , 'B_2' , ''    , ''    , ''    , 'B_2' , ''    , ''    , ''    , 'B_3' , ''    , ''    , ''    , ''    , 'K_7' , 'B_11' ],
        [ ''    , ''    , ''    , ''    , ''    , 'K_10', 'B_2' , ''    , 'B_3' , 'B_1' , 'B_2' , 'B_1' , 'B_3' , 'B_1' , 'K_5' , ''    , ''    , ''    , ''    , ''    , ''     ],
        [ ''    , 'K_8' , ''    , ''    , ''    , 'B_1' , ''    , 'K_7' , 'K_7' , ''    , ''    , 'K_3' , 'K_3' , 'K_1' , 'K_5' , 'B_1' , ''    , ''    , ''    , ''    , ''     ],
        [ ''    , ''    , ''    , 'K_6' , 'B_8' , 'K_5' , ''    , 'K_7' , ''    , ''    , 'K_3' , 'K_3' , ''    , ''    , ''    , 'K_7' , 'B_8' , 'K_6' , ''    , ''    , ''     ],
        [ ''    , ''    , 'K_8' , 'B_6' , ''    , ''    , ''    , ''    , ''    , 'B_5' , 'B_1' , 'B_5' , 'K_5' , ''    , 'K_4' , ''    , ''    , 'B_6' , ''    , 'K_8' , ''     ],
        [ ''    , ''    , ''    , ''    , ''    , 'K_5' , ''    , 'K_2' , 'K_2' , ''    , ''    , ''    , 'K_4' , ''    , ''    , 'K_1' , ''    , ''    , ''    , ''    , ''     ],
        [ ''    , ''    , ''    , ''    , 'K_7' , ''    , ''    , ''    , 'K_6' , ''    , 'B_3' , ''    , 'K_10', ''    , 'K_2' , ''    , ''    , ''    , 'K_8' , ''    , ''     ],
        [ ''    , 'K_6' , ''    , ''    , ''    , 'K_7' , 'K_7' , ''    , ''    , ''    , ''    , ''    , ''    , ''    , 'K_2' , 'K_4' , ''    , ''    , ''    , 'K_6' , ''     ],
        [ ''    , 'K_3' , ''    , ''    , ''    , ''    , ''    , 'K_6' , 'K_6' , 'K_1' , 'B_3' , 'K_2' , 'K_2' , ''    , ''    , ''    , 'K_7' , ''    , ''    , 'K_3' , ''     ],
        [ ''    , ''    , ''    , 'B_6' , ''    , ''    , ''    , ''    , ''    , 'B_1' , 'K_5' , 'B_1' , ''    , ''    , 'K_3' , ''    , 'K_4' , 'B_6' , ''    , ''    , ''     ],
        [ 'B_11', 'K_3' , ''    , 'K_2' , 'B_3' , 'K_6' , ''    , 'K_3' , 'K_1' , ''    , ''    , 'K_10', ''    , 'K_2' , ''    , 'K_3' , 'B_3' , 'K_2' , ''    , 'K_3' , 'B_11' ],
        [ ''    , 'B_1' , 'K_6' , 'K_2' , ''    , 'B_3' , 'K_3' , ''    , 'K_5' , ''    , 'K_3' , ''    , 'K_3' , 'K_2' , 'K_1' , 'B_3' , ''    , 'K_2' , 'K_6' , 'B_1' , ''     ],
        [ ''    , ''    , 'B_2' , 'B_2' , ''    , ''    , 'B_9' , ''    , ''    , ''    , ''    , ''    , ''    , ''    , 'B_9' , ''    , ''    , 'B_2' , 'B_2' , ''    , ''     ],
        [ ''    , ''    , ''    , ''    , ''    , ''    , 'R_4' , ''    , ''    , 'R_4' , 'Y_1' , 'R_4' , ''    , ''    , 'R_4' , ''    , ''    , ''    , ''    , ''    , ''     ],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print('ground = np.' + repr(np.array([[solution.get(get_pos(x=x, y=y), ('', ''))[0] for x in range(board.shape[1])] for y in range(board.shape[0])]).astype(str)))
    ground = np.array([['', '', '', '', '', '', '', '25', '25', '25', '25', '25', '25', '25', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '0', '26', '26', '28', '1', '38', '38', '38', '2', '', '', '', '', '', ''],
        ['', '', '', '', '', '3', '26', '26', '28', '28', '38', '38', '55', '55', '55', '4', '', '', '', '', ''],
        ['', '', '', '64', '64', '26', '26', '66', '66', '66', '38', '67', '67', '67', '55', '55', '65', '65', '', '', ''],
        ['', '', '5', '76', '64', '26', '101', '', '', '', '102', '', '', '', '70', '56', '65', '39', '6', '', ''],
        ['', '7', '76', '76', '64', '26', '101', '', '71', '', '102', '', '72', '', '70', '56', '65', '39', '81', '8', ''],
        ['109', '76', '76', '48', '64', '26', '105', '', '71', '', '106', '', '72', '', '70', '56', '65', '39', '81', '81', '110'],
        ['109', '76', '76', '48', '64', '26', '105', '', '71', '9', '106', '10', '72', '11', '56', '56', '65', '39', '81', '81', '110'],
        ['109', '118', '48', '48', '64', '12', '84', '84', '86', '86', '29', '29', '30', '13', '57', '14', '65', '39', '81', '81', '110'],
        ['109', '118', '48', '48', '64', '61', '84', '86', '86', '86', '29', '30', '30', '57', '57', '93', '65', '39', '142', '142', '110'],
        ['109', '118', '118', '155', '61', '61', '84', '86', '86', '157', '15', '157', '57', '57', '159', '93', '93', '156', '142', '142', '110'],
        ['109', '118', '118', '155', '61', '61', '84', '161', '161', '157', '157', '157', '159', '159', '159', '16', '93', '156', '142', '142', '110'],
        ['109', '118', '118', '155', '96', '', '84', '', '49', '49', '73', '27', '27', '', '162', '', '93', '156', '142', '142', '110'],
        ['109', '50', '50', '155', '96', '96', '84', '49', '49', '49', '73', '27', '27', '27', '162', '160', '93', '156', '51', '51', '110'],
        ['109', '31', '50', '155', '96', '96', '', '49', '54', '17', '73', '163', '163', '27', '', '160', '93', '156', '51', '32', '110'],
        ['109', '31', '50', '155', '96', '96', '54', '54', '54', '18', '63', '19', '27', '27', '34', '160', '160', '156', '51', '32', '110'],
        ['109', '31', '50', '164', '74', '54', '54', '35', '20', '63', '63', '27', '27', '165', '34', '34', '75', '166', '51', '32', '110'],
        ['', '21', '50', '164', '74', '74', '35', '35', '63', '63', '37', '37', '37', '165', '22', '75', '75', '166', '51', '23', ''],
        ['', '', '107', '107', '', '', '167', '167', '167', '167', '167', '167', '167', '167', '167', '', '', '108', '108', '', ''],
        ['', '', '', '', '', '', '168', '168', '168', '168', '24', '169', '169', '169', '169', '', '', '', '', '', '']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert str(solution[pos][0]) == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos][0]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    debug_shapes_between()
    test_toy()
    test_easy()
    test_ground()

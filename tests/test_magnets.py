import numpy as np

from puzzle_solver import magnets_solver as solver
from puzzle_solver.core.utils import get_pos


def test_dummy():
  # define board and parameters
  board = np.array([
    ['H', 'H', 'H', 'H', 'V'],
    ['V', 'V', 'H', 'H', 'V'],
    ['V', 'V', 'H', 'H', 'V'],
    ['H', 'H', 'H', 'H', 'V'],
    ['V', 'H', 'H', 'V', 'V'],
    ['V', 'H', 'H', 'V', 'V'],
  ])
  top_pos = np.array([3, 2, 2, 0, 2])
  top_neg = np.array([2, 2, 1, 2, 2])
  side_pos = np.array([2, 1, 1, 2, 2, 1])
  side_neg = np.array([1, 2, 1, 2, 2, 1])
  binst = solver.Board(board=board, top_pos=top_pos, top_neg=top_neg, side_pos=side_pos, side_neg=side_neg)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    [' ', ' ', '+', '-', '+'],
    ['+', '-', ' ', ' ', '-'],
    ['-', '+', ' ', ' ', ' '],
    ['+', '-', '+', '-', ' '],
    ['-', '+', '-', ' ', '+'],
    ['+', ' ', ' ', ' ', '-'],
  ])
  ground_assignment = {get_pos(x=x, y=y): ground[y][x].replace(' ', 'x') for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos][1] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos][1]} != {ground_assignment[pos]}'


def test_ground():
  # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html#10x9:..3533.3.4,5...5.31.,.234.34344,4.4.54.2.,LRLRTTTTLRLRLRBBBBTTLRLRLRLRBBTTTLRLRLRTBBBTTTTLRBTLRBBBBTTTBTTTTLRBBBTBBBBTLRLRBLRLRBLRLR
  board = np.array([
    ['H', 'H', 'H', 'H', 'V', 'V', 'V', 'V', 'H', 'H'],
    ['H', 'H', 'H', 'H', 'V', 'V', 'V', 'V', 'V', 'V'],
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'V', 'V'],
    ['V', 'V', 'V', 'H', 'H', 'H', 'H', 'H', 'H', 'V'],
    ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'H', 'H', 'V'],
    ['V', 'H', 'H', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
    ['V', 'V', 'V', 'V', 'V', 'H', 'H', 'V', 'V', 'V'],
    ['V', 'V', 'V', 'V', 'V', 'V', 'H', 'H', 'H', 'H'],
    ['V', 'H', 'H', 'H', 'H', 'V', 'H', 'H', 'H', 'H'],
  ])
  top_pos = np.array([-1, -1, 3, 5, 3, 3, -1, 3, -1, 4])
  top_neg = np.array([-1, 2, 3, 4, -1, 3, 4, 3, 4, 4])
  side_pos = np.array([5, -1, -1, -1, 5, -1, 3, 1, -1])
  side_neg = np.array([4, -1, 4, -1, 5, 4, -1, 2, -1])
  binst = solver.Board(board=board, top_pos=top_pos, top_neg=top_neg, side_pos=side_pos, side_neg=side_neg)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['-', '+', '-', '+', ' ', '+', '-', '+', '-', '+'],
    [' ', ' ', '+', '-', ' ', '-', '+', '-', '+', '-'],
    ['-', '+', '-', '+', ' ', ' ', '-', '+', '-', '+'],
    ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-'],
    ['-', '+', '-', '+', '-', '+', '-', '+', '-', '+'],
    [' ', '-', '+', '-', '+', '-', '+', ' ', '+', '-'],
    [' ', ' ', ' ', '+', '-', '+', '-', ' ', '-', '+'],
    ['-', ' ', ' ', '-', '+', ' ', ' ', ' ', ' ', ' '],
    ['+', ' ', ' ', '+', '-', ' ', '+', '-', '+', '-'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x].replace(' ', 'x') for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos][1] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos][1]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_dummy()
  test_ground()

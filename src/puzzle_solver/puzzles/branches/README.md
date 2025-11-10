# Branches (Puzzle Type #82)

This is a dedicated solver for Branches.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.youtube.com/watch?v=1IsYiSnhiZ0)

**Rules**

In Branches you must fill the board with straight horizontal and vertical lines (Branches) that stem from each number.

The number in itself tells you how many total tiles its Branches fill up. The tile with the number doesn’t count. For example, if a number says 4, it could be 1 up, 2 left and 3 down.

There can’t be blank tiles and Branches can’t overlap, nor run over the numbers. Moreover Branches must be in a single straight line and can’t make corners.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/branches_unsolved.png" alt="Branches unsolved" width="500">


```python
import numpy as np
from puzzle_solver import branches_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', ' ', '2'],
    ['5', ' ', '7', ' ', ' ', ' '],
    [' ', ' ', ' ', '3', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', '2'],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '7', ' ', ' ', '3', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5
  ┌───┬───┬───┬───┬───┬───┐
 0│ * │ * │ * │ *─┼───┤ 2 │
  ├─┴─┼─┼─┼─┴─┼───┼───┼───┤
 1│ 5 │ │ │ 7 ├───┼───┼─* │
  ├─┬─┼─┼─┼─┬─┼───┼───┼───┤
 2│ │ │ │ │ │ │ 3 ├─* │ * │
  ├─┼─┼─┼─┼─┼─┼─┬─┼───┼─┴─┤
 3│ │ │ │ │ │ │ │ │ * │ 2 │
  ├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┬─┤
 4│ │ │ │ │ * │ * │ │ │ * │
  ├─┼─┼─┴─┼───┼───┼─┴─┼───┤
 5│ * │ 7 ├───┼─* │ 3 ├─* │
  └───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/branches_solved.png" alt="Branches solved" width="500">

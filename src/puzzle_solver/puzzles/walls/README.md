# Walls (Puzzle Type #86)

This is a dedicated solver for Walls.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7wll.htm)

**Rules**

The task is to place a horizontal or a vertical line in every blank cell.

A number in a black cell indicates the total length of the segments connected to that square.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/walls_unsolved.png" alt="Walls unsolved" width="500">


```python
import numpy as np
from puzzle_solver import walls_solver as solver
board = np.array([
    [' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', '2', ' '],
    [' ', ' ', '1', ' ', ' ', '2', ' ', ' ', ' ', '2'],
    ['5', ' ', ' ', ' ', '4', ' ', ' ', '4', ' ', ' '],
    [' ', ' ', '3', ' ', ' ', '4', ' ', ' ', ' ', ' '],
    ['7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6', '6'],
    [' ', '2', ' ', ' ', '5', ' ', '6', ' ', ' ', ' '],
    [' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' '],
    ['4', ' ', '2', ' ', ' ', '4', ' ', '4', ' ', ' '],
    [' ', ' ', '4', ' ', ' ', ' ', ' ', ' ', ' ', '6'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───┬───┬───┬───┬─┬─┬─┬─┬─┬─┬───┬───┐
 0├───┼───┼───┤ 5 ├───┤ │ │ │ │ │ │ 2 ├───┤
  ├─┬─┼───┼───┼─┬─┼─┬─┼─┴─┼─┼─┼─┼─┼─┬─┼───┤
 1│ │ ├───┤ 1 │ │ │ │ │ 2 │ │ │ │ │ │ │ 2 │
  ├─┴─┼───┼───┼─┴─┼─┴─┼─┬─┼─┼─┼─┴─┼─┴─┼─┬─┤
 2│ 5 ├───┼───┼───┤ 4 │ │ │ │ │ 4 ├───┤ │ │
  ├─┬─┼───┼───┼───┼───┼─┴─┼─┼─┼─┬─┼─┬─┼─┼─┤
 3│ │ ├───┤ 3 ├───┼───┤ 4 │ │ │ │ │ │ │ │ │
  ├─┴─┼───┼───┼───┼─┬─┼─┬─┼─┼─┼─┴─┼─┴─┼─┴─┤
 4│ 7 ├───┼───┼───┤ │ │ │ │ │ ├───┤ 6 │ 6 │
  ├─┬─┼───┼───┼───┼─┴─┼─┴─┼─┴─┼─┬─┼─┬─┼─┬─┤
 5│ │ │ 2 ├───┼───┤ 5 ├───┤ 6 │ │ │ │ │ │ │
  ├─┼─┼───┼───┼─┬─┼─┬─┼─┬─┼───┼─┼─┼─┼─┼─┼─┤
 6│ │ ├───┤ 1 │ │ │ │ │ │ │ 1 │ │ │ │ │ │ │
  ├─┼─┼───┼───┼─┴─┼─┴─┼─┼─┼─┬─┼─┼─┼─┼─┼─┼─┤
 7│ │ ├───┼───┼───┤ 5 │ │ │ │ │ │ │ │ │ │ │
  ├─┴─┼───┼───┼───┼─┬─┼─┴─┼─┴─┼─┴─┼─┼─┼─┼─┤
 8│ 4 ├───┤ 2 ├───┤ │ │ 4 ├───┤ 4 │ │ │ │ │
  ├───┼───┼───┼───┼─┴─┼─┬─┼─┬─┼───┼─┴─┼─┴─┤
 9├───┼───┤ 4 ├───┼───┤ │ │ │ ├───┼───┤ 6 │
  └───┴───┴───┴───┴───┴─│─┴─│─┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/walls_solved.png" alt="Walls solved" width="500">

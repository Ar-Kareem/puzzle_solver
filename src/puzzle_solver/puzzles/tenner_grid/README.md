# Tenner Grid (Puzzle Type #91)

This is a dedicated solver for Tenner Grid. Also known as "From 1 to 10", "Zehnergitter", "Grid Ten".

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7tng.htm)

**Rules**

Tenner Grid consists of a rectangular grid of width ten cells. The task is to fill in the grid so that every row contains the digits 0 through 9.

In columns the numbers may be repeated. The bottom numbers give the sum of the numbers in column. The digits in contiguous cells (even diagonally contiguous cells) must be different.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/tenner_grid_unsolved.png" alt="Tenner Grid unsolved" width="500">


```python
import numpy as np
from puzzle_solver import tenner_grid_solver as solver
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
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│ 7 │ 3 │ 2 │ 4 │ 6 │ 8 │ 0 │ 9 │ 1 │ 5 │
  │   │   │   │   │   │   │   │   │   │   │
 1│ 4 │ 8 │ 0 │ 9 │ 1 │ 5 │ 6 │ 2 │ 7 │ 3 │
  │   │   │   │   │   │   │   │   │   │   │
 2│ 7 │ 5 │ 3 │ 2 │ 4 │ 9 │ 8 │ 1 │ 6 │ 0 │
  │   │   │   │   │   │   │   │   │   │   │
 3│ 0 │ 2 │ 4 │ 8 │ 1 │ 6 │ 3 │ 9 │ 5 │ 7 │
  │   │   │   │   │   │   │   │   │   │   │
 4│ 8 │ 1 │ 0 │ 3 │ 9 │ 7 │ 5 │ 6 │ 4 │ 2 │
  │   │   │   │   │   │   │   │   │   │   │
 5│ 7 │ 3 │ 4 │ 8 │ 5 │ 6 │ 0 │ 2 │ 9 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│33 │22 │13 │34 │26 │41 │22 │29 │32 │18 │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.24 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/tenner_grid_solved.png" alt="Tenner Grid solved" width="500">

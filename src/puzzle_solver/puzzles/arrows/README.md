# Arrows (Puzzle Type #89)

This is a dedicated solver for Arrows.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/help.htm)

**Rules**

Arrows is played on a rectangular grid filled with numbers. The task is to place arrows outside the grid.

Every arrow can go horizontally, vertically or diagonally and points to at least one cell in the grid.

The numbers indicate the total number of arrows that point to them.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/arrows_unsolved.png" alt="Arrows unsolved" width="500">


```python
import numpy as np
from puzzle_solver import arrows_solver as solver
board = np.array([
    [3, 1, 4, 1, 3, 2, 3, 2],
    [5, 2, 4, 4, 2, 3, 4, 4],
    [5, 5, 4, 3, 6, 2, 5, 6],
    [5, 2, 4, 2, 3, 4, 3, 3],
    [3, 1, 2, 2, 2, 2, 3, 2],
    [3, 2, 3, 2, 5, 1, 4, 4],
    [5, 1, 3, 3, 2, 4, 2, 3],
    [2, 2, 2, 0, 3, 0, 3, 1],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│   │ ↓ │ ↘ │ ↓ │ ↙ │ ↘ │ ↘ │ ↘ │ ↓ │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ ↘ │ 3 │ 1 │ 4 │ 1 │ 3 │ 2 │ 3 │ 2 │ ↙ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│ ↗ │ 5 │ 2 │ 4 │ 4 │ 2 │ 3 │ 4 │ 4 │ ← │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│ → │ 5 │ 5 │ 4 │ 3 │ 6 │ 2 │ 5 │ 6 │ ← │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│ → │ 5 │ 2 │ 4 │ 2 │ 3 │ 4 │ 3 │ 3 │ ↖ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│ ↗ │ 3 │ 1 │ 2 │ 2 │ 2 │ 2 │ 3 │ 2 │ ↖ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│ ↗ │ 3 │ 2 │ 3 │ 2 │ 5 │ 1 │ 4 │ 4 │ ← │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│ → │ 5 │ 1 │ 3 │ 3 │ 2 │ 4 │ 2 │ 3 │ ↖ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│ ↗ │ 2 │ 2 │ 2 │ 0 │ 3 │ 0 │ 3 │ 1 │ ↖ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │ ↑ │ ↗ │ ↖ │ ↗ │ ↑ │ ↖ │ ↑ │ ↖ │   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/arrows_solved.png" alt="Arrows solved" width="500">

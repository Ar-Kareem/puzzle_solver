# Kropki (Puzzle Type #75)

* [**Play online**](https://krazydad.com/play/kropki)

Each digit from 1-6 occurs once within each row and column. White circles separate consecutive digits. Black circles separate digits with a 2:1 ratio.

All number pairs that *can* be clued will receive clues – numbers that do *not* have circle clues are neither consecutive nor in a 2:1 ratio.

There is only one solution.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/kropki_unsolved.png" alt="Kropki unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import kropki_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '2', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '4', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
])
horiz_board = np.array([
    [' ', ' ', ' ', ' ', 'W'],
    [' ', ' ', ' ', ' ', ' '],
    ['B', ' ', 'B', ' ', ' '],
    ['B', 'W', ' ', 'W', ' '],
    ['B', 'W', ' ', ' ', 'W'],
    [' ', 'W', ' ', 'W', 'W'],
])
vert_board = np.array([
    [' ', ' ', ' ', ' ', ' ', 'W'],
    ['W', ' ', ' ', 'W', ' ', ' '],
    [' ', 'W', ' ', ' ', ' ', ' '],
    [' ', 'W', 'W', ' ', 'W', ' '],
    ['W', ' ', ' ', 'W', ' ', ' '],
])
binst = solver.Board(board=board, horiz_board=horiz_board, vert_board=vert_board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5
  ┌───┬───┬───┬───┬───┬───┐
 0│ 5 │ 1 │ 4 │ 6 │ 2 │ 3 │
  ├───┼───┼───┼───┼───┼───┤
 1│ 3 │ 5 │ 1 │ 4 │ 6 │ 2 │
  ├───┼───┼───┼───┼───┼───┤
 2│ 4 │ 2 │ 6 │ 3 │ 1 │ 5 │
  ├───┼───┼───┼───┼───┼───┤
 3│ 6 │ 3 │ 2 │ 5 │ 4 │ 1 │
  ├───┼───┼───┼───┼───┼───┤
 4│ 2 │ 4 │ 3 │ 1 │ 5 │ 6 │
  ├───┼───┼───┼───┼───┼───┤
 5│ 1 │ 6 │ 5 │ 2 │ 3 │ 4 │
  └───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/kropki_solved.png" alt="Kropki solved" width="500">

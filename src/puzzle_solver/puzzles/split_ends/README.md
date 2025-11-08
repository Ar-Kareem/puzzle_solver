# Split Ends (Puzzle Type #60)

This is a dedicated solver for Split Ends.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://krazydad.com/play/splitends/)

Each row and column contains four unique Y shapes (four different orientations) and two Os. Ys should not form straight lines by touching other Ys.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/split_ends_unsolved.png" alt="Split Ends unsolved" width="500">

Code to utilize this package and solve the puzzle:

Note: the 4 letters ("U", "L", "D", "R") represent the 4 shapes, each letter corresponds to the direction of the cardinal line, so the "Y" shape for example is "D" because the cardinal line is down.

```python
import numpy as np
from puzzle_solver import split_ends_solver as solver
board = np.array([
    ['O', ' ', 'O', 'L', ' ', 'U'],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'R', ' ', ' ', 'O', ' '],
    [' ', 'O', ' ', ' ', 'L', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    ['U', ' ', 'L', 'D', ' ', 'R'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5
  ┌───┬───┬───┬───┬───┬───┐
 0│ O │ D │ O │ L │ R │ U │
  ├───┼───┼───┼───┼───┼───┤
 1│ O │ L │ D │ R │ U │ O │
  ├───┼───┼───┼───┼───┼───┤
 2│ D │ R │ O │ U │ O │ L │
  ├───┼───┼───┼───┼───┼───┤
 3│ R │ O │ U │ O │ L │ D │
  ├───┼───┼───┼───┼───┼───┤
 4│ L │ U │ R │ O │ D │ O │
  ├───┼───┼───┼───┼───┼───┤
 5│ U │ O │ L │ D │ O │ R │
  └───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/split_ends_solved.png" alt="Split Ends solved" width="500">

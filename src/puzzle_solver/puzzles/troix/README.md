# Troix (Puzzle Type #63)

* [**Solver Code**](https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/troix)

The board should be filled with `O`s, `X`s, and `I`s. Horizontally and vertically.

There should never be a continuous run of the same symbol longer than 2. 

There are an equal number of each symbol in each row and column.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/troix_unsolved.png" alt="Troix unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import troix_solver as solver
board = np.array([
    ['O', 'I', 'O', ' ', 'I', ' ', 'X', 'O', 'I'],
    [' ', 'O', ' ', 'I', ' ', 'X', ' ', 'X', ' '],
    ['I', ' ', 'X', ' ', 'I', ' ', 'I', ' ', 'X'],
    ['X', 'I', ' ', ' ', ' ', ' ', ' ', 'X', 'X'],
    [' ', ' ', 'O', 'I', ' ', 'X', 'X', ' ', ' '],
    ['I', 'O', ' ', ' ', ' ', ' ', ' ', 'I', 'I'],
    ['O', ' ', 'O', ' ', 'O', ' ', 'I', ' ', 'X'],
    [' ', 'X', ' ', 'I', ' ', 'O', ' ', 'O', ' '],
    ['X', 'O', 'X', ' ', 'O', ' ', 'O', 'I', 'I'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7   8
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│ O │ I │ O │ X │ I │ X │ X │ O │ I │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ I │ O │ I │ I │ X │ X │ O │ X │ O │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│ I │ X │ X │ O │ I │ O │ I │ O │ X │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│ X │ I │ I │ O │ O │ I │ O │ X │ X │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│ O │ X │ O │ I │ I │ X │ X │ I │ O │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│ I │ O │ X │ O │ X │ O │ X │ I │ I │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│ O │ I │ O │ X │ O │ I │ I │ X │ X │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│ X │ X │ I │ I │ X │ O │ I │ O │ O │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│ X │ O │ X │ X │ O │ I │ O │ I │ I │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/troix_solved.png" alt="Troix solved" width="500">

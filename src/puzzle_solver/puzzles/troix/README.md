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

# Dumplings (Puzzle Type #63)

* [**Solver Code**](https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/dumplings)

The finished puzzle should be filled with soup dumplings. There are an equal number of each flavor in each row and column. 

This is very similar to Troix, except the grid is only 6x6 and the rule disallowing 3 consecutive symbols in a row no longer applies here (since each row and column only has 2 of each symbol)

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/dumplings_unsolved.png" alt="Dumplings unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import dumplings_solver as solver
board = np.array([
    ['W', ' ', 'G', ' ', ' ', 'G'],
    ['W', 'W', ' ', ' ', 'O', ' '],
    [' ', ' ', ' ', 'G', 'O', 'G'],
    [' ', ' ', ' ', 'O', ' ', 'O'],
    ['G', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5
  ┌───┬───┬───┬───┬───┬───┐
 0│ W │ O │ G │ O │ W │ G │
  ├───┼───┼───┼───┼───┼───┤
 1│ W │ W │ G │ G │ O │ O │
  ├───┼───┼───┼───┼───┼───┤
 2│ O │ W │ W │ G │ O │ G │
  ├───┼───┼───┼───┼───┼───┤
 3│ G │ G │ W │ O │ W │ O │
  ├───┼───┼───┼───┼───┼───┤
 4│ G │ O │ O │ W │ G │ W │
  ├───┼───┼───┼───┼───┼───┤
 5│ O │ G │ O │ W │ G │ W │
  └───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/dumplings_solved.png" alt="Dumplings solved" width="500">

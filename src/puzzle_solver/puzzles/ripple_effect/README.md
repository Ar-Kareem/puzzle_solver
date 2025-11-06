# Ripple Effect (Puzzle Type #76)

* [**Play online**](https://krazydad.com/play/ripple)

Heavy lines indicate areas, called cages, from 1 to 9 cells in size. 

Fill each cage with unique digits, counting up from 1. So for example a 2-cell cage contains the numbers 1 and 2; and a 5-cell cage contains all the numbers from 1 to 5. 

If two identical numbers appear in the same row or column, at least that many cells must separate them. For example, if two 3s appear in the same column, they must be separated by at least three other cells that do not contain 3.

This puzzle is a variant of Suguru in which the clues create curious cascading effects.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/ripple_effect_unsolved.png" alt="Ripple Effect unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import ripple_effect_solver as solver
id_board = np.array([
    ['00', '01', '02', '02', '03', '03', '04'],
    ['00', '05', '05', '02', '03', '06', '06'],
    ['07', '07', '05', '08', '03', '03', '06'],
    ['09', '07', '07', '07', '03', '10', '10'],
    ['11', '11', '12', '12', '13', '13', '10'],
    ['14', '11', '14', '12', '13', '15', '15'],
    ['14', '14', '14', '16', '13', '13', '15']
])
board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', '5', ' '],
    [' ', ' ', '4', ' ', '6', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '1'],
    [' ', ' ', '1', ' ', ' ', ' ', ' '],
    [' ', '4', ' ', ' ', ' ', ' ', ' '],
])
binst = solver.Board(board=board, id_board=id_board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┬───┐
 0│ 2 │ 1 │ 3 │ 1 │ 4 │ 2 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┤
 1│ 1 │ 3 │ 1 │ 2 │ 1 │ 3 │ 2 │
  ├───┼───┼───┼───┼───┼───┼───┤
 2│ 3 │ 1 │ 2 │ 1 │ 3 │ 5 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┤
 3│ 1 │ 2 │ 4 │ 5 │ 6 │ 2 │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┤
 4│ 2 │ 1 │ 3 │ 1 │ 5 │ 4 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┤
 5│ 5 │ 3 │ 1 │ 2 │ 1 │ 3 │ 2 │
  ├───┼───┼───┼───┼───┼───┼───┤
 6│ 3 │ 4 │ 2 │ 1 │ 3 │ 2 │ 1 │
  └───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/ripple_effect_solved.png" alt="Ripple Effect solved" width="500">

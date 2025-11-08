# Hidoku (Puzzle Type #64)

This is a dedicated solver for Hidoku.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://puzzlemadness.co.uk/hidoku/medium)

**Rules**

The puzzle starts with a partially filled grid of numbers, and your aim is to fill the grid with unique integers such that you can draw a single continuous line from the number 1 to the number maximum number.

You can move one cell in any direction, including diagonally. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/hidoku_unsolved.png" alt="Hidoku unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import hidoku_solver as solver
board = np.array([
    ['  ', '  ', '24', '  ', '  ', '  ', '  '],
    ['  ', '25', '  ', '  ', '22', '39', '40'],
    ['  ', '27', '  ', '  ', '  ', '20', '  '],
    ['  ', '03', '  ', '01', '  ', '  ', '  '],
    ['  ', '05', '06', '17', '16', '  ', '  '],
    ['  ', '08', '  ', '49', '  ', '46', '  '],
    ['09', '  ', '  ', '  ', '  ', '  ', '  '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┬───┐
 0│31 │32 │24 │23 │36 │37 │38 │
  ├───┼───┼───┼───┼───┼───┼───┤
 1│30 │25 │33 │35 │22 │39 │40 │
  ├───┼───┼───┼───┼───┼───┼───┤
 2│29 │27 │26 │34 │21 │20 │41 │
  ├───┼───┼───┼───┼───┼───┼───┤
 3│28 │ 3 │ 2 │ 1 │18 │19 │42 │
  ├───┼───┼───┼───┼───┼───┼───┤
 4│ 4 │ 5 │ 6 │17 │16 │15 │43 │
  ├───┼───┼───┼───┼───┼───┼───┤
 5│10 │ 8 │ 7 │49 │14 │46 │44 │
  ├───┼───┼───┼───┼───┼───┼───┤
 6│ 9 │11 │12 │13 │48 │47 │45 │
  └───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/hidoku_solved.png" alt="Hidoku solved" width="500">

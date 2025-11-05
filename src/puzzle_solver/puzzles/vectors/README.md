# Vectors (Puzzle Type #72)

* [**Play online**](https://vectors.puzzlebaron.com/init.php)

The puzzle grid consists of a series of numbered black squares. Your task is to draw arrows starting from each of these black squares in such a way so that the total number of white squares covered by arrows emanating from any black square equals exactly the number displayed. Arrows can go up, down, left or right, but can never cross another arrow. You must also fill every empty square on the grid with one arrow segment. Each puzzle has only one unique solution, and each can be solved using pure logical deduction.

   - Every numbered black square must have exactly that number of combined arrow lengths emanating from it in the final solution.
   - No two arrows can cross each other.
   - Every square on the grid must be filled with an arrow.
   - A number will turn green once it has arrows emanating from it with the correct combined length, but that does not necessarily mean those arrows are placed correctly.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/vectors_unsolved.png" alt="Vectors unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import vectors_solver as solver
board = np.array([
    ['  ', '  ', '  ', '  ', '  ', '  ', '11', '  ', '  ', '  ', '  ', '  ', '  ', '1 ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '6 ', '  ', '  '],
    ['5 ', '  ', '  ', '1 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5 ', '  ', '1 ', '  '],
    ['  ', '  ', '5 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '11'],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5 ', '  ', '  ', '9 ', '  '],
    ['  ', '  ', '2 ', '  ', '  ', '13', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['1 ', '  ', '  ', '  ', '  ', '  ', '  ', '12', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  ', '  ', '  ', '  '],
    ['2 ', '  ', '  ', '5 ', '  ', '5 ', '  ', '  ', '  ', '2 ', '  ', '6 ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  ', '6 ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '2 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5 ', '  ', '  ', '  ', '  '],
    ['3 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '1 ', '  ', '  ', '  ', '  ', '6 '],
    ['  ', '15', '  ', '4 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '3 ', '  ', '  ', '2 ', '  ', '  ', '  ', '  ', '1 '],
    ['  ', '  ', '1 ', '  ', '15', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '13', '  ', '  '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3   4
  ┌───┬───┬───┬───────────────────────────────────┬───┬───────┐
 0│   │   │   │            11                     │   │ 1     │
  │   │   │   ├───┬───┬───┐   ┌───────────────────┘   ├───┬───┤
 1│   │   │   │   │   │   │   │                     6 │   │   │
  │   │   │   │   │   │   │   ├───────────────────────┤   │   │
 2│ 5 │   │   │ 1 │   │   │   │                 5     │ 1 │   │
  │   │   │   └───┤   │   │   ├───────────────────────┴───┘   │
 3│   │   │ 5     │   │   │   │                            11 │
  │   │   │   ┌───┤   │   ├───┴───────────────────┬───────┐   │
 4│   │   │   │   │   │   │                 5     │     9 │   │
  │   │   ├───┤   │   │   └───────────────────────┴───┐   │   │
 5│   │   │ 2 │   │   │13                             │   │   │
  ├───┤   │   │   │   │   ┌───────────────────────────┤   ├───┤
 6│ 1 │   │   │   │   │   │    12                     │   │   │
  │   │   │   │   │   │   ├───┐   ┌───┬───┬───────────┤   │   │
 7│   │   │   │   │   │   │   │   │   │   │ 2         │   │   │
  ├───┤   ├───┘   │   ├───┤   │   │   │   └───┬───────┤   │   │
 8│ 2 │   │     5 │   │ 5 │   │   │   │ 2     │ 6     │   │   │
  │   │   ├───┬───┤   │   │   │   │   └───┬───┤   ┌───┤   │   │
 9│   │   │   │   │   │   │ 2 │   │ 6     │   │   │   │   │   │
  │   │   │   │   │   │   ├───┤   │   ┌───┘   │   │   │   │   │
10│   │   │ 2 │   │   │   │   │   │   │     5 │   │   │   │   │
  ├───┤   │   │   │   │   │   │   │   ├───┐   │   │   │   │   │
11│ 3 │   │   │   │   │   │   │   │   │ 1 │   │   │   │   │ 6 │
  │   │   └───┤   │   │   │   │   │   │   │   │   │   │   │   │
12│   │15     │ 4 │   │   │   │   │   │   │   │   │   │   │   │
  │   │   ┌───┤   │   │   │   ├───┴───┴───┤   │   │   ├───┴───┤
13│   │   │   │   │   │   │ 3 │         2 │   │   │   │     1 │
  │   │   │   ├───┘   └───┼───┴───────────┴───┴───┘   └───────┤
14│   │   │ 1 │    15     │                        13         │
  └───┴───┴───┴───────────┴───────────────────────────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/vectors_solved.png" alt="Vectors solved" width="500">

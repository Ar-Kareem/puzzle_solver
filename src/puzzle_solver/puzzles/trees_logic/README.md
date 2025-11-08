# Trees Logic (Puzzle Type #71)

This is a dedicated solver for Trees Logic.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.sporcle.com/games/Katie_Wandering/trees-logic-puzzle)

**Rules**

   - Each row, column, and colored shape each contains exactly one tree. Trees cannot touch, even diagonally.
   - Mark each tree with a "T", and everywhere where there cannot be a tree with a "-" (hyphen). You must completely fill in the grid to complete the puzzle.
   - This puzzle can be solved without guessing, and only has one possible solution.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/trees_logic_unsolved.png" alt="Trees Logic unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import trees_logic_solver as solver
board = np.array([
    ['01', '01', '02', '02', '02', '03', '03', '03'],
    ['04', '01', '01', '02', '08', '03', '08', '08'],
    ['04', '01', '01', '02', '08', '08', '08', '08'],
    ['04', '01', '01', '02', '02', '05', '05', '05'],
    ['04', '01', '01', '01', '02', '02', '05', '05'],
    ['04', '04', '01', '01', '02', '06', '06', '06'],
    ['04', '04', '04', '04', '07', '07', '07', '06'],
    ['04', '04', '07', '07', '07', '06', '06', '06'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7
  ┌───────┬───────────┬───────────┐
 0│       │           │    ▒▒▒    │
  ├───┐   └───┐   ┌───┤   ┌───────┤
 1│   │       │   │▒▒▒│   │       │
  │   │       │   │   └───┘       │
 2│   │▒▒▒    │   │               │
  │   │       │   └───┬───────────┤
 3│   │       │▒▒▒    │           │
  │   │       └───┐   └───┐       │
 4│   │           │       │    ▒▒▒│
  │   └───┐       │   ┌───┴───────┤
 5│       │       │   │▒▒▒        │
  │       └───────┼───┴───────┐   │
 6│▒▒▒            │           │   │
  │       ┌───────┘   ┌───────┘   │
 7│       │▒▒▒        │           │
  └───────┴───────────┴───────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/trees_logic_solved.png" alt="Trees Logic solved" width="500">

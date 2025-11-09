# Hidden Stars (Puzzle Type #81)

This is a dedicated solver for Hidden Stars.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.youtube.com/watch?v=RiqTy2Z5CHU)

**Rules**

You must identify where the stars are positioned on the grid knowing that an arrow is pointing to a star.

Each arrow must point to at least one star and every star has an arrow pointing to it.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/hidden_stars_unsolved.png" alt="Hidden Stars unsolved" width="500">


```python
import numpy as np
from puzzle_solver import hidden_stars_solver as solver
# Q = up-left, W = up, E = up-right, A = left, D = right, Z = down-left, X = down, C = down-right
board = np.array([
    [' ', 'C', 'A', ' ', 'X', ' ', 'X'],
    ['C', ' ', 'Z', 'C', ' ', 'Z', ' '],
    ['D', ' ', ' ', ' ', 'W', ' ', ' '],
    [' ', ' ', 'X', ' ', ' ', ' ', ' '],
    [' ', ' ', 'A', ' ', ' ', ' ', ' '],
    ['W', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'W', ' ', ' ', 'A', 'Q', ' '],
])
side = np.array([1, 2, 2, 1, 1, 3, 1])
top = np.array([1, 3, 2, 1, 2, 1, 1])
binst = solver.Board(board=board, side=side, top=top)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│ C │ A │   │ X │   │ X │
  ├───┼───┼───┼───┼───┼───┼───┤
 1│ C │   │ Z │ C │▒▒▒│ Z │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┤
 2│ D │▒▒▒│   │▒▒▒│ W │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
 3│   │   │ X │   │   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┤
 4│   │▒▒▒│ A │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
 5│ W │▒▒▒│▒▒▒│   │▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
 6│   │ W │▒▒▒│   │ A │ Q │   │
  └───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/hidden_stars_solved.png" alt="Hidden Stars solved" width="500">

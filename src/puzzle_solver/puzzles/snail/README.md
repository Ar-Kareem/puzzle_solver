# Snail (Puzzle Type #80)

This is a dedicated solver for Snail.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.somethinkodd.com/oddthinking/2018/06/15/the-snail-puzzle/)

**Rules**

The gameboard is a grid of squares, which are marked out as a spiral. Each cell can marked as “empty” with a dot, or marked as having a 1, 2, or 3 in it. Some are filled in as initial clues.

The rules are are:

   - Each number must appear exactly once in each row and column.
   - As you follow the spiralling path from the outside to the centre, the numbers must repeat the sequence 1-2-3, starting with a 1 and finishing with a 3.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/snail_unsolved.png" alt="Snail unsolved" width="500">


```python
import numpy as np
from puzzle_solver import snail_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '3', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    ['1', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', '1', ' ', ' ', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5
  ┌───┬───┬───┬───┬───┬───┐
 0│   │ 1 │ 2 │ 3 │   │   │
  ├───┼───┼───┼───┼───┼───┤
 1│   │ 3 │   │ 1 │ 2 │   │
  ├───┼───┼───┼───┼───┼───┤
 2│ 2 │   │   │   │ 3 │ 1 │
  ├───┼───┼───┼───┼───┼───┤
 3│   │   │ 3 │   │ 1 │ 2 │
  ├───┼───┼───┼───┼───┼───┤
 4│ 1 │   │   │ 2 │   │ 3 │
  ├───┼───┼───┼───┼───┼───┤
 5│ 3 │ 2 │ 1 │   │   │   │
  └───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/snail_solved.png" alt="Snail solved" width="500">

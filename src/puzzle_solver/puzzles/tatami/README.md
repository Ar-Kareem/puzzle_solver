# Tatami (Puzzle Type #83)

This is a dedicated solver for Tatami. Also known as Patchwork.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.crauswords.com/tatami.html)

**Rules**

A Tatami puzzle consists of a square grid which has been covered with rectangular tiles which are either 3, 4 or 5 cells in area. Any given puzzle will be fully covered using tiles of only one of these sizes. To solve such a puzzle, the solver must place numbers from 1 up to the numerical size of the tile into the puzzle cells so that the following three rules are met:-

   - The numbers within a tile must all be different.
   - Horizontally or Vertically adjacent puzzle cells must not contain the same number.
   - Each row and column of the puzzle must contain the same number of appearances of each number.

Some of the puzzle cells will have a number already inserted to get you started.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/tatami_unsolved.png" alt="Tatami unsolved" width="500">


```python
import numpy as np
from puzzle_solver import tatami_solver as solver
id_board = np.array([
    ['00', '01', '01', '01', '01', '01', '02', '03', '04', '05'],
    ['00', '06', '06', '06', '06', '06', '02', '03', '04', '05'],
    ['00', '07', '07', '07', '07', '07', '02', '03', '04', '05'],
    ['00', '08', '08', '08', '08', '08', '02', '03', '04', '05'],
    ['00', '09', '09', '09', '09', '09', '02', '03', '04', '05'],
    ['10', '10', '10', '10', '10', '11', '11', '11', '11', '11'],
    ['12', '12', '12', '12', '12', '13', '13', '13', '13', '13'],
    ['14', '14', '14', '14', '14', '15', '15', '15', '15', '15'],
    ['16', '16', '16', '16', '16', '17', '17', '17', '17', '17'],
    ['18', '18', '18', '18', '18', '19', '19', '19', '19', '19'],
])
board = np.array([
    [' ', ' ', ' ', ' ', '2', '3', ' ', '4', ' ', ' '],
    [' ', '1', ' ', '5', '4', '2', '3', ' ', ' ', ' '],
    [' ', ' ', ' ', '4', ' ', '1', ' ', ' ', ' ', ' '],
    ['2', '1', ' ', ' ', '2', ' ', ' ', ' ', '5', ' '],
    ['3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5'],
    [' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '2', '5', ' ', '1', ' ', ' ', ' '],
    [' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' '],
    [' ', ' ', '4', '5', ' ', '2', ' ', '3', '5', ' '],
    [' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', '4'],
])
binst = solver.Board(board=board, id_board=id_board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───────────────────┬───┬───┬───┬───┐
 0│ 1 │ 5   1   4   2   3 │ 5 │ 4 │ 2 │ 3 │
  │   ├───────────────────┤   │   │   │   │
 1│ 5 │ 1   3   5   4   2 │ 3 │ 1 │ 4 │ 2 │
  │   ├───────────────────┤   │   │   │   │
 2│ 4 │ 5   2   4   3   1 │ 2 │ 5 │ 3 │ 1 │
  │   ├───────────────────┤   │   │   │   │
 3│ 2 │ 1   5   3   2   4 │ 1 │ 3 │ 5 │ 4 │
  │   ├───────────────────┤   │   │   │   │
 4│ 3 │ 4   3   2   1   5 │ 4 │ 2 │ 1 │ 5 │
  ├───┴───────────────┬───┴───┴───┴───┴───┤
 5│ 5   2   1   3   4 │ 1   5   4   2   3 │
  ├───────────────────┼───────────────────┤
 6│ 1   3   4   2   5 │ 4   1   2   3   5 │
  ├───────────────────┼───────────────────┤
 7│ 4   2   5   1   3 │ 5   3   1   4   2 │
  ├───────────────────┼───────────────────┤
 8│ 2   3   4   5   1 │ 2   4   3   5   1 │
  ├───────────────────┼───────────────────┤
 9│ 3   4   2   1   5 │ 3   2   5   1   4 │
  └───────────────────┴───────────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/tatami_solved.png" alt="Tatami solved" width="500">

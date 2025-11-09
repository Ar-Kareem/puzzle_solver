# Circle 9 (Puzzle Type #78)

This is a dedicated solver for Circle 9.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://krazydad.com/circle9/)

**Rules**

The object is to circle just the nine numbers 1–9, such that each row, column, and block contain a single circled number. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/circle_9_unsolved.png" alt="Circle 9 unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import circle_9_solver as solver
board = np.array([
    ['7', '6', '9',  ' ', ' ', ' ',  '5', '4', '2'],
    [' ', ' ', ' ',  ' ', '9', '4',  ' ', '7', ' '],
    [' ', ' ', '8',  ' ', '8', ' ',  ' ', '6', '6'],

    [' ', ' ', ' ',  ' ', '3', ' ',  '7', ' ', ' '],
    ['2', '5', ' ',  '7', ' ', '8',  ' ', '7', '8'],
    [' ', ' ', '4',  ' ', '9', ' ',  ' ', ' ', ' '],

    ['3', '4', ' ',  ' ', '8', ' ',  '3', ' ', ' '],
    [' ', '2', ' ',  '6', '2', ' ',  ' ', ' ', ' '],
    ['8', '2', '7',  ' ', ' ', ' ',  '9', '1', '3'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```
**Script Output**
```python
Solution found

    0   1   2   3   4   5   6   7   8
          ┌───┐
 0  6   . │ 1 │ .   .   .   1   .   2
          └───┼───┐
 1  .   .   . │ 2 │ .   2   .   .   .
              └───┘           ┌───┐
 2  .   3   .   .   8   .   . │ 9 │ .
  ┌───┐                       └───┘
 3│ 8 │ .   9   .   .   .   2   .   9
  └───┘           ┌───┐
 4  .   .   .   . │ 3 │ .   .   .   .
                  └───┘   ┌───┐
 5  6   .   1   .   .   . │ 4 │ .   8
      ┌───┐               └───┘
 6  . │ 5 │ .   .   2   .   .   7   .
      └───┘           ┌───┐
 7  .   .   .   9   . │ 7 │ .   .   .
                      └───┘       ┌───┐
 8  3   .   8   .   .   .   1   . │ 6 │
                                  └───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/circle_9_solved.png" alt="Circle 9 solved" width="500">

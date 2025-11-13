# Mathrax (Puzzle Type #88)

This is a dedicated solver for Mathrax.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7mrx.htm)

**Rules**

Mathrax consists of a square grid. The goal is to fill in each cell with numbers from 1 to N, where N is the size of the puzzle's side. No number may appear twice in any row or column. Circles with additional conditions may be situated on intersections of lines inside the grid; a circle may contain:

   - A number and a sign of mathematical operation (addition, subtraction, multiplication, division); the number is the result of applying a mathematical operation to numbers in diagonally adjacent cells.
   - A letter "E" ("even"): all numbers in four cells are even.
   - A letter "O" ("odd"): all numbers in four cells are odd.

**Example puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/mathrax_unsolved.png" alt="Mathrax unsolved" width="500">


```python
import numpy as np
from puzzle_solver import mathrax_solver as solver
circle_board = np.array([
    [' ',  ' ',  '1-', '9+', ' ',  ' '],
    [' ',  '2-', ' ',  ' ',  ' ',  ' '],
    [' ',  ' ',  '1-', ' ',  'O',  ' '],
    [' ',  ' ',  ' ',  '4-', ' ',  ' '],
    [' ',  ' ',  ' ',  ' ',  ' ',  ' '],
    [' ',  ' ',  ' ',  ' ',  ' ',  ' '],
])
board = np.array([
    [' ',  ' ',  ' ',  ' ',  ' ',  ' ', ' '],
    [' ',  ' ',  ' ',  ' ',  ' ',  '2', ' '],
    [' ',  ' ',  ' ',  ' ',  ' ',  '1', ' '],
    ['2',  ' ',  ' ',  '5',  ' ',  ' ', ' '],
    [' ',  ' ',  ' ',  ' ',  ' ',  ' ', ' '],
    ['3',  ' ',  ' ',  ' ',  ' ',  ' ', ' '],
    ['1',  ' ',  ' ',  ' ',  ' ',  '5', ' '],
])
binst = solver.Board(circle_board=circle_board, board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┬───┐
 0│ 5 │ 1 │ 6 │ 4 │ 2 │ 7 │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┤
 1│ 4 │ 6 │ 3 │ 7 │ 5 │ 2 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┤
 2│ 6 │ 5 │ 4 │ 2 │ 3 │ 1 │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┤
 3│ 2 │ 4 │ 1 │ 5 │ 7 │ 3 │ 6 │
  ├───┼───┼───┼───┼───┼───┼───┤
 4│ 7 │ 2 │ 5 │ 3 │ 1 │ 6 │ 4 │
  ├───┼───┼───┼───┼───┼───┼───┤
 5│ 3 │ 7 │ 2 │ 1 │ 6 │ 4 │ 5 │
  ├───┼───┼───┼───┼───┼───┼───┤
 6│ 1 │ 3 │ 7 │ 6 │ 4 │ 5 │ 2 │
  └───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/mathrax_solved.png" alt="Mathrax solved" width="500">

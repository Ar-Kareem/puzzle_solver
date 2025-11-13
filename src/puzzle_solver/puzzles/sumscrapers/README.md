# Sumscrapers (Puzzle Type #90)

This is a dedicated solver for Sumscrapers.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7sks.htm)

**Rules**

You have a square grid. On each square of the grid you can build a tower, with its height ranging from 1 to the size of the grid. Around the edge of the grid are some numeric clues.

Your task is to build a tower on every square, in such a way that:

  - Each row contains every possible height of tower once
  - Each column contains every possible height of tower once
  - Each numeric clue describes the sum of heights of towers that can be seen if you look into the square from that direction, assuming that shorter towers are hidden behind taller ones. For example, in a 5×5 grid, a clue marked ‘11’ indicates that the the sum of the visible tower heights must be 11 (i.e. only towers 2, 4, and 5 are visible, or only towers 1, 2, 3, and 5 are visible).

In harder or larger puzzles, some towers will be specified for you as well as the clues round the edge, and some edge clues may be missing. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sumscrapers_unsolved.png" alt="Sumscrapers unsolved" width="500">


```python
import numpy as np
from puzzle_solver import sumscrapers_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', '2', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '3', ' ', '2'],
    [' ', ' ', ' ', '3', ' ', ' ', ' '],
    [' ', '4', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '5', ' ', ' '],
])
top = np.array([' ', '13', '19', '7', ' ', '18', ' '])
left = np.array(['15', '7', '12', '13', ' ', '16', '16'])
right = np.array(['15', '18', '15', ' ', '13', ' ', ' '])
bottom = np.array([' ', ' ', ' ', ' ', ' ', '7', '17'])
binst = solver.Board(board=board, top=top, left=left, right=right, bottom=bottom)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┬───┐
 0│ 2 │ 6 │ 1 │ 7 │ 4 │ 5 │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┤
 1│ 7 │ 3 │ 2 │ 4 │ 6 │ 1 │ 5 │
  ├───┼───┼───┼───┼───┼───┼───┤
 2│ 5 │ 7 │ 4 │ 1 │ 3 │ 6 │ 2 │
  ├───┼───┼───┼───┼───┼───┼───┤
 3│ 6 │ 2 │ 5 │ 3 │ 1 │ 4 │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┤
 4│ 1 │ 4 │ 3 │ 5 │ 7 │ 2 │ 6 │
  ├───┼───┼───┼───┼───┼───┼───┤
 5│ 4 │ 5 │ 7 │ 6 │ 2 │ 3 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┤
 6│ 3 │ 1 │ 6 │ 2 │ 5 │ 7 │ 4 │
  └───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sumscrapers_solved.png" alt="Sumscrapers solved" width="500">

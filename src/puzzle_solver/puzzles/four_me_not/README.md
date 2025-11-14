# Four Me Not (Puzzle Type #94)

This is a dedicated solver for Four Me Not. Also known as "Forbidden Four" or Fobidoshi.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7fbd4.htm)

**Rules**

This puzzle is played on a rectangular or square grid. Some of the cells have circles in them. The aim is to place circles into empty cells; all the circles must form an orthogonally continuous area. A line of connected circles must not contain more than 3 circles.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/four_me_not_unsolved.png" alt="Four Me Not unsolved" width="500">


```python
import numpy as np
from puzzle_solver import four_me_not_solver as solver
board = np.array([
    ['1', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', '1', '1', ' ', ' ', '1'],
    [' ', ' ', ' ', '1', '1', ' ', '1', '1', ' ', '1'],
    [' ', ' ', '1', ' ', '1', '1', '1', ' ', '1', ' '],
    [' ', '1', '1', ' ', '1', '1', ' ', ' ', ' ', '1'],
    [' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    [' ', '1', ' ', ' ', ' ', ' ', '1', ' ', '1', '1'],
    ['1', ' ', '1', ' ', ' ', ' ', ' ', '1', '1', '1'],
    [' ', '1', ' ', '1', ' ', '1', ' ', ' ', ' ', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│▒▒▒│   │▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│▒▒▒│   │   │▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.08 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/four_me_not_solved.png" alt="Four Me Not solved" width="500">

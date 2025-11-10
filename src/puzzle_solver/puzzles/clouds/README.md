# Clouds (Puzzle Type #84)

This is a dedicated solver for Clouds. Also known as Rain Clouds or Radar.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7cld.htm)

**Rules**

Clouds is a variant of Battleships puzzle. The task is to mark certain cells of the rectangular grid as belonging to a cloud.

Clouds occupy an area of rectangular shape and their width and height is at least two cells. No clouds touch each other, not even diagonally.

Numbers outside the grid show the quantity of cells occupied by clouds in corresponding row or column.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/clouds_unsolved.png" alt="Clouds unsolved" width="500">


```python
import numpy as np
from puzzle_solver import clouds_solver as solver
side = np.array([5, 7, 7, 4, 2, 7, 5, 7, 2, 2, 2, 10, 8, 3])
top = np.array([6, 6, 3, 5, 4, 4, 5, 8, 6, 3, 3, 6, 6, 6])
binst = solver.Board(side=side, top=top)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│▒▒▒│   │   │   │   │   │▒▒▒│▒▒▒│▒▒▒│   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│▒▒▒│▒▒▒│   │   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│   │   │   │   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│   │   │▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│▒▒▒│   │   │   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│   │   │▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│▒▒▒│   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│   │   │▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│   │   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│▒▒▒│▒▒▒│   │   │   │   │   │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
11│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │   │▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
12│   │   │   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │   │▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
13│   │   │   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│▒▒▒│
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 1.88 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/clouds_solved.png" alt="Clouds solved" width="500">

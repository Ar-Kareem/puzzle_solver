# Lighthouses (Puzzle Type #93)

This is a dedicated solver for Lighthouses.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7lths.htm)

**Rules**

Lighthouses is played on a rectangular or square grid. It contains black cells with numbers ("lighthouses").

The number in the cell represents the number of ships lit by the lighthouse.

A ship is lit if it is in the same row or column as the lighthouse, also ships behind other ships or lighthouses.

Each ship is lit by at least one lighthouse.

The ships are placed so that no ship touches any other ship or lighthouse, not even diagonally.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/lighthouses_unsolved.png" alt="Lighthouses unsolved" width="500">


```python
import numpy as np
from puzzle_solver import lighthouses_solver as solver
ground = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', ' ', '1'],
    ['4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' '],
    [' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0'],
    [' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' '],
])
binst = solver.Board(board=ground)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0   1
    0   1   2   3   4   5   6   7   8   9   0
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│   │   │   │▒▒▒│   │   │   │ 4 │   │   │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ 4 │   │   │   │   │▒▒▒│   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│   │   │▒▒▒│   │   │   │   │   │ 1 │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│▒▒▒│   │   │   │▒▒▒│   │ 2 │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│   │   │ 1 │   │   │   │   │   │   │   │ 0 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│▒▒▒│   │   │   │   │ 3 │   │▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│   │   │   │   │   │   │   │   │   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│   │   │   │   │   │ 2 │   │▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│▒▒▒│   │   │▒▒▒│   │   │   │   │   │ 4 │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │   │   │   │   │   │   │▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│   │   │   │   │ 2 │   │   │   │   │▒▒▒│   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/lighthouses_solved.png" alt="Lighthouses solved" width="500">

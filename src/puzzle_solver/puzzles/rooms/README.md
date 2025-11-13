# Rooms (Puzzle Type #87)

This is a dedicated solver for Rooms. Also known as Seethrough, Doors, or "Open Office".

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7wll.htm)

**Rules**

Every cell denotes a "room".

The aim is to close some "doors" between rooms.

Open doors allow to look into other rooms.

The number in the cell indicates the total number of rooms visible in horizontal and vertical direction from that room (the room itself excluded).

There can be no isolated rooms; this means that you should be able to reach all rooms by moving horizontally and vertically.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/rooms_unsolved.png" alt="Rooms unsolved" width="500">


```python
import numpy as np
from puzzle_solver import rooms_solver as solver
board = np.array([
    ['1', '6', ' ', '2', ' ', '3', '2', ' ', '3', ' '],
    ['2', ' ', '2', '2', '9', ' ', '8', '5', ' ', '7'],
    ['4', '8', ' ', '1', '8', '3', ' ', '5', '6', ' '],
    [' ', ' ', '3', '2', ' ', '3', ' ', ' ', '6', '6'],
    ['2', '7', '3', ' ', '9', ' ', '5', '3', '1', ' '],
    [' ', '6', '5', '3', ' ', '7', ' ', '3', '2', '5'],
    ['3', '7', ' ', ' ', '11',' ', '5', '4', ' ', ' '],
    [' ', '2', '2', ' ', '9', '5', '2', ' ', '2', '6'],
    ['5', ' ', '3', '2', ' ', '6', '4', '3', ' ', '6'],
    [' ', '2', ' ', '1', '13',' ', '5', ' ', '5', '10'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───┬───────────┬───────────┬───┬───┐
 0│ 1 │ 6 │     2     │ 3   2     │ 3 │   │
  │   │   │   ┌───────┤   ─────   │   │   │
 1│ 2     │ 2 │ 2   9 │     8   5       7 │
  ├────   │   │   │   ├────   ─────   │   │
 2│ 4   8     │ 1 │ 8 │ 3       5   6 │   │
  │   │   ────┼───┘   └───┐           │   │
 3│   │     3 │ 2       3 │         6   6 │
  │   │       ├────   │   │   │   ────┬───┤
 4│ 2 │ 7   3 │     9 │     5 │ 3   1 │   │
  ├───┤   │   └────   └───┐   ├───────┤   │
 5│   │ 6 │ 5   3       7 │   │ 3   2 │ 5 │
  │   │   └───┬────       └───┤       │   │
 6│ 3 │ 7     │    11       5 │ 4         │
  │   ├────   │   │       │   │   ┌────   │
 7│   │ 2   2 │   │ 9   5 │ 2 │   │ 2   6 │
  │   │   ────┼───┘   │   │   └───┤       │
 8│ 5       3 │ 2     │ 6   4   3 │     6 │
  ├────────   │   │   │   ─────   └────   │
 9│     2     │ 1 │13       5       5  10 │
  └───────────┴───┴───────────────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 1.67 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/rooms_solved.png" alt="Rooms solved" width="500">

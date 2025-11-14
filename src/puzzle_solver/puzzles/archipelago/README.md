# Archipelago (Puzzle Type #92)

This is a dedicated solver for Archipelago. Also known as "Akiperago".

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

* [**Instructions**](https://www.cross-plus-a.com/html/cros7aprg.htm)

**Rules**

Archipelago is a logic puzzle published by Nikoli. A rectangular or square grid contains black cells; some of them contain numbers. The goal is to blacken some cells of a grid according to the following rules:

   - The black cells form "islands". No two islands may share an edge; islands may be connected through their corners.
   - If an island contains a numbered cell, this number represents the amount of black cells in the island. An island may contain few numbered cells (all numbers will be the same inside an island).
   - All islands form "archipelagos". An archipelago is a group of two or more islands, connected through their corners.
   - If an archipelago contains N islands, they will be from 1 to N cells (not necessarily in that order).


**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/archipelago_unsolved.png" alt="Archipelago unsolved" width="500">


```python
import numpy as np
from puzzle_solver import archipelago_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '6', ' ', ' ', ' ', '9', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', '8', ' ', ' '],
    [' ', ' ', '6', ' ', ' ', ' ', ' ', ' ', ' ', '2'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───────┬───┬───────────┬───┬───────┐
 0│▒▒▒│       │▒▒▒│           │▒▒▒│     6 │
  │   │       │   │           │   │       │
 1│▒▒▒│       │▒▒▒│           │▒▒▒│       │
  │   │       │   │           │   │       │
 2│▒▒▒│ 6     │▒▒▒│     9     │▒▒▒│       │
  ├───┼───────┼───┼───────────┼───┼───────┤
 3│   │▒▒▒ ▒▒▒│   │▒▒▒ ▒▒▒ ▒▒▒│   │▒▒▒ ▒▒▒│
  ├───┼───┐   │   │   ┌───────┼───┼───┐   │
 4│▒▒▒│   │▒▒▒│ 5 │▒▒▒│       │▒▒▒│   │▒▒▒│
  │   │   │   │   │   │       │   │   │   │
 5│▒▒▒│   │▒▒▒│   │▒▒▒│       │▒▒▒│   │▒▒▒│
  │   │   │   │   │   │       │   │   │   │
 6│▒▒▒│ 3 │▒▒▒│   │▒▒▒│       │▒▒▒│   │▒▒▒│
  │   └───┘   │   │   └───────┘   │   │   │
 7│▒▒▒ ▒▒▒ ▒▒▒│   │▒▒▒ ▒▒▒ ▒▒▒ ▒▒▒│ 4 │▒▒▒│
  ├───────────┼───┼───────────────┼───┼───┤
 8│           │▒▒▒│             8 │▒▒▒│   │
  │           │   │               │   │   │
 9│         6 │▒▒▒│               │▒▒▒│ 2 │
  └───────────┴───┴───────────────┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.15 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/archipelago_solved.png" alt="Archipelago solved" width="500">

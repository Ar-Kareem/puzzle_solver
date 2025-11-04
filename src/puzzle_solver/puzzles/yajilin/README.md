# Yajilin (Puzzle Type #68)

* [**Play online**](https://puzzlemadness.co.uk/yajilin/hard)

* [**Instructions**](https://www.nikoli.co.jp/en/puzzles/yajilin/)

The aim of a Yajilin puzzle is to draw a single closed loop passing through every non-filled and non-clue cell.

   - The clues tell you exactly how many filled cells are in the given direction.

   - Filled cells cannot touch each other (diagonally is fine).

   - There can't be any empty cells - each cell must be a clue, filled, or contain the loop.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/yajilin_unsolved.png" alt="Yajilin unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import yajilin_solver as solver
board = np.array([
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'D1'],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['D1', '  ', '  ', '  ', '  ', 'D1', '  ', '  ', '  '],
    ['  ', '  ', '  ', 'R2', '  ', '  ', '  ', 'L1', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', 'U1', '  ', '  '],
    ['  ', 'U0', '  ', 'D0', '  ', '  ', '  ', '  ', '  '],
    ['R2', '  ', 'U2', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', 'U0', '  ', '  ', 'D0', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7   8
  ┌───────────────────────────────────┐
 0│ ┌───────────────────────────┐  1↓ │
  │ │                           │     │
 1│ └───┐  ▒▒▒  ┌───────────┐   └───┐ │
  │     │       │           │       │ │
 2│1↓   └───┐   └───┐  1↓   └───────┘ │
  │         │       │                 │
 3│ ┌───────┘  2→   └───┐  ▒▒▒ 1←  ▒▒▒│
  │ │                   │             │
 4│ └───────────────┐   │  1↑   ┌───┐ │
  │                 │   │       │   │ │
 5│▒▒▒ 0↑  ▒▒▒ 0↓   │   └───┐   │   │ │
  │                 │       │   │   │ │
 6│2→  ▒▒▒ 2↑   ┌───┘  ▒▒▒  └───┘   │ │
  │             │                   │ │
 7│ ┌───────────┘  0↑   ┌───┐  0↓   │ │
  │ │                   │   │       │ │
 8│ └───────────────────┘   └───────┘ │
  └───────────────────────────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.07 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/yajilin_solved.png" alt="Yajilin solved" width="500">

# Vermicelli (Puzzle Type #72)

* [**Play online**](https://krazydad.com/play/vermicelli)

Connect worms to make a loop that visits every square in the grid. The worm can’t fork nor cross itself, and it can't go through walls.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/vermicelli_unsolved.png" alt="Vermicelli unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import vermicelli_solver as solver
walls = np.array([
    ['  ', '  ', '  ', 'D ', '  ', '  ', 'R ', '  ', '  ', '  '],
    ['  ', 'D ', '  ', '  ', '  ', 'R ', 'D ', '  ', '  ', '  '],
    ['R ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', 'D ', '  ', '  ', '  ', '  ', '  ', 'R ', '  '],
    ['D ', '  ', 'R ', 'D ', '  ', 'DR', '  ', 'R ', 'D ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', 'D ', 'R ', 'D ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'R ', '  ', '  ', 'U ', '  '],
])
binst = solver.Board(walls=walls)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9
                              │
 0  ┌───┐   ┌───────┐   ┌───┐ │ ┌───────┐
    │   │   │ ───── │   │ │ │ │ │       │
 1  │   └───┘   ┌───┘   │ │ └───┘   ┌───┘
    │ ┌────     │       │ └────     │
 2  │ │ ┌───────┘   ┌───┘   ┌───┐   └───┐
    │ │ │           │       │   │     │ │
 3  │   └───────┐   └───┐   │   └───┐ │ │
    │     ────┐ │       │ │ │     │ │ │ │
 4  └───────┐ │ └───────┘ │ └───┐ │ └───┘
  ─────     │ └────   ────┘     │ └────
 5  ┌───┐   │   ┌───────────┐   │   ┌───┐
    │   │   │ │ │           │   │   │   │
 6  │   └───┘ │ └───────┐   │   └───┘   │
    │ ─────   └────     │ │ │     ───── │
 7  └───────────────────┘ │ └───────────┘
                          │
Solutions found: 1
status: OPTIMAL
Time taken: 0.04 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/vermicelli_solved.png" alt="Vermicelli solved" width="500">

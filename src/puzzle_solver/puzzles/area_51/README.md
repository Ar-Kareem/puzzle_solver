# Area 51 (Puzzle Type #77)

* [**Play online**](https://krazydad.com/play/area51)

You are building a labyrinthian fence enclosing Area 51. The fence must separate the aliens, kept inside, from the cacti, which are outside. The finished fence must make an enclosed circuit without touching or crossing itself.

A cell containing an uncircled digit must be surrounded by that many pieces of fence.

Numbers inside dotted-circles must be inside the fence and show how many cells can be seen up, down, left, and right (plus itself) from that cell before reaching a fence.

On black circles the fence must have a 90 degree turn with two straight sections before and after. On white circles the fence must continue straight with at least one turn immediately before or after the circle.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/area_51_unsolved.png" alt="Area 51 unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import area_51_solver as solver
board = np.array([
    ['  ', 'A ', '  ', '  ', '  ', '  ', '  ', 'O4'],
    ['  ', '  ', '  ', '2 ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '1 ', '  ', '1 ', '3 ', 'C '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '2 ', '  '],
    ['  ', '  ', '2 ', '1 ', '2 ', '1 ', '  ', '  '],
    ['  ', '  ', '  ', '2 ', '3 ', '  ', '2 ', '  '],
    ['  ', '  ', '1 ', '  ', '  ', '  ', '3 ', '  '],
    ['  ', '  ', '  ', '  ', '1 ', '  ', '  ', '  '],
    ['  ', '  ', '1 ', '  ', '  ', '  ', '  ', '2 '],
    ['3 ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
])
dots = {
    get_pos(x=1, y=1): 'B', 
    get_pos(x=5, y=7): 'B',
    get_pos(x=5, y=1): 'W', get_pos(x=0, y=5): 'W', get_pos(x=1, y=6): 'W', get_pos(x=1, y=7): 'W',
    get_pos(x=7, y=7): 'W', 
    get_pos(x=6, y=8): 'W', 
    get_pos(x=6, y=9): 'W', 
    get_pos(x=2, y=10): 'W',
}
binst = solver.Board(board=board, dots=dots)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution:

    0   1   2   3   4   5   6   7
  ┌───────────────┐   ┌───────────┐
 0│     A         │   │        O4 │
  │   ┌───────┐   │   │           │
 1│   │       │ 2 │   │           │
  │   │   ┌───┘   └───┘   ┌───────┘
 2│   │   │     1       1 │ 3   C
  └───┘   └───────────┐   └───────┐
 3                    │     2     │
  ┌───┐   ┌───────────┘   ┌───────┘
 4│   │   │ 2   1   2   1 │
  │   └───┘       ┌───┐   └───────┐
 5│             2 │ 3 │     2     │
  └───────────────┘   │   ┌───────┘
 6          1         │   │ 3
  ┌───────┐   ┌───────┘   └───────┐
 7│       │   │     1             │
  └───┐   └───┘       ┌───────────┘
 8    │     1         │         2
  ┌───┘       ┌───┐   └───────────┐
 9│ 3         │   │               │
  └───────────┘   └───────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.05 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/area_51_solved.png" alt="Area 51 solved" width="500">

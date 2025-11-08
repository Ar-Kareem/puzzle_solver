# Cow and Cactus (Puzzle Type #74)

This is a dedicated solver for Cow and Cactus.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://krazydad.com/play/corral)

You are building a fence for your ranch. The fence must separate the cows inside, from the cacti outside.

The finished fence must make an enclosed circuit without touching or crossing itself.

Numbers inside dotted-circles are corral clues.  These squares must be inside the fence.  The number shows how many cells can be seen up, down, left, and right (plus itself) from that location before reaching a fence.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/cow_and_cactus_unsolved.png" alt="Cow and Cactus unsolved" width="500">

Code to utilize this package and solve the puzzle:

Note: `W` refers to a cow and `P` refers to a cactus (sadly both words start with 'C' so we have to avoid using that)

```python
import numpy as np
from puzzle_solver import cow_and_cactus_solver as solver
board = np.array([
    ['  ', '  ', '15', '  ', '11', '9 ', '8 ', '11'],
    ['  ', '  ', '  ', 'P ', '  ', '  ', '  ', '  '],
    ['W ', '3 ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['W ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['W ', '  ', '  ', '  ', '  ', 'W ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '4 ', '  '],
    ['W ', '  ', '  ', '  ', 'W ', 'W ', 'P ', 'W '],
    ['P ', 'W ', '  ', '  ', 'W ', 'W ', '  ', 'P '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution:

    0   1   2   3   4   5   6   7
  ┌───────────────────────────────┐
 0│        15      11   9   8  11 │
  ├───────┐   ┌───┐       ┌───┐   │
 1│       │   │ P │       │   │   │
  ├───────┘   │   │   ┌───┘   │   │
 2│ W   3     │   │   │       │   │
  │   ┌───┐   │   │   └───┐   │   │
 3│ W │   │   │   │       │   │   │
  │   │   │   │   └───┐   │   └───┤
 4│ W │   │   │       │ W │       │
  ├───┘   │   │   ┌───┘   └───────┤
 5│       │   │   │         4     │
  ├───────┘   │   │       ┌───┐   │
 6│ W         │   │ W   W │ P │ W │
  ├───┐       │   │       │   └───┤
 7│ P │ W     │   │ W   W │     P │
  └───┴───────┴───┴───────┴───────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.04 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/cow_and_cactus_solved.png" alt="Cow and Cactus solved" width="500">

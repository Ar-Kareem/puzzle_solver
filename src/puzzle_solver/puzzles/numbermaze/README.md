# NumberMaze (Puzzle Type #69)

This is a dedicated solver for NumberMaze. Also known as Dot Stream.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://puzzlemadness.co.uk/numbermaze/hard)

Your aim is to draw a single line starting from the number 1 through all of the numbers, covering all of the cells in the grid as you go.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/numbermaze_unsolved.png" alt="Number Maze unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import numbermaze_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '3', ' ', '5', ' ', ' ', '4', ' ', '7'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '#', ' ', ' ', '#', ' ', '6', '8', ' '],
    ['2', ' ', '#', '#', ' ', ' ', ' ', ' ', ' '],
    ['#', ' ', '1', ' ', ' ', '#', ' ', '#', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['9', ' ', '10', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', '11', '#', ' ', ' ', ' ', '#'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7   8
  ┌───────────────────────────────────┐
 0│ ┌───────────────────────┐   ┌───┐ │
  │ │                       │   │   │ │
 1│ └───3   ┌───5───────────4   │   7 │
  │     │   │                   │   │ │
 2│ ┌───┘   │   ┌───────┐   ┌───┘   │ │
  │ │       │   │       │   │       │ │
 3│ │  ▒▒▒  └───┘  ▒▒▒  └───6   8───┘ │
  │ │                           │     │
 4│ 2───┐  ▒▒▒ ▒▒▒  ┌───────┐   └───┐ │
  │     │           │       │       │ │
 5│▒▒▒  └───1   ┌───┘  ▒▒▒  │  ▒▒▒  │ │
  │             │           │       │ │
 6│ ┌───────────┘   ┌───────┘   ┌───┘ │
  │ │               │           │     │
 7│ 9───┐  10───┐   └───┐  ▒▒▒  │  ▒▒▒│
  │     │   │   │       │       │     │
 8│▒▒▒  └───┘  11  ▒▒▒  └───────┘  ▒▒▒│
  └───────────────────────────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.05 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/numbermaze_solved.png" alt="Number Maze solved" width="500">

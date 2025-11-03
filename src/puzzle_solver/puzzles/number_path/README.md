# Number Path (Puzzle Type #67)

* [**Play online**](https://puzzlemadness.co.uk/numberpath/large)

The aim is to draw a single unbroken line from the start cell (green) to the end cell (red).

The numbers along the path must follow the pattern 1, 2, 3, 4, 1, 2, 3, 4, 1 etc.

The path can move in any direction horizontally, vertically or diagonally. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/number_path_unsolved.png" alt="Number Path unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import number_path_solver as solver
board = np.array([
    ['3', '2', '4', '1', '2', '3', '1', '2'],
    ['4', '3', '1', '4', '3', '1', '4', '3'],
    ['2', '1', '2', '4', '2', '4', '4', '1'],
    ['3', '1', '3', '1', '2', '3', '2', '4'],
    ['4', '1', '2', '3', '2', '1', '3', '1'],
    ['2', '3', '4', '4', '1', '4', '3', '2'],
    ['3', '1', '4', '3', '3', '4', '1', '4'],
    ['2', '4', '1', '2', '1', '2', '3', '2'],
])
start = Pos(x=6, y=6)
end = Pos(x=7, y=6)
binst = solver.Board(board=board, start=start, end=end)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7
  ┌───┬───┬───┬───┬───┬───┬───┬───┐
 0│ ↓ │ ← │ → │ → │ → │ ↘ │ → │ ↓ │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 1│ ↘ │ ↗ │ ↖ │ ← │ ← │ ↙ │ ↑ │ ↙ │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 2│ ↓ │ ← │ ↖ │ ↓ │ ↑ │ ↑ │ → │ ↙ │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 3│ ↓ │ ↘ │ ↗ │ ↖ │ ↙ │ ↑ │ ↓ │ ↓ │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 4│ ↗ │ ↙ │ ↑ │ ↙ │ ↗ │ ↖ │ ↗ │ ↓ │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 5│ → │ ↘ │ ↖ │ → │ ↑ │ ↑ │ ↘ │ ← │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 6│ ↘ │ ↙ │ ← │ ↑ │ ↗ │ ↙ │ ↘ │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 7│ ↑ │ → │ → │ ↑ │ → │ ↖ │ ↖ │ ← │
  └───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/number_path_solved.png" alt="Number Path solved" width="500">

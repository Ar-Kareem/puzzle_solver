# Linesweeper (Puzzle Type #84)

This is a dedicated solver for Linesweeper.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://sudoku-puzzles.net/linesweeper-easy/)

* [**Android App**](https://play.google.com/store/apps/details?id=com.andreasabbatini.logicgamestk)

**Rules**

Linesweeper (also known as "Loop") is a logic puzzle played on a rectangular grid. The goal is to draw a single, continuous, non-intersecting loop that connects the centers of the grid cells.

Certain cells contain numbers that impose additional constraints on the loop's path.


   - The loop must be continuous and cannot cross itself or branch.
   - The numbered cells cannot be part of the loop.
   - A numbered cell dictates how many of its 8 surrounding cells contain part of the loop.
     -  Example: A cell with "0" means none of the 8 adjacent cells can contain the loop.


**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/linesweeper_unsolved.png" alt="Linesweeper unsolved" width="500">


```python
import numpy as np
from puzzle_solver import linesweeper_solver as solver
board = np.array([
    [' ', '3', ' ', ' ', ' ', ' ', '5', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '6', ' ', '5', ' ', ' ', ' ', ' ', ' ', '5'],
    [' ', ' ', '5', ' ', ' ', '7', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '6', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', '7', '6', ' ', ' ', ' ', '7', ' ', '5'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '7', ' ', ' ', '8', ' ', '8', ' ', '8', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['3', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9

 0      3       ┌───────┐   5   ┌───────┐
                │       │       │       │
 1  ┌───────────┘       └───────┘   ┌───┘
    │                               │
 2  │   6       5   ┌───────┐       │   5
    │               │       │       │
 3  └───┐   5   ┌───┘   7   └───┐   └───┐
        │       │               │       │
 4      └───────┘   6   ┌───────┘   ┌───┘
                        │           │
 5  ┌───┐   7   6   ┌───┘       7   │   5
    │   │           │               │
 6  │   └───┐   ┌───┘   ┌───────┐   └───┐
    │       │   │       │       │       │
 7  │   7   └───┘   8   │   8   │   8   │
    │                   │       │       │
 8  └───┐       ┌───┐   └───┐   └───┐   │
        │       │   │       │       │   │
 9  3   └───────┘   └───────┘   5   └───┘

Solutions found: 1
status: OPTIMAL
Time taken: 0.08 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/linesweeper_solved.png" alt="Linesweeper solved" width="500">

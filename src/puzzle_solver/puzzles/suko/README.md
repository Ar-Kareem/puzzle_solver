# Suko (Puzzle Type #65)

* [**Play online**](https://puzzlemadness.co.uk/suko/medium)

Your aim is to insert the numbers 1-9 in to the grid so that each number only appears once, and all the totals are satisfied.
There are two types of totals you can see in this grid,

    Quadrant totals: These are the numbers given in the circles inside the grid itself. The quadrant total in the top-left is 14, for example. We can add the 4 cells around this total together, 6+1+2+5, to check that we get 14.

    We can do the same thing for the lower-right quadrant total of 25, i.e. 5+8+3+9 to make sure that gives us 25.

    Layout totals: There will always be three different colours for the cells in each puzzle. The numbers above the grid tell you what these should add to. From this puzzle, we can see that,
        The green cells should add to 9 (2+7).
        The blue cells should add to 20 (8+3+9).
        The red cells should add to 16 (6+1+4+5).

Suko is a Trademark owned by Jai Kobayaashi Gomer of Kobayaashi Studios. The original design and puzzle format was also created by Jai. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/suko_unsolved.png" alt="Suko unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import suko_solver as solver
board = np.array([
    ['R', 'B', 'G'],
    ['R', 'B', 'G'],
    ['R', 'R', 'G'],
])
quadrant = np.array([
    [21, 23],
    [17, 15],
])
color_sums = {'R': 19, 'G': 17, 'B': 9}
binst = solver.Board(board=board, quadrant=quadrant, color_sums=color_sums)
```

**Script Output**

```python
Solution found

    0   1   2
  ┌───┬───┬───┐
 0│ 4 │ 7 │ 5 │
  ├───┼───┼───┤
 1│ 8 │ 2 │ 9 │
  ├───┼───┼───┤
 2│ 6 │ 1 │ 3 │
  └───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/suko_solved.png" alt="Suko solved" width="500">

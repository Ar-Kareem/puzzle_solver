# Images

This folder contains all the images used in the `README`'s.

We also list screenshots of several website that host collections of puzzles as well as highlighting in blue which puzzles are implemented in this repo.

Below are the websites from the screenshots:

1. https://www.chiark.greenend.org.uk/~sgtatham/puzzles (All puzzles are playable)
2. https://www.puzzle-kurodoko.com/ (All puzzles are playable)
3. https://www.nikoli.co.jp/en/puzzles/ (Does not have playable puzzles, only instructions)
4. https://www.brainbashers.com/puzzles.asp (All puzzles are playable; Website up since 1997, relic of an old past. Used to love this website when I was a kid)
5. https://krazydad.com (Some puzzles are playable, some are only printable)
6. https://puzzlemadness.co.uk/ (All puzzles are playable)


Most of the puzzles we target in this repo are pen and paper puzzles (i.e. not dynamic puzzles). The simplest and biggest difference is that if the puzzle can be played on a printed sheet of paper then it is not a dynamic puzzle. 

The only two exceptions to the above rule are "Pipes" and "Flip", "Pipes" might not easilly work on a printed sheet of paper as the icons need to be rotated but I still consider it to be significantly on the pen and paper side of the spectrum, and "Keen" which is a mathematical puzzle that is more on the pen and paper side of the spectrum. While "Flip" is a dynamic puzzle as flipping a square changes the state of the board but it can be modeled as a static pen and paper puzzle with slight modifications of how the puzzle is represented that does not change the final solution.

We rarely provide solvers for dynamic puzzles except for (at the time of writing) five puzzles which are Minesweeper, Guess, Inertia, Flood it, and Twiddle.

Below we list the puzzles that are yet to be implemented in the websites listed above.

## Website 1 ✅

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzle_list_1.png" alt="Website 1" width="500">

**https://www.chiark.greenend.org.uk/~sgtatham/puzzles (All puzzles are playable)**

All pen and paper puzzles have been implemented. 

A total of 33 puzzles were implemented, and 7 remaining puzzles we aren't targeting which are all dynamic.

## Website 2 ✅

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzle_list_2.png" alt="Website 2" width="500">

**https://www.puzzle-kurodoko.com/ (All puzzles are playable)**

Equivalant to: **https://www.puzzles-mobile.com/**

All pen and paper logic puzzles have been implemented.

39 puzzles were implemented, and only 1 remaining puzzle we aren't targeting which is a word search puzzle. We are interested in logic games that depend on pure mathematical reasoning and not simply dependent on a specific language.

## Website 3 (In Progress)

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzle_list_3_full.png" alt="Website 3" width="500">

**https://www.nikoli.co.jp/en/puzzles/ (Does not have playable puzzles, only instructions)**

Only 16 out of 45 puzzles are implemented.

There are still several puzzles in here that we plan on implementing in the future. As this website does not host playable version of the puzzles, we will slightly deprioritize them unless the puzzles are hosted somewhere else online in another website.

## Website 4 ✅

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzle_list_4.png" alt="Website 4" width="500">

**https://www.brainbashers.com/puzzles.asp (All puzzles are playable; Website up since 1997)**

All pen and paper puzzles have been implemented.

21 puzzles were implemented, and only 1 remaining puzzle we aren't targeting which is a dynamic puzzle (Net Slide also on website 1).

## Website 5 (In Progress)

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzle_list_5.png" alt="Website 5" width="500">

**https://krazydad.com (Some puzzles are playable, some are only printable)**

The website has exactly 86 puzzles in total:

- 54 are Sudoku-like puzzles (?/54 implemented)
- 22 Interactive and nonudoku puzzles (17/22 implemented; 5 remaining)
- 10 Printable only non-Sudoku puzzles (4/10 implemented; 6 remaining)

Sudoku variants are so abundant so they are currently not prioritized.

## Website 6 (In Progress)

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzle_list_6.png" alt="Website 6" width="500">

**https://puzzlemadness.co.uk/ (All puzzles are playable)**

The website has exactly 90 puzzles in total:

- 38 are Sudoku-like puzzles (?/38 implemented)
- 48 logic puzzles (39/48 implemented; 9 remaining)
- 4 other puzzles that we aren't targeting (word search, solitaire, 4-in-a-row, pairs)

Sudoku variants are similarly abundant in this website, thus they are currently not prioritized.

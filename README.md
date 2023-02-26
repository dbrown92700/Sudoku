# Sudoku Solver

- Save your puzzle as a text file (with .txt extension) using dashes and digits as shown below.
- Run with python3 main.py.
- Program will present a menu of all .txt files in the directory and ask for which one to solve.

Currently a single pass will do multiple iterations eliminating candidate values, looking for
unique row, column and cell values, and looking for pairs before prompting the user to continue.
Continuing will run through another set of iterations.  The prompt is in place in case the program
is unable to solve the puzzle after multiple attempts.

The program currently has no "Advanced" elimination methods like x-wing, swordfish, etc. and may be
unable to complete the puzzle.

## Sample Starting Puzzle File
Should contain a 9X9 block of dashes and digits with no exra spacing.

~~~
---93---5
96--85---
--3----2-
-----64-2
-958723-1
21649-5-7
-----8--9
32-7---5-
-49----76
~~~

## Minesweeper

Run the program using Python 3 with following arguments: numberOfRows, numberOfColumns, numberOfMines.

Example:

## `python3 minesweeper.py 15 15 30`

### Implementation

I chose Python because it is very handy and simple language for such a short program. The data structure I used to store the playboard is 2D list of Tile objects (Tile is a single field of a playboard). That gives me easy access to individual elements of the playboard (upper-right corner element: board[0][numberOfColumns-1].value). See the code for the specific classes and algorithms I used.

The visualization of the game is provided by simple and lightweight library graphics.py.

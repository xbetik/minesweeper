from graphics import *
import random, sys, unittest

TILE_SIZE = 30

'''
Class Tile represents a single field.
Possible values:
  'X' (mine)
  ' ' (zero surrounding mines)
  n (the number of surrounding mines, 0<n<9)
'''
class Tile():
    def __init__(self, value):
        self.value = value

'''
Class Game operates with a board (2d list of Tiles) of size rows*cols.
'''
class Game():
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[Tile(' ') for _ in range(cols)] for _ in range(rows)]
    
    def placeMines(self):
        placed_mines = []
        for _ in range(self.mines):
            mine_row, mine_col = tryToPlaceMine(placed_mines, self.rows, self.cols)
            placed_mines.append((mine_row, mine_col))
            self.board[mine_row][mine_col].value = 'X'
            
    def solve(self):
        for row in range(self.rows):        
            for col in range(self.cols):
                if self.board[row][col].value != 'X':
                    neighborMines = countNeighborMines(self.board, row, col, self.rows, self.cols)
                    if neighborMines > 0:
                        self.board[row][col].value = neighborMines
        
    def run(self):
        if self.mines > self.rows*self.cols:
            print("Incorrect input. More mines than fields.")
            return 0
        if self.rows < 1 or self.cols < 1:
            print("Incorrect input. Smallest playground needs atleast one row and one column.")
            return 0
        self.placeMines()
        self.solve()
        graphics = Graphics(self.board, self.rows, self.cols, TILE_SIZE, mines)
        graphics.draw()
        return 1

    def consolePrint(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.board[i][j].value, end='')
            print()

def tryToPlaceMine(mines_placed, rows, cols):
    while True:
        mine_row = random.randint(0, rows-1)
        mine_col = random.randint(0, cols-1)
        if (mine_row, mine_col) not in mines_placed:
            return mine_row, mine_col
    
def isValidField(row, col, rows, cols):
    return row >= 0 and col >= 0 and row < rows and col < cols
    
def countNeighborMines(board, row, col, rows, cols):
    totalMines = 0
    # Upper-left, upper-middle, upper-right field check
    if isValidField(row-1, col-1, rows, cols) and board[row-1][col-1].value == 'X':
        totalMines+=1
    if isValidField(row-1, col, rows, cols) and board[row-1][col].value == 'X':
        totalMines+=1
    if isValidField(row-1, col+1, rows, cols) and board[row-1][col+1].value == 'X':
        totalMines+=1
        
    # Middle-left, middle-right field check
    if isValidField(row, col-1, rows, cols) and board[row][col-1].value == 'X':
        totalMines+=1
    if isValidField(row, col+1, rows, cols) and board[row][col+1].value == 'X':
        totalMines+=1
        
    # Down-left, down-middle, down-right field check
    if isValidField(row+1, col-1, rows, cols) and board[row+1][col-1].value == 'X':
        totalMines+=1
    if isValidField(row+1, col, rows, cols) and board[row+1][col].value == 'X':
        totalMines+=1
    if isValidField(row+1, col+1, rows, cols) and board[row+1][col+1].value == 'X':
        totalMines+=1
    return totalMines

# I used graphics.py because it is a simple library for drawing basic shapes
class Graphics():
    def __init__(self, board, rows, cols, size, mines):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.size = size
        self.mines = mines
        self.canvas = GraphWin('MineSweeper (' + str(rows) + 'x' + str(cols) + 'x' + str(mines) + ')', width = self.size*self.rows, height = self.size*self.rows)
        
    def draw(self):
        colors = ['blue', 'green', 'red', 'orange', 'brown', 'yellow', 'grey', 'purple']
        for row in range(self.rows):
            for col in range(self.cols):
                tile_grid = Rectangle(Point(row*self.size, col*self.size), Point(row*self.size+self.size, col*self.size+self.size))
                tile_grid.draw(self.canvas)
                value = Text(Point(row*self.size+(self.size/2), col*self.size+(self.size/2)), self.board[row][col].value)
                if isinstance(self.board[row][col].value, int):
                    value.setOutline(colors[self.board[row][col].value-1])
                value.draw(self.canvas)
        self.canvas.getMouse()
        self.canvas.close()

# Some trivial tests for incorrect inputs.
class TestIncorrectInputs(unittest.TestCase):
    def test_more_mines_than_fields(self):
        g = Game(10, 10, 101)
        self.assertEqual(g.run(), 0, "More mines than fields")
    
    def test_incorrect_number_of_rows_or_cols(self):
        g1 = Game(0, 1, 0)
        self.assertEqual(g1.run(), 0, "Incorrect number of rows")
        g2 = Game(1, 0, 0)
        self.assertEqual(g2.run(), 0, "Incorrect number of cols")
        g3 = Game(-2, -3, 0)
        self.assertEqual(g3.run(), 0, "Incorrect number of rows or cols")
         
if __name__ == '__main__':
    args = sys.argv
    rows, cols, mines = int(args[1]), int(args[2]), int(args[3])
    game = Game(rows, cols, mines)
    game.run()
    
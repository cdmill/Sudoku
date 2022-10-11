""" Sudoke game by Casey Miller, September 2022 """

import pygame as pg
import random
import time

# setup
pg.init()
SCREEN = pg.display.set_mode((600, 650))
pg.display.set_caption("Sudoku")
FONT = pg.font.SysFont("Menlo", 20)

value = 0
clicked = False
CELL_LENGTH = 500 / 9

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (57, 255, 20)

# backing grid
grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

def calculate_mouse_pos(pos):
    """ Get the coordinates of a mouse click relative to the game window (x, y) and the sudoku grid (m, n) """
    global m, n, x, y

    # calculate the x,y position of the mouse click
    x = pos[ 0 ]
    y = pos[ 1 ]
    # calculate which cell was clicked
    m = (pos[ 0 ]-50) // CELL_LENGTH
    n = (pos[ 1 ]-100) // CELL_LENGTH


def draw_lines():
    """ Draws the lines of the suduko grid """

    for i in range(0 , 10):
        if( i % 3 == 0 ):
            lineThickness = 6
        else:
            lineThickness = 2
        # vertical lines
        pg.draw.line(SCREEN, (166, 166, 166), (50 + i*CELL_LENGTH, 100), (50 + i*CELL_LENGTH, 600 ), lineThickness )
        # horizonatal lines
        pg.draw.line(SCREEN, (166, 166, 166), (48, 100 + i*CELL_LENGTH), (553, 100 + i*CELL_LENGTH), lineThickness )    


def fill_grid():
    """ Draws the contents of the backing grid onto the display grid """
 
    for col in range(9):
        for row in range(9):
            curr = grid[row][col]
            if curr == 0:
                continue
            elif valid_value(row, col, curr):
                text = FONT.render(str(curr), True, WHITE)
            else:
                text = FONT.render(str(curr), True, RED) # incorrect value

            SCREEN.blit(text, (72 + row*CELL_LENGTH, 115 + col*CELL_LENGTH))   

def valid_value(row, col, value):
    """ Determines if a given value is valid in the sudoku grid. A block refers to a 3x3 grouping of cells """

    # check columns/rows for current value
    for i in range(9):
        if grid[row][i] == value and not i == col:
            return False
        if grid[i][col] == value and not i == row:
            return False

    # check block for current value
    blockX = row // 3
    blockY = col // 3
    for i in range(blockX * 3, blockX * 3 + 3):
        for j in range (blockY * 3, blockY * 3 + 3):
            if grid[i][j] == value and not i == row and not j == col:
                return False
    return True

def generate_grid(difficulty):
    """ Generates a starting grid based on the given difficulty level """

    if difficulty == "normal":
        k = 30
    if difficulty == "hard":
        k = 10

    # fill grid with k number of random values
    for i in range(k):
        col = random.randrange(0, 9)
        row = random.randrange(0, 9)
        value = random.randrange(1, 10)
        if valid_value(col, row, value):
            grid[col][row] = value
            i += 1

def clear_grid():
    """ Clears backing grid """

    global grid
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

def find_empty_cell():
    """ Finds an empty cell in *this* sudoku grid. Returns a tuple of the index """

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

def solve():
    """ Solves *this* sudoku grid """

    # find next empty cell
    emptyCell = find_empty_cell()
    if not emptyCell:
        return True
    else:
        row, col = emptyCell
    
    for i in range(1, 10):
        if valid_value(row, col, i):
            grid[row][col] = i

            if solve():
                return True

            grid[row][col] = 0
    return False

def format_time(secs):
    """ Formats time into a readable format """

    sec = secs%60
    minute = secs//60
    formatted = " " + str(minute) + ":" + str(sec)
    return formatted

def draw_time(time):
    """ Draws timer to the screen """

    text = FONT.render("Time: " + format_time(time), True, WHITE)
    SCREEN.blit(text, (500-(text.get_width()/2), 57))

class Button():
		
	width = 80
	height = 30

	def __init__(self, x, y, text):
		self.x = x - self.width/2
		self.y = y
		self.text = text

	def draw_button(self):

		global clicked
		action = False

		# get mouse position
		pos = pg.mouse.get_pos()

		# create Rect object for the button
		button_rect = pg.Rect(self.x, self.y, self.width, self.height)

		# add text to button
		text_img = FONT.render(self.text, True, WHITE)
		text_len = text_img.get_width()
		
		# check mouseover and clicked conditions
		if button_rect.collidepoint(pos):
			if pg.mouse.get_pressed()[0] == 1:
				clicked = True
				pg.draw.rect(SCREEN, BLACK, button_rect)
			elif pg.mouse.get_pressed()[0] == 0 and clicked == True:
				clicked = False
				action = True
			else:
				SCREEN.blit(FONT.render(self.text, True, GREEN), (self.x + int(self.width / 2) - int(text_len / 2), self.y+7.5))
		else:
			SCREEN.blit(FONT.render(self.text, True, WHITE), (self.x + int(self.width / 2) - int(text_len / 2), self.y+7.5))

		return action

# initialize buttons        
new = Button(90, 50, 'New')
solved = Button(300, 50, 'Solve')
normal = Button(170, 30, "Normal")
hard = Button(170, 60, "Hard")
# initialize flags and timer
running=True  
newClicked = False
isSolved = False
isUnsolvable = False
start = time.time()

while running:
    SCREEN.fill(BLACK)
    draw_lines()
    if not isSolved:
        playTime = round(time.time() - start)
        draw_time(playTime)
    if new.draw_button():
        newClicked = True
    if solved.draw_button():
        if solve():
            isSolved = True
        else:
            isUnsolvable = True

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()    
        if event.type == pg.MOUSEBUTTONDOWN:
            calculate_mouse_pos(pg.mouse.get_pos())
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                value = 1
            if event.key == pg.K_2:
                value = 2   
            if event.key == pg.K_3:
                value = 3
            if event.key == pg.K_4:
                value = 4
            if event.key == pg.K_5:
                value = 5
            if event.key == pg.K_6:
                value = 6
            if event.key == pg.K_7:
                value = 7
            if event.key == pg.K_8:
                value = 8
            if event.key == pg.K_9:
                value = 9
            if event.key == pg.K_BACKSPACE:
                value = -1

        if value != 0: 
            if value == -1:
                grid[int(m)][int(n)] = 0
            elif x > 48 and x < 553 and y > 100 and y < 600:
                grid[int(m)][int(n)] = value
            value = 0

    if newClicked:
        if normal.draw_button():
            clear_grid()
            generate_grid("normal")
            newClicked = False
            isSolved = False
            isUnsolvable = False
        if hard.draw_button():
            clear_grid()
            generate_grid("hard")
            newClicked = False
            isSolved = False
            isUnsolvable = False
        start = time.time()

    if isSolved or not find_empty_cell():
        draw_time(playTime)
        text = FONT.render("Puzzle Solved!", True, RED)
        SCREEN.blit(text, (300 - (text.get_width()/2), 5))

    if isUnsolvable:
        text = FONT.render("Puzzle Unsolvable.", True, RED)
        SCREEN.blit(text, (300 - (text.get_width()/2), 5))  
    
    fill_grid()
    pg.display.flip() 
   
pg.quit()    
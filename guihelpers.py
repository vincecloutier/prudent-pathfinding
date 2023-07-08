import pygame
from cell import Cell
from algorithms import pathfinder, astar_priority, dijkstra_priority
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, GRID_COLUMNS, GRID_ROWS, GAP, COLOURS


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, True, (0, 0, 0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTONS = [
    Button(COLOURS['RED'], 0, SCREEN_HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, 'A*'),
    Button(COLOURS['GREEN'], BUTTON_WIDTH, SCREEN_HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, 'Dijkstra'),
    Button(COLOURS['BLACK'], BUTTON_WIDTH * 2, SCREEN_HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, 'Reset'),
]


def pathfinding(window, grid, startCell, endCell, algorithm):
    for row in grid:
        for cell in row:
            cell.updateNeighbours(grid)
    if algorithm == 'astar':
        pathfinder(lambda: draw(window, grid), grid, startCell, endCell, astar_priority)
    elif algorithm == 'dijkstra':
        pathfinder(lambda: draw(window, grid), grid, startCell, endCell, dijkstra_priority)

def make_grid():
    grid = []
    for i in range(GRID_COLUMNS):
        grid.append([])
        for j in range(GRID_ROWS):
            cell = Cell(i , j, GAP)
            grid[i].append(cell)
    return grid

def draw(window, grid):
    window.fill(COLOURS['WHITE'])
    for row in grid:
        for cell in row:
            cell.draw(window)
    for i in range(GRID_COLUMNS):
        pygame.draw.line(window, COLOURS['BLACK'], (0, i * GAP), (SCREEN_WIDTH, i * GAP))
    for j in range(GRID_ROWS):
        pygame.draw.line(window, COLOURS['BLACK'], (j * GAP, 0), (j * GAP, SCREEN_HEIGHT - 200))  # adjust height here
    for button in BUTTONS:  # make sure to draw buttons after grid lines
        button.draw(window)
    pygame.display.update()

def handle_mouse_click(grid, startCell, endCell):
    if pygame.mouse.get_pressed()[0]:
        y, x = pygame.mouse.get_pos()
        if y < SCREEN_HEIGHT - 200:  # restrict cell selection to grid area
            row = y // GAP
            col = x // GAP
            cell = grid[row][col]
            if not startCell and cell != endCell:
                startCell = cell
                startCell.makeStart()
            elif not endCell and cell != startCell:
                endCell = cell
                endCell.makeEnd()
            elif cell != endCell and cell != startCell:
                cell.makeWall()
    return startCell, endCell

def reset_grid(grid):
    startCell = None
    endCell = None
    for row in grid:
        for cell in row:
            cell.reset()
    return startCell, endCell
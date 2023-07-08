import pygame
from cell import Cell
from constants import *

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
        pygame.draw.line(window, COLOURS['BLACK'], (j * GAP, 0), (j * GAP, SCREEN_HEIGHT - BUTTON_HEIGHT))  # adjust height here
    for button in BUTTONS:  # make sure to draw buttons after grid lines
        button.draw(window)
    pygame.display.update()

def handle_mouse_click(grid, startCell, endCell, wall_only = False):
    y, x = pygame.mouse.get_pos()
    row = y // GAP
    col = x // GAP
    cell = grid[row][col]
    if not wall_only:
        if not startCell and cell != endCell:
            startCell = cell
            startCell.makeStart()
        elif not endCell and cell != startCell:
            endCell = cell
            endCell.makeEnd()
    if cell != endCell and cell != startCell:
        cell.makeWall()
    return startCell, endCell

def reset_grid(grid):
    startCell = None
    endCell = None
    for row in grid:
        for cell in row:
            cell.reset()
    return startCell, endCell
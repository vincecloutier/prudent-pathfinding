import pygame
from cell import Cell
from algorithms import pathfinder, astar_priority, dijkstra_priority
from constants import SCREENHEIGHT, SCREENWIDTH, GRID_WIDTH, GRID_HEIGHT, GAP, COLOURS

def makeGrid():
    grid = []
    for i in range(GRID_WIDTH):
        grid.append([])
        for j in range(GRID_HEIGHT):
            cell = Cell(i , j, GAP)
            grid[i].append(cell)
    return grid

def draw(window, grid):
    window.fill(COLOURS['WHITE'])
    for row in grid:
        for cell in row:
            cell.draw(window)
    for i in range(GRID_WIDTH):
        pygame.draw.line(window, COLOURS['BLACK'], (0, i * GAP), (SCREENWIDTH, i * GAP))
        for j in range(GRID_HEIGHT):
            pygame.draw.line(window, COLOURS['BLACK'], (j * GAP, 0), (j * GAP, SCREENHEIGHT))
    pygame.display.update()

def handle_mouse_click(grid, startCell, endCell):
    if pygame.mouse.get_pressed()[0]:
        y, x = pygame.mouse.get_pos()
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

def pathfinding(window, grid, startCell, endCell, algorithm):
    for row in grid:
        for cell in row:
            cell.updateNeighbours(grid)
    if algorithm == 'astar':
        pathfinder(lambda: draw(window, grid), grid, startCell, endCell, astar_priority)
    elif algorithm == 'dijkstra':
        pathfinder(lambda: draw(window, grid), grid, startCell, endCell, dijkstra_priority)

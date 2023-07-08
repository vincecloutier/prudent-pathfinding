import pygame
from cell import Cell
from algorithms import astar, dijkstra, bfs, dfs

def makeGrid():
    grid = []
    gap = 800 // 50
    for i in range(50):
        grid.append([])
        for j in range(50):
            cell = Cell(i , j, gap)
            grid[i].append(cell)
    return grid

def draw(window, grid):
    gap = 800 // 50
    window.fill((255, 255, 255))
    for row in grid:
        for cell in row:
            cell.draw(window)
    for i in range(50):
        pygame.draw.line(window, (0 , 0, 0), (0, i * gap), (800, i * gap))
        for j in range(50):
            pygame.draw.line(window, (0 , 0, 0), (j * gap, 0), (j * gap, 800))
    pygame.display.update()

def handle_mouse_click(grid, startCell, endCell):
    if pygame.mouse.get_pressed()[0]:
        gap = 800 // 50
        y, x = pygame.mouse.get_pos()
        row = y // gap
        col = x // gap
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
        astar(lambda: draw(window, grid), grid, startCell, endCell)
    elif algorithm == 'dijkstra':
        dijkstra(lambda: draw(window, grid), grid, startCell, endCell)
    elif algorithm == 'bfs':
        bfs(lambda: draw(window, grid), grid, startCell, endCell)
    elif algorithm == 'dfs':
        dfs(lambda: draw(window, grid), grid, startCell, endCell)
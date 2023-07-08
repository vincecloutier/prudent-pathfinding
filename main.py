import pygame
from constants import SCREENWIDTH, SCREENHEIGHT
from guihelpers import makeGrid, draw, handle_mouse_click, reset_grid, pathfinding

if __name__ == "__main__":
    window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")
    grid = makeGrid()
    startCell = None
    endCell = None
    run = True
    while run:
        draw(window, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and startCell and endCell:
                    pathfinding(window, grid, startCell, endCell, 'astar')
                elif event.key == pygame.K_d and startCell and endCell:
                    pathfinding(window, grid, startCell, endCell, 'dijkstra')
                elif event.key == pygame.K_c:
                    startCell, endCell = reset_grid(grid)
        startCell, endCell = handle_mouse_click(grid, startCell, endCell)
    pygame.quit()
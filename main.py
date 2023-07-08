import pygame
from constants import *
from helpers import make_grid, draw, reset_grid, handle_mouse_click
from algorithms import pathfinder, astar_priority, dijkstra_priority, greedy_priority

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")
    grid = make_grid()
    startCell = None
    endCell = None
    run = True
    while run:
        draw(window, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] < SCREEN_HEIGHT - BUTTON_HEIGHT:  # restrict cell selection to grid area
                    startCell, endCell = handle_mouse_click(grid, startCell, endCell)
                else:
                    for button in BUTTONS:
                        if button.isOver(pos):
                            for row in grid:
                                for cell in row:
                                    cell.updateNeighbours(grid)
                            if button.text == 'A*' and startCell and endCell:
                                pathfinder(lambda: draw(window, grid), grid, startCell, endCell, astar_priority)
                            elif button.text == 'Dijkstra' and startCell and endCell:
                                pathfinder(lambda: draw(window, grid), grid, startCell, endCell, dijkstra_priority)
                            elif button.text == 'Greedy' and startCell and endCell:
                                pathfinder(lambda: draw(window, grid), grid, startCell, endCell, greedy_priority)
                            elif button.text == 'Reset':
                                startCell, endCell = reset_grid(grid)
            elif event.type == pygame.MOUSEMOTION:  # added event
                if pygame.mouse.get_pressed()[0]:  # check if left button is held down
                    pos = pygame.mouse.get_pos()
                    if pos[1] < SCREEN_HEIGHT - BUTTON_HEIGHT:  # restrict cell selection to grid area
                        startCell, endCell = handle_mouse_click(grid, startCell, endCell, True)  # draw walls only
    pygame.quit()

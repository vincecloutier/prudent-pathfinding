import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from guihelpers import BUTTONS, pathfinding, make_grid, draw, reset_grid, handle_mouse_click

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
                if pos[1] < SCREEN_HEIGHT - 200:  # restrict cell selection to grid area
                    startCell, endCell = handle_mouse_click(grid, startCell, endCell)
                else:
                    for button in BUTTONS:
                        if button.isOver(pos):
                            if button.text == 'A*' and startCell and endCell:
                                pathfinding(window, grid, startCell, endCell, 'astar')
                            elif button.text == 'Dijkstra' and startCell and endCell:
                                pathfinding(window, grid, startCell, endCell, 'dijkstra')
                            elif button.text == 'Reset':
                                startCell, endCell = reset_grid(grid)
    pygame.quit()

import pygame
from queue import PriorityQueue

pygame.display.set_caption("A* Visualizer")

BLACK = (0 , 0, 0) #Wall
WHITE = (255, 255, 255) #Empty
GRAY = (128, 128, 128) #Grid Lines
RED = (255, 0 , 0) #Closed
GREEN = (0, 255, 0) #Open
ORANGE = (255, 165, 0) #Start
PURPLE = (128, 0 , 128) #End
TURQUOISE = (64, 224, 208) #Path

class Cell:
    def __init__(self, row, col, size, totalRows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbours = []
        self.size = size
        self.totalRows = totalRows

    def makeClosed(self):
        self.color = RED
    def makeOpen(self):
        self.color = GREEN
    def makeWall(self):
        self.color = BLACK
    def makeStart(self):
        self.color = ORANGE
    def makeEnd(self):
        self.color = PURPLE
    def makePath(self):
        self.color = TURQUOISE

    def isClosed(self):
        return self.color == RED
    def isOpen(self):
        return self.color == GREEN
    def isWall(self):
        return self.color == BLACK
    def isStart(self):
        return self.color == ORANGE
    def isEnd(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
    def getPos(self):
        return self.row, self.col
    def updateNeighbours(self, grid):
        self.neighbours = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall(): #DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():  #UP
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall(): #RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.row > 0 and not grid[self.row][self.col - 1].isWall(): #LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstructPath(cameFrom, current, draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    openSetHash = {start}
    cameFrom = {}

    g = {cell: float("inf") for row in grid for cell in row}
    g[start] = 0
    f = {cell: float("inf") for row in grid for cell in row}
    f[start] = h(start.getPos(), end.getPos())

    while not openSet.empty():
        current = openSet.get()[2]
        openSetHash.remove(current)
        if current == end:
            reconstructPath(cameFrom, end, draw)
            end.makeEnd()
            return True
        for neighbour in current.neighbours:
            tempG = g[current] + 1
            if tempG < g[neighbour]:
                cameFrom[neighbour] = current
                g[neighbour] = tempG
                f[neighbour] = tempG + h(neighbour.getPos(), end.getPos())
                if neighbour not in openSetHash:
                    count += 1
                    openSet.put((f[neighbour], count, neighbour))
                    openSetHash.add(neighbour)
                    neighbour.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False        

def makeGrid(rows, size):
    grid = []
    gap = size // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i , j, gap, rows)
            grid[i].append(cell)
    return grid

def draw(window, grid, rows, size):
    gap = size // rows
    window.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(window)
    for i in range(rows):
        pygame.draw.line(window, BLACK, (0, i * gap), (size, i * gap))
        for j in range(rows):
            pygame.draw.line(window, BLACK, (j * gap, 0), (j * gap, size))
    pygame.display.update()

def getClickedPosition(pos, rows, size):
    gap = size // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(window, size):

    rows = 50
    grid = makeGrid(rows, size)
    startCell = None
    endCell = None
    run = True

    while run:
        draw(window, grid, rows, size)
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, rows, size)
                cell = grid[row][col]
                if not startCell and cell != endCell:
                    startCell = cell
                    startCell.makeStart()
                elif not endCell and cell != startCell:
                    endCell = cell
                    endCell.makeEnd()
                elif cell != endCell and cell != startCell:
                    cell.makeWall()                         
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startCell and endCell:
                    for row in grid:
                        for cell in row:
                            cell.updateNeighbours(grid)
                    algorithm(lambda: draw(window, grid, rows, size), grid, startCell, endCell)
                if event.key == pygame.K_c:
                    startCell = None
                    endCell = None
                    for row in grid:
                        for cell in row:
                            cell.reset()
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

main(pygame.display.set_mode((800, 800)), 800)
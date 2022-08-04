import pygame
from queue import PriorityQueue

class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = (255, 255, 255)
        self.neighbours = []
        self.size = size
        self.totalRows = 50

    def makeClosed(self):
        self.color = (255, 0 , 0)
    def makeOpen(self):
        self.color = (0, 255, 0)
    def makeWall(self):
        self.color = (0 , 0, 0)
    def makeStart(self):
        self.color = (255, 165, 0)
    def makeEnd(self):
        self.color =  (128, 0 , 128)
    def makePath(self):
        self.color = (64, 224, 208)

    def isClosed(self):
        return self.color == (255, 0 , 0)
    def isOpen(self):
        return self.color == (0, 255, 0)
    def isWall(self):
        return self.color == (0 , 0, 0)
    def isStart(self):
        return self.color == (255, 165, 0)
    def isEnd(self):
        return self.color ==  (128, 0 , 128)

    def reset(self):
        self.color = (255, 255, 255)
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
            while end in cameFrom:
                end = cameFrom[end]
                end.makePath()
                draw()
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

def main():
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("A* Visualizer")
    grid = makeGrid()
    startCell = None
    endCell = None
    run = True
    while run:
        draw(window, grid)
        for event in pygame.event.get():
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startCell and endCell:
                    for row in grid:
                        for cell in row:
                            cell.updateNeighbours(grid)
                    algorithm(lambda: draw(window, grid), grid, startCell, endCell)
                if event.key == pygame.K_c:
                    startCell = None
                    endCell = None
                    for row in grid:
                        for cell in row:
                            cell.reset()
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

main()
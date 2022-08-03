import pygame
from queue import PriorityQueue

pygame.display.set_caption("A* Visualizer")

#Defining RGB Color Codes for our Cells
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
        self.neighbors = []
        self.size = size
        self.totalRows = totalRows

    #Gets the position of the cell
    def getPos(self):
        return self.row, self.col
    
    #Methods that check the type of cell
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

    #Methods that set/make cells 
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

    #Resets cell back to empty/white
    def reset(self):
        self.color = WHITE

    #Draws Cell
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    #Checks and updates neighboring Cells
    def update_neighbors(self, grid):
        self.neighbors = []

        #DOWN
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall():
            self.neighbors.append(grid[self.row + 1][self.col])

        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        #RIGHT
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall():
            self.neighbors.append(grid[self.row][self.col + 1])

        #LEFT
        if self.row > 0 and not grid[self.row][self.col - 1].isWall():
            self.neighbors.append(grid[self.row][self.col - 1])

    

#Defining our heuristic to calculate the distance between two points (p1 and p2)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#Reconstructs shortest path between start and end to draw
def reconstructPath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.makePath()
        draw()

#Algorithm Logic
def aStarAlgo(draw, grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    came_from = {}
    g = {cell: float("inf") for row in grid for cell in row}
    g[start] = 0
    f = {cell: float("inf") for row in grid for cell in row}
    f[start] = h(start.getPos(), end.getPos())
    openSetHash = {start}

    while not openSet.empty():
        current = openSet.get()[2]
        openSetHash.remove(current)
        if current == end:
            reconstructPath(came_from, end, draw)
            end.makeEnd()
            return True
        for neighbor in current.neighbors:
            tempG = g[current] + 1
            if tempG < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = tempG
                f[neighbor] = tempG + h(neighbor.getPos(), end.getPos())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((f[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()
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

def drawGrid(window, rows, size):
    gap = size // rows
    # Vertical lines
    for i in range(rows):
        pygame.draw.line(window, BLACK, (0, i * gap), (size, i * gap))
        # Horizontal lines
        for j in range(rows):
            pygame.draw.line(window, BLACK, (j * gap, 0), (j * gap, size))

def draw(window, grid, rows, size):
    window.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(window)
    drawGrid(window, rows, size)
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
        #Checks for different types of events that may happen
        for event in pygame.event.get():
            #Quit Event
            if event.type == pygame.QUIT:
                run = False

            #Left Mouse Click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, rows, size)
                cell = grid[row][col]

                #If Start cell does not exist, make it
                if not startCell and cell != endCell:
                    startCell = cell
                    startCell.makeStart()

                #If End cell does not exist, make it
                elif not endCell and cell != startCell:
                    endCell = cell
                    endCell.makeEnd()

                #make barrier cells
                elif cell != endCell and cell != startCell:
                    cell.makeWall()

            #if the user clicks c clear the board
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    startCell = None
                    endCell = None
                    for row in grid:
                        for cell in row:
                            cell.reset()
                            
            #SPACEBAR starts the pathfinding aStarAlgo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startCell and endCell:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    aStarAlgo(lambda: draw(window, grid, rows, size), grid, startCell, endCell)

    pygame.quit()

main(pygame.display.set_mode((800, 800)), 800)
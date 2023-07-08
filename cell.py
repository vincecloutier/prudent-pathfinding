import pygame
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

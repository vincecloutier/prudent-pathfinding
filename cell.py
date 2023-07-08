import pygame
from constants import *

class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = COLOURS['WHITE']
        self.neighbours = []
        self.size = size
        self.totalRows = GRID_COLUMNS

    def makeClosed(self):
        self.color = COLOURS['RED']
    def makeOpen(self):
        self.color = COLOURS['GREEN']
    def makeWall(self):
        self.color = COLOURS['BLACK']
    def makeStart(self):
        self.color = COLOURS['ORANGE']
    def makeEnd(self):
        self.color = COLOURS['PURPLE']
    def makePath(self):
        self.color = COLOURS['TURQUOISE']

    def isClosed(self):
        return self.color == COLOURS['RED']
    def isOpen(self):
        return self.color == COLOURS['GREEN']
    def isWall(self):
        return self.color == COLOURS['BLACK']
    def isStart(self):
        return self.color == COLOURS['ORANGE']
    def isEnd(self):
        return self.color == COLOURS['PURPLE']

    def reset(self):
        self.color = COLOURS['WHITE']
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
    def getPos(self):
        return self.row, self.col
    
    def updateNeighbours(self, grid):
        self.neighbours = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall(): #DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].isWall(): #UP
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall(): #RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].isWall(): #LEFT
            self.neighbours.append(grid[self.row][self.col - 1])
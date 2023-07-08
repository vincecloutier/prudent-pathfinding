from queue import PriorityQueue
from helpers import h

# A* algorithm
def astar(draw, grid, start, end):
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


# Dijkstra's algorithm
def dijkstra(draw, grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    openSetHash = {start}
    cameFrom = {}

    g = {cell: float("inf") for row in grid for cell in row}
    g[start] = 0

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
                if neighbour not in openSetHash:
                    count += 1
                    openSet.put((g[neighbour], count, neighbour))
                    openSetHash.add(neighbour)
                    neighbour.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False

# Breadth-first search
def bfs(draw, grid, start, end):
    queue = [start]
    visited = {start}
    cameFrom = {}

    while queue:
        current = queue.pop(0)
        if current == end:
            while end in cameFrom:
                end = cameFrom[end]
                end.makePath()
                draw()
            end.makeEnd()
            return True
        for neighbour in current.neighbours:
            if neighbour not in visited:
                cameFrom[neighbour] = current
                visited.add(neighbour)
                queue.append(neighbour)
                neighbour.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False

# Depth-first search
def dfs(draw, grid, start, end):
    stack = [start]
    visited = {start}
    cameFrom = {}

    while stack:
        current = stack.pop()
        if current == end:
            while end in cameFrom:
                end = cameFrom[end]
                end.makePath()
                draw()
            end.makeEnd()
            return True
        for neighbour in current.neighbours:
            if neighbour not in visited:
                cameFrom[neighbour] = current
                visited.add(neighbour)
                stack.append(neighbour)
                neighbour.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False


from queue import PriorityQueue

# Manhattan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# A* algorithm
def astar(draw, grid, start, end, grid_width, grid_height):
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
            x, y = neighbour.getPos()
            if x < 0 or y < 0 or x >= grid_width or y >= grid_height:
                continue
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
def dijkstra(draw, grid, start, end, grid_width, grid_height):
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
            x, y = neighbour.getPos()
            if x < 0 or y < 0 or x >= grid_width or y >= grid_height:
                continue
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

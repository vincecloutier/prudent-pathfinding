from queue import PriorityQueue

# Heuristic functions
def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Priority functions
def astar_priority(g, h, node):
    return g[node] + h[node]

def dijkstra_priority(g, _, node):
    return g[node]

def greedy_priority(_, h, node):
    return h[node]

# Pathfinder algorithm
def pathfinder(draw, grid, start, end, heuristic_fn, priority_fn):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    openSetHash = {start}
    cameFrom = {}

    g = {cell: float("inf") for row in grid for cell in row}
    g[start] = 0
    h = {cell: float("inf") for row in grid for cell in row}
    h[start] = heuristic_fn(start.getPos(), end.getPos())

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
                    h[neighbour] = heuristic_fn(neighbour.getPos(), end.getPos())
                    priority = priority_fn(g, h, neighbour)
                    openSet.put((priority, count, neighbour))
                    openSetHash.add(neighbour)
                    neighbour.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False
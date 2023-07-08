# Pathfinding Visualizer
This project is a pathfinding visualizer that demonstrates different pathfinding algorithms in a 2D grid. The pathfinding algorithms currently supported are A*, Dijkstra's, and Greedy Best-First Search. You can draw walls on the grid, place start and end nodes, and visualize how different algorithms find a path from the start to the end. The visualization grid has the size of 800x800 pixels, while the bottom 50x800 area is dedicated to control buttons.

## Interactions
Here's how to interact with the visualizer:
1. Click anywhere on the grid to create a start node (green).
2. Click again to create an end node (red).
3. After placing the start and end nodes, you can click/drag to draw walls (black).
4. Select an algorithm (A*, Dijkstra, Greedy) from the buttons at the bottom and click on it to start the visualization. The shortest path will be colored in purple.
6. Run another algorithm or click the 'Reset' button to clear the grid and start with a new map.

## Changing the Behaviour of the Pathfinder
The 'plug-in' nature of this pathfinder allows you to easily include additional priority functions or heuristic functions to emulate other algorithms. Depending on these functions, you can make the algorithm behave differently, leading to a range of pathfinding algorithms like A*, Dijkstra's, Greedy Best-First Search and more. Here's how you can add a new ones:

### Create Your Own Priority Function
Priority functions are used to determine the order of exploration of the cells. <br>
In the file where the existing priority functions are defined (`algorithms.py`), define a new function. This function should take three arguments:
- `g`: a dictionary mapping each `Cell` object in the grid to its current shortest known distance from the start cell.
- `h`: a dictionary mapping each `Cell` object in the grid to its heuristic distance from the end cell.
- `node`: the `Cell` object that you're computing the priority for.
Your function should return a number that represents the priority of the node. Lower priorities will be explored before higher priorities.

Here's a sample of a somewhat unusual priority function:
```
def unusual_priority(g, h, node):
    return g[node] * h[node]
```
This priority function could lead to interesting behavior because it multiplies the shortest known distance from the start cell by the heuristic distance from the end cell.

### Create Your Own Heuristic Function
Heuristic functions provide an estimate of the distance from a given cell to the target cell. <br>
In the file where the existing priority functions are defined (`algorithms.py`), define a new function. This function should take three arguments:
- `p1`: a tuple representing the (x, y) coordinates of the first cell.
- `p2`: a tuple representing the (x, y) coordinates of the second cell.
Your function should return a number that represents the estimated distance from p1 to p2. <br>

Remember that the success of these functions might depend heavily on the nature of the grid and the start/end points. <br>

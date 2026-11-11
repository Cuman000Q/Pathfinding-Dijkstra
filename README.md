# Pathfinding & Grid Agents with Dijkstra's Algorithm

Three small Python projects that build up from one idea: **agents moving on a grid**.
It starts with a plain implementation of Dijkstra's shortest-path algorithm, then a grid
where players hunt each other, and ends with agents that use Dijkstra to find the
cheapest route to a target.

Everything is written from scratch with object-oriented Python, with no external libraries.

| File | What it does |
|------|--------------|
| [`dijkstra_basic.py`](dijkstra_basic.py) | Dijkstra's algorithm on a small weighted graph |
| [`grid_chase.py`](grid_chase.py) | Players chase the closest opponent on a grid until one survives |
| [`grid_dijkstra.py`](grid_dijkstra.py) | Agents use Dijkstra to walk to a random target on a free grid |

## Requirements

- Python 3.8 or newer: only the standard library is used

```bash
git clone https://github.com/Cuman000Q/pathfinding-dijkstra.git
cd pathfinding-dijkstra
```

---

## 1. Dijkstra's algorithm: `dijkstra_basic.py`

Finds the cheapest path between two nodes of a weighted, directed graph.

```bash
python dijkstra_basic.py
```

The example network (directed edges with their costs):

```
A → B  (5)
A → C  (1)
C → B  (1)
B → D  (2)
C → D  (7)
```

```
Cheapest path: A -> C -> B -> D
Total cost: 4
```

The direct-looking routes (`A → B → D` = 7, `A → C → D` = 8) are more expensive than going
through both `C` and `B`.

**How it works**
- Each `Node` stores its best known cost `g` (starting at infinity) and a link to the
  `parent_node` it was reached from.
- The start node gets cost `0`. The algorithm repeatedly takes the cheapest unprocessed
  node, and updates each neighbour if the path through the current node is cheaper.
- When the target is reached, the path is rebuilt by following the `parent_node` links back
  to the start.

## 2. Grid chase: `grid_chase.py`

Three players are placed on an 8×8 grid. Every tick, each player finds the **closest
living player** and moves one step towards it (horizontally, vertically or diagonally).
A player that starts its turn next to its target, including diagonally, eliminates it.
The last player standing wins.

```bash
python grid_chase.py
```

```
--- Start ---
Z . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . L . . .
. . . . . . . .
. . . . . . A .
. . . . . . . .

--- Tick 1 ---
Leo eliminated Alen
Alen has been removed
. . . . . . . .
. Z . . . . . .
...

The winner is: Zhan
```

## 3. Grid agents with Dijkstra: `grid_dijkstra.py`

A 10×8 grid with a random target `X` and three agents at random positions. Every tick,
each agent builds a graph of the grid, runs Dijkstra from its own cell to the target and
takes **one step** along the cheapest path. Straight steps cost `1`, diagonal steps
cost `1.414` (≈ √2). The first agent to reach `X` wins.

```bash
python grid_dijkstra.py
```

```
Target X at (5, 2)
Agent_0 starts at (6, 0)
Agent_1 starts at (1, 1)
Agent_2 starts at (5, 0)

--- Start ---
. . . . . 2 0 . . .
. 1 . . . . . . . .
. . . . . X . . . .
...
```

You can change the size of the world and the number of agents at the bottom of the file:

```python
world=FGW(width=10, height=8, agent_nums=3)
world.run(delay=0.5)   # seconds between ticks
```

## Ideas for next steps

- [ ] Add walls and obstacles to the grid, so the paths actually have to go around something
- [ ] Use a priority queue (`heapq`) instead of sorting the list on every step
- [ ] Implement A* (Dijkstra + a distance heuristic) and compare the speed
- [ ] Combine both games: agents that use Dijkstra to chase each other

## Author

Made by [Cuman000Q](https://github.com/Cuman000Q).

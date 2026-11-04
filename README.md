# Smart Traffic Navigation System - A* Search

This project demonstrates route planning with the **A\*** search algorithm.
It models intersections as nodes in a weighted, bidirectional graph and roads
as edges with travel costs. A\* searches for a route from a chosen start
location to a destination while using heuristic estimates to guide the search.

At each step, the algorithm prioritizes the node with the lowest estimated
total route cost:

```text
f(n) = g(n) + h(n)
```

- `g(n)` is the actual cost from the start to node `n`.
- `h(n)` is the estimated remaining cost from `n` to the destination.
- `f(n)` is the estimated total cost of a route through `n`.

The project is an offline simulation. Road costs are example values and are
not obtained from live traffic, maps, or location services.

## Requirements

- Python 3
- Tkinter for the graphical interface (usually included with desktop Python)
- Optional: `networkx` and `matplotlib` for the static graph visualization

The A\* algorithm and command-line programs use only Python's standard library.
There is no dependency manifest in the repository. To use the optional
visualization:

```powershell
python -m pip install networkx matplotlib
```

## Run the A* project

Run commands from the repository root:

```powershell
# Command-line route search using the built-in road network
python ".\A_Star Approch\main.py"

# GUI route planner with road blocking and reset controls
python ".\A_Star Approch\ui.py"

# Enter a custom graph and heuristic estimates interactively
python ".\A_Star Approch\user_input.py"

# Optional static drawing of the built-in road network
python ".\A_Star Approch\visualize.py"
```

## Built-in road network

The default network, defined in `A_Star Approch/road_network.py`, contains:

| Road | Cost |
|---|---:|
| Home <-> Signal | 3 |
| Home <-> Flyover | 4 |
| Signal <-> Office | 6 |
| Flyover <-> Office | 2 |

For the default search from `Home` to `Office`, A\* finds
`Home -> Flyover -> Office`, with a total cost of `6`. The command-line program
prints the search steps, including the selected node, `g(n)`, `h(n)`, `f(n)`,
and current path.

The Tkinter GUI displays the road network, lets you select a start and
destination, and highlights the route it finds. You can block an open road and
search again, or use **Reset Roads** to restore the original network. Blocking
roads changes only the local simulation; it does not represent live road
conditions.

## Create a custom graph

Run `python ".\A_Star Approch\user_input.py"` and enter:

1. The number of locations and a unique name for each one.
2. The number of roads, each road's endpoints, and its travel cost.
3. A start location and destination.
4. A non-negative heuristic estimate for each location.

The destination's heuristic is set to zero. Roads entered by the graph-input
program are bidirectional. To guarantee a minimum-cost route, heuristic values
should not overestimate the true remaining cost. The implementation uses a
closed set, so a consistent heuristic is suitable.

## Project structure

```text
A_Star Approch/
|-- astar.py          # A* search implementation
|-- main.py           # CLI using the built-in road network
|-- user_input.py     # CLI for entering a graph and heuristic
|-- ui.py             # Tkinter route-planning GUI
|-- road_network.py   # Built-in roads, heuristic, graph builder
|-- graph_input.py    # Interactive weighted-graph input
|-- traffic_rules.py  # Helper to block a road in a road list
|-- visualize.py      # Optional NetworkX/Matplotlib graph drawing
|-- test_cases.py     # A* route and traffic-rule tests
`-- test_rules.py     # A* road-network tests
```

## Tests

Run the A\* tests with:

```powershell
python -m unittest discover -s "A_Star Approch" -p "test_*.py"
```

**Current limitation:** test discovery currently fails because both A\* test
modules import `update_road_cost` from `traffic_rules.py`, but the module
currently provides `block_road` instead.

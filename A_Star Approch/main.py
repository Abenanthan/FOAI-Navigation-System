from astar import astar
from road_network import ROAD_RULES, HEURISTIC, build_graph

graph = build_graph(ROAD_RULES)

print("Smart Traffic Navigation System")
print("Available Locations:", list(graph.keys()))

start = input("Enter Start Location: ").strip()
goal = input("Enter Destination: ").strip()

if start not in graph or goal not in graph:
    print("Invalid location!")
else:
    status, cost, path, visited = astar(
        graph, start, goal, HEURISTIC
    )

    print("\nStatus:", status)

    if path:
        print("Route:", " -> ".join(path))
        print("Total Travel Cost:", cost)
        print("Visited Nodes:", visited)
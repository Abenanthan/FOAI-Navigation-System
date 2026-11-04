
from graph_input import read_graph
from ucs import ucs

graph = read_graph()

print("\nAvailable Locations:", list(graph.keys()))

start = input("Enter Start Location: ").strip()
goal = input("Enter Destination: ").strip()

if start not in graph or goal not in graph:
    print("Invalid location!")
else:
    status, cost, path = ucs(graph, start, goal)

    print("\nStatus:", status)

    if path:
        print("Route:", " -> ".join(path))
        print("Total Travel Cost:", cost)
    else:
        print("No route found.")

from graph_input import read_graph
from astar import astar

graph = read_graph()

print("\nAvailable Locations:", list(graph.keys()))

start = input("Enter Start Location: ").strip()
goal = input("Enter Destination: ").strip()

if start not in graph or goal not in graph:
    print("Invalid location!")

else:
    heuristic = {}

    print("\nEnter estimated cost to the destination.")
    print("Heuristic for the destination must be 0.")

    for node in graph:
        if node == goal:
            heuristic[node] = 0
        else:
            while True:
                try:
                    value = float(
                        input(f"Heuristic for {node}: ")
                    )

                    if value < 0:
                        print("Heuristic cannot be negative.")
                        continue

                    heuristic[node] = value
                    break

                except ValueError:
                    print("Enter a valid number.")

    status, cost, path, explored = astar(
        graph, start, goal, heuristic
    )

    print("\n--- Final Result ---")
    print("Status:", status)

    if path:
        print("Route:", " -> ".join(path))
        print("Total Travel Cost:", cost)
    else:
        print("No route found.")

    print("Exploration Order:", explored)

import heapq

def astar(graph, start, goal, heuristic):

    if start not in graph:
        return "Start node not found", None, [], []

    if goal not in graph:
        return "Goal node not found", None, [], []
    
    pq = []
    #heapq.heappush(queue, (f(n), g(n), node, path))
    heapq.heappush(pq, (heuristic[start], 0, start, [start]))

    visited = set()
    step = 0
    #Counts how many nodees have been removed
    
    while pq:
        f, cost, node, path = heapq.heappop(pq)
        step += 1

        print("\nStep", step)
        print("Selected Node:", node)
        print("Actual Cost g(n):", cost)
        print("Heuristic h(n):", heuristic[node])
        print("Total Cost f(n):", f)
        print("Current Path:", " -> ".join(path))

        if node == goal:
            print("Goal Found!")
            return "Goal Found", cost, path, list(visited)

        if node not in visited:
            visited.add(node)
            print("Visited Nodes:", visited)

            for neighbor, edge_cost in graph[node]:
                if neighbor not in visited:
                    new_cost = cost + edge_cost
                    new_f = new_cost + heuristic[neighbor]

                    print("Adding:", neighbor)
                    print("  g(n) =", new_cost)
                    print("  h(n) =", heuristic[neighbor])
                    print("  f(n) =", new_f)

                    heapq.heappush(
                        pq,
                        (new_f, new_cost, neighbor, path + [neighbor])
                    )

    return "Goal Not Found", None, [], list(visited)
    #returns the status, cost, path, and visited nodes
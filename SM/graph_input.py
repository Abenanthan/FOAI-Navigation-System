
def read_graph():
    graph = {}

    n = int(input("Enter number of locations: "))

    for i in range(n):
        node = input(f"Enter location {i + 1}: ").strip()

        while not node or node in graph:
            print("Location must be non-empty and unique.")
            node = input(f"Enter location {i + 1}: ").strip()

        graph[node] = []

    roads = int(input("Enter number of roads: "))

    for i in range(roads):
        print(f"\nRoad {i + 1}")

        while True:
            start = input("From: ").strip()
            end = input("To: ").strip()

            if start not in graph or end not in graph:
                print("Enter locations defined in the graph.")
                continue

            try:
                cost = float(input("Cost: "))
                if cost < 0:
                    print("Cost cannot be negative.")
                    continue
                if cost.is_integer():
                    cost = int(cost)
                break
            except ValueError:
                print("Enter a valid cost.")

        graph[start].append((end, cost))
        graph[end].append((start, cost))

    return graph
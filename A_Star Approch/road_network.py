"""Staff-specification road network and graph helpers."""

ROAD_RULES = [
    ("Home", "Signal", 3),
    ("Home", "Flyover", 4),
    ("Signal", "Office", 6),
    ("Flyover", "Office", 2),
]

# Example estimates of remaining cost to Office.
# These are illustrative values; replace them with suitable estimates
# if your staff provides a specific heuristic.
HEURISTIC = {
    "Home": 5,
    "Signal": 5,
    "Flyover": 2,
    "Office": 0,
}


def build_graph(road_rules):
    """Build an undirected weighted graph from (start, end, cost) rules."""
    graph = {}
    for start, end, cost in road_rules:
        if cost < 0:
            raise ValueError("Road costs must be non-negative.")
        graph.setdefault(start, [])
        graph.setdefault(end, [])
        graph[start].append((end, cost))
        graph[end].append((start, cost))
    return graph

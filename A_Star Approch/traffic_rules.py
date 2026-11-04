def block_road(road_rules, start, end):
    """Return a new road list with the selected bidirectional road removed."""
    updated = []
    found = False
    for a, b, cost in road_rules:
        if (a == start and b == end) or (a == end and b == start):
            found = True
        else:
            updated.append((a, b, cost))
    if not found:
        raise ValueError(f"Road between {start} and {end} was not found.")
    return updated

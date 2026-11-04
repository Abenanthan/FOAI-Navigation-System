"""Optional graph visualization using networkx and matplotlib.

Install dependencies from requirements.txt, then run:
    python visualize.py
"""
import matplotlib.pyplot as plt
import networkx as nx

from road_network import ROAD_RULES


def main():
    graph = nx.Graph()
    for start, end, cost in ROAD_RULES:
        graph.add_edge(start, end, weight=cost)

    positions = nx.spring_layout(graph, seed=7)
    nx.draw_networkx_nodes(graph, positions, node_size=1800)
    nx.draw_networkx_labels(graph, positions, font_size=10)
    nx.draw_networkx_edges(graph, positions, width=2)
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels)
    plt.title("Smart Traffic Navigation System — Road Costs")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

import unittest

from astar import astar
from road_network import ROAD_RULES, HEURISTIC, build_graph
from traffic_rules import update_road_cost


class AStarTests(unittest.TestCase):
    def test_staff_sample_best_route(self):
        graph = build_graph(ROAD_RULES)
        status, cost, path, _ = astar(graph, "Home", "Office", HEURISTIC)
        self.assertEqual(status, "Goal Found")
        self.assertEqual(cost, 6)
        self.assertEqual(path, ["Home", "Flyover", "Office"])

    def test_start_equals_goal(self):
        graph = build_graph(ROAD_RULES)
        status, cost, path, _ = astar(graph, "Home", "Home", HEURISTIC)
        self.assertEqual(status, "Goal Found")
        self.assertEqual(cost, 0)
        self.assertEqual(path, ["Home"])

    def test_invalid_start(self):
        graph = build_graph(ROAD_RULES)
        status, cost, path, _ = astar(graph, "Unknown", "Office", HEURISTIC)
        self.assertEqual(status, "Start node not found")
        self.assertIsNone(cost)
        self.assertEqual(path, [])

    def test_disconnected_graph(self):
        graph = {"A": [("B", 2)], "B": [("A", 2)],
                 "C": [("D", 1)], "D": [("C", 1)]}
        status, cost, path, _ = astar(graph, "A", "D", {"A": 0, "B": 0, "C": 0, "D": 0})
        self.assertEqual(status, "Goal Not Found")
        self.assertIsNone(cost)
        self.assertEqual(path, [])

    def test_traffic_update_changes_best_route(self):
        # Increase Home-Flyover cost; the alternative route should become cheaper.
        roads = update_road_cost(ROAD_RULES, "Home", "Flyover", 10)
        graph = build_graph(roads)
        zero_heuristic = {node: 0 for node in graph}
        status, cost, path, _ = astar(graph, "Home", "Office", zero_heuristic)
        self.assertEqual(status, "Goal Found")
        self.assertEqual(cost, 9)
        self.assertEqual(path, ["Home", "Signal", "Office"])

    def test_traffic_update_unknown_road(self):
        with self.assertRaises(ValueError):
            update_road_cost(ROAD_RULES, "Home", "Airport", 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)

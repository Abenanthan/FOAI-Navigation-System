
import unittest

from road_network import ROAD_RULES, HEURISTIC, build_graph
from traffic_rules import update_road_cost


class TestRoadRules(unittest.TestCase):

    def setUp(self):
        self.graph = build_graph(ROAD_RULES)

    def test_graph_contains_all_locations(self):
        self.assertEqual(
            set(self.graph.keys()),
            {"Home", "Signal", "Flyover", "Office"}
        )

    def test_roads_are_bidirectional(self):
        self.assertIn(("Signal", 3), self.graph["Home"])
        self.assertIn(("Home", 3), self.graph["Signal"])

    def test_road_costs_are_correct(self):
        self.assertIn(("Flyover", 4), self.graph["Home"])
        self.assertIn(("Office", 2), self.graph["Flyover"])

    def test_heuristic_values_exist(self):
        for node in self.graph:
            self.assertIn(node, HEURISTIC)

        self.assertEqual(HEURISTIC["Office"], 0)

    def test_traffic_cost_update(self):
        updated_roads = update_road_cost(
            ROAD_RULES, "Home", "Flyover", 10
        )
        updated_graph = build_graph(updated_roads)

        self.assertIn(("Flyover", 10), updated_graph["Home"])
        self.assertIn(("Home", 10), updated_graph["Flyover"])

    def test_invalid_road_update(self):
        with self.assertRaises(ValueError):
            update_road_cost(
                ROAD_RULES, "Home", "Airport", 5
            )

    def test_negative_traffic_cost(self):
        with self.assertRaises(ValueError):
            update_road_cost(
                ROAD_RULES, "Home", "Flyover", -5
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
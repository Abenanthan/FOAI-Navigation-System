import tkinter as tk
from tkinter import ttk, messagebox

from astar import astar
from road_network import ROAD_RULES, HEURISTIC, build_graph


class TrafficNavigationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Traffic Navigation System — A*")
        self.root.geometry("900x620")
        self.root.minsize(780, 540)

        self.roads = list(ROAD_RULES)
        self.graph = build_graph(self.roads)
        self.heuristic = dict(HEURISTIC)

        self.start_var = tk.StringVar(value="Home")
        self.goal_var = tk.StringVar(value="Office")
        self.status_var = tk.StringVar(value="Choose a start and destination, then find a route.")
        self.route_var = tk.StringVar(value="Route: —")
        self.cost_var = tk.StringVar(value="Total travel cost: —")

        self._build_ui()
        self._draw_graph()

    def _build_ui(self):
        header = ttk.Frame(self.root, padding=(16, 14))
        header.pack(fill="x")
        ttk.Label(header, text="Smart Traffic Navigation System",
                  font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(header, text="A* Search • Road blocking and route recalculation",
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))

        controls = ttk.LabelFrame(self.root, text="Route planning", padding=12)
        controls.pack(fill="x", padx=16, pady=(0, 10))

        ttk.Label(controls, text="Start").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.start_box = ttk.Combobox(controls, textvariable=self.start_var, state="readonly", width=18)
        self.start_box.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=(4, 0))

        ttk.Label(controls, text="Destination").grid(row=0, column=1, sticky="w", padx=(0, 6))
        self.goal_box = ttk.Combobox(controls, textvariable=self.goal_var, state="readonly", width=18)
        self.goal_box.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=(4, 0))

        ttk.Button(controls, text="Find Route", command=self.find_route).grid(
            row=1, column=2, padx=(0, 8), pady=(4, 0))
        ttk.Button(controls, text="Block Road", command=self.block_road_dialog).grid(
            row=1, column=3, pady=(4, 0))
        ttk.Button(controls, text="Reset Roads", command=self.reset_roads).grid(
            row=1, column=4, padx=(8, 0), pady=(4, 0))

        self._refresh_locations()

        content = ttk.Frame(self.root, padding=(16, 0, 16, 10))
        content.pack(fill="both", expand=True)
        graph_frame = ttk.LabelFrame(content, text="Road network", padding=8)
        graph_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.canvas = tk.Canvas(graph_frame, background="white", height=360,
                                highlightthickness=1, highlightbackground="#d1d5db")
        self.canvas.pack(fill="both", expand=True)

        result_frame = ttk.LabelFrame(content, text="Route result", padding=12, width=240)
        result_frame.pack(side="right", fill="y")
        result_frame.pack_propagate(False)
        ttk.Label(result_frame, textvariable=self.status_var, wraplength=205).pack(
            anchor="w", pady=(0, 14))
        ttk.Label(result_frame, textvariable=self.route_var, wraplength=205,
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 12))
        ttk.Label(result_frame, textvariable=self.cost_var, wraplength=205).pack(anchor="w")
        ttk.Separator(result_frame).pack(fill="x", pady=14)
        ttk.Label(result_frame, text="Road status", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.road_list = tk.Listbox(result_frame, height=9, activestyle="none")
        self.road_list.pack(fill="x", pady=(6, 0))
        self._refresh_road_list()

        ttk.Label(self.root,
                  text="Blocked roads are removed from the graph. This is a simulation, not live road data.",
                  padding=(16, 5)).pack(fill="x")

    def _refresh_locations(self):
        locations = sorted(self.graph.keys())
        self.start_box["values"] = locations
        self.goal_box["values"] = locations
        if self.start_var.get() not in locations:
            self.start_var.set(locations[0] if locations else "")
        if self.goal_var.get() not in locations:
            self.goal_var.set(locations[-1] if locations else "")

    def _refresh_road_list(self):
        self.road_list.delete(0, tk.END)
        active = {frozenset((a, b)) for a, b, _ in self.roads}
        for a, b, cost in ROAD_RULES:
            if frozenset((a, b)) in active:
                self.road_list.insert(tk.END, f"OPEN  {a} ↔ {b} (cost {cost})")
            else:
                self.road_list.insert(tk.END, f"BLOCKED  {a} ↔ {b}")

    def _positions(self):
        return {"Home": (0.12, 0.50), "Signal": (0.42, 0.20),
                "Flyover": (0.42, 0.80), "Office": (0.82, 0.50)}

    def _draw_graph(self, route=None):
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 500)
        height = max(self.canvas.winfo_height(), 300)
        points = {n: (int(x * width), int(y * height))
                  for n, (x, y) in self._positions().items()}
        route_edges = set()
        if route:
            for i in range(len(route) - 1):
                route_edges.add(frozenset((route[i], route[i + 1])))
        active = {frozenset((a, b)) for a, b, _ in self.roads}

        for a, b, cost in ROAD_RULES:
            x1, y1 = points[a]
            x2, y2 = points[b]
            edge = frozenset((a, b))
            if edge in active:
                selected = edge in route_edges
                self.canvas.create_line(x1, y1, x2, y2,
                    fill="#dc2626" if selected else "#9ca3af",
                    width=4 if selected else 2)
                mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                self.canvas.create_rectangle(mx - 18, my - 12, mx + 18, my + 12,
                                             fill="white", outline="")
                self.canvas.create_text(mx, my, text=str(cost), fill="#111827",
                                        font=("Segoe UI", 10, "bold"))
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill="#d1d5db",
                                        width=2, dash=(5, 4))
                mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                self.canvas.create_text(mx, my, text="X", fill="#dc2626",
                                        font=("Segoe UI", 12, "bold"))

        for node, (x, y) in points.items():
            r = 27
            selected = route and node in route
            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                fill="#fee2e2" if selected else "#dbeafe",
                outline="#dc2626" if selected else "#2563eb", width=2)
            self.canvas.create_text(x, y, text=node, fill="#111827",
                                    font=("Segoe UI", 9, "bold"))

    def find_route(self):
        self.graph = build_graph(self.roads)
        status, cost, path, explored = astar(
            self.graph, self.start_var.get(), self.goal_var.get(), self.heuristic)
        self.status_var.set(status + (". Explored: " + ", ".join(explored) if explored else ""))
        if path:
            self.route_var.set("Route: " + " → ".join(path))
            self.cost_var.set(f"Total travel cost: {cost}")
            self._draw_graph(path)
        else:
            self.route_var.set("Route: unavailable")
            self.cost_var.set("Total travel cost: —")
            self._draw_graph()

    def block_road_dialog(self):
        if not self.roads:
            messagebox.showinfo("No open roads", "All roads are already blocked.")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Block a road")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select a road to block").grid(
            row=0, column=0, padx=12, pady=(12, 4), sticky="w")
        options = [f"{a} ↔ {b} (cost {cost})" for a, b, cost in self.roads]
        road_var = tk.StringVar(value=options[0])
        road_box = ttk.Combobox(dialog, textvariable=road_var, values=options,
                                state="readonly", width=30)
        road_box.grid(row=1, column=0, padx=12, sticky="w")

        def apply_block():
            index = road_box.current()
            if index < 0:
                return
            a, b, _ = self.roads[index]
            self.roads = [road for road in self.roads
                          if not ((road[0] == a and road[1] == b) or
                                  (road[0] == b and road[1] == a))]
            self.graph = build_graph(self.roads)
            self._refresh_road_list()
            self._draw_graph()
            self.route_var.set("Route: —")
            self.cost_var.set("Total travel cost: —")
            self.status_var.set(f"Road {a} ↔ {b} blocked. Click Find Route to recalculate.")
            dialog.destroy()

        ttk.Button(dialog, text="Block Road", command=apply_block).grid(
            row=2, column=0, padx=12, pady=12, sticky="w")

    def reset_roads(self):
        self.roads = list(ROAD_RULES)
        self.graph = build_graph(self.roads)
        self._refresh_locations()
        self._refresh_road_list()
        self._draw_graph()
        self.route_var.set("Route: —")
        self.cost_var.set("Total travel cost: —")
        self.status_var.set("Road network reset. Click Find Route to search again.")


def main():
    root = tk.Tk()
    TrafficNavigationUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import math
from itertools import count


class TrafficNavigationUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Traffic Navigation System")
        self.root.geometry("1150x700")

        self.locations = []
        self.graph = {}
        self.original_graph = {}
        self.heuristics = {}
        self.positions = {}

        self.location_entries = []
        self.road_entries = []
        self.heuristic_entries = []

        self.create_interface()

    def create_interface(self):

        # Scrollable container
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)

        self.scroll_canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            outer, orient="vertical", command=self.scroll_canvas.yview
        )
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        self.main = ttk.Frame(self.scroll_canvas)
        window_id = self.scroll_canvas.create_window(
            (0, 0), window=self.main, anchor="nw"
        )

        # Keep scroll region and width in sync
        self.main.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")
            )
        )
        self.scroll_canvas.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.itemconfig(window_id, width=e.width)
        )

        # Mouse wheel (Windows/macOS and Linux)
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)
        self.root.bind_all(
            "<Button-4>",
            lambda e: self.scroll_canvas.yview_scroll(-1, "units")
        )
        self.root.bind_all(
            "<Button-5>",
            lambda e: self.scroll_canvas.yview_scroll(1, "units")
        )

        # Number of locations
        top = ttk.LabelFrame(
            self.main, text="1. Location Configuration", padding=10
        )
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Number of locations:").grid(
            row=0, column=0
        )

        self.location_count = ttk.Entry(top, width=10)
        self.location_count.grid(row=0, column=1, padx=5)

        ttk.Button(
            top,
            text="Set Locations",
            command=self.create_location_inputs
        ).grid(row=0, column=2, padx=5)

        self.location_frame = ttk.LabelFrame(
            self.main, text="Enter Location Names", padding=10
        )
        self.location_frame.pack(fill="x", padx=10, pady=5)

        # Road inputs
        self.road_frame = ttk.LabelFrame(
            self.main, text="2. Road Configuration", padding=10
        )
        self.road_frame.pack(fill="x", padx=10, pady=5)

        # Heuristic inputs
        self.heuristic_frame = ttk.LabelFrame(
            self.main, text="3. Heuristic Values", padding=10
        )
        self.heuristic_frame.pack(fill="x", padx=10, pady=5)

        # Route selection
        self.route_frame = ttk.LabelFrame(
            self.main, text="4. Route Selection", padding=10
        )
        self.route_frame.pack(fill="x", padx=10, pady=5)

        self.canvas_frame = ttk.LabelFrame(
            self.main, text="Road Network Graph", padding=5
        )
        self.canvas_frame.pack(
            fill="both", expand=True, padx=10, pady=5
        )

        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="white",
            height=380
        )
        self.canvas.pack(fill="both", expand=True)

        self.result_label = ttk.Label(
            self.main,
            text="Enter graph details to begin.",
            font=("Arial", 11)
        )
        self.result_label.pack(pady=10)

    def on_mousewheel(self, event):
        # Windows: delta is +/-120, macOS: small ints
        step = -1 if event.delta > 0 else 1
        self.scroll_canvas.yview_scroll(step, "units")

    # STEP 1: Create location inputs

    def create_location_inputs(self):

        try:
            n = int(self.location_count.get())

            if n < 2:
                raise ValueError("Enter at least 2 locations.")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Enter a valid number of locations (minimum 2)."
            )
            return

        for widget in self.location_frame.winfo_children():
            widget.destroy()

        self.location_entries = []

        for i in range(n):

            ttk.Label(
                self.location_frame,
                text=f"Location {i + 1}:"
            ).grid(row=i, column=0, padx=5, pady=3)

            entry = ttk.Entry(self.location_frame, width=25)
            entry.grid(row=i, column=1, padx=5, pady=3)

            self.location_entries.append(entry)

        ttk.Button(
            self.location_frame,
            text="Continue to Road Configuration",
            command=self.create_road_inputs
        ).grid(row=n, column=1, pady=8)

        self.clear_later_sections()

    def clear_later_sections(self):

        for frame in [
            self.road_frame,
            self.heuristic_frame,
            self.route_frame
        ]:
            for widget in frame.winfo_children():
                widget.destroy()

        self.canvas.delete("all")
        self.result_label.config(text="")

    # STEP 2: Create road inputs

    def create_road_inputs(self):

        names = [
            entry.get().strip()
            for entry in self.location_entries
        ]

        if any(not name for name in names):
            messagebox.showerror(
                "Input Error", "Enter all location names."
            )
            return

        if len(set(names)) != len(names):
            messagebox.showerror(
                "Input Error", "Location names must be unique."
            )
            return

        self.locations = names

        for widget in self.road_frame.winfo_children():
            widget.destroy()

        self.road_entries = []

        ttk.Label(
            self.road_frame,
            text="Number of roads:"
        ).grid(row=0, column=0)

        self.road_count = ttk.Entry(
            self.road_frame, width=10
        )
        self.road_count.grid(row=0, column=1, padx=5)

        ttk.Button(
            self.road_frame,
            text="Set Roads",
            command=self.create_road_fields
        ).grid(row=0, column=2, padx=5)

    def create_road_fields(self):

        try:
            n = int(self.road_count.get())

            if n < 1:
                raise ValueError()

        except ValueError:
            messagebox.showerror(
                "Input Error", "Enter a valid number of roads."
            )
            return

        for widget in self.road_frame.winfo_children():
            if int(widget.grid_info().get("row", 0)) > 0:
                widget.destroy()

        self.road_entries = []

        headers = ["Road", "From", "To", "Travel Cost"]

        for col, header in enumerate(headers):
            ttk.Label(
                self.road_frame,
                text=header
            ).grid(row=1, column=col, padx=5)

        for i in range(n):

            ttk.Label(
                self.road_frame,
                text=f"Road {i + 1}"
            ).grid(row=i + 2, column=0, padx=5, pady=3)

            start = ttk.Combobox(
                self.road_frame,
                values=self.locations,
                state="readonly",
                width=18
            )
            start.grid(row=i + 2, column=1, padx=5)

            end = ttk.Combobox(
                self.road_frame,
                values=self.locations,
                state="readonly",
                width=18
            )
            end.grid(row=i + 2, column=2, padx=5)

            cost = ttk.Entry(
                self.road_frame, width=12
            )
            cost.grid(row=i + 2, column=3, padx=5)

            self.road_entries.append((start, end, cost))

        ttk.Button(
            self.road_frame,
            text="Continue to Heuristic Values",
            command=self.create_heuristic_inputs
        ).grid(row=n + 2, column=1, columnspan=2, pady=8)

    # STEP 3: Heuristic values

    def create_heuristic_inputs(self):

        for widget in self.heuristic_frame.winfo_children():
            widget.destroy()

        self.heuristic_entries = []

        ttk.Label(
            self.heuristic_frame,
            text="Enter estimated cost from each location to the destination:"
        ).grid(row=0, column=0, columnspan=2, pady=5)

        for i, location in enumerate(self.locations):

            ttk.Label(
                self.heuristic_frame,
                text=f"h({location}):"
            ).grid(row=i + 1, column=0, padx=5, pady=3)

            entry = ttk.Entry(
                self.heuristic_frame, width=15
            )
            entry.grid(row=i + 1, column=1, padx=5, pady=3)

            self.heuristic_entries.append(entry)

        ttk.Button(
            self.heuristic_frame,
            text="Generate Graph",
            command=self.generate_graph
        ).grid(
            row=len(self.locations) + 1,
            column=1,
            pady=8
        )

    # STEP 4: Build graph

    def generate_graph(self):

        graph = {
            location: {} for location in self.locations
        }

        try:
            for start_box, end_box, cost_entry in self.road_entries:

                start = start_box.get()
                end = end_box.get()
                cost = float(cost_entry.get())

                if not start or not end:
                    raise ValueError("Select both road endpoints.")

                if start == end or cost < 0:
                    raise ValueError("Invalid road or travel cost.")

                if end in graph[start]:
                    raise ValueError(
                        f"Duplicate road: {start} - {end}"
                    )

                # Bidirectional roads
                graph[start][end] = cost
                graph[end][start] = cost

            heuristics = {}

            for location, entry in zip(
                self.locations, self.heuristic_entries
            ):
                value = float(entry.get())

                if value < 0:
                    raise ValueError(
                        "Heuristic values cannot be negative."
                    )

                heuristics[location] = value

            self.graph = graph
            self.original_graph = {
                node: neighbours.copy()
                for node, neighbours in graph.items()
            }

            self.heuristics = heuristics

            self.create_route_controls()
            self.draw_graph()

            self.result_label.config(
                text="Graph generated successfully."
            )

        except ValueError as error:
            messagebox.showerror(
                "Input Error", str(error)
            )

    # STEP 5: Source and destination

    def create_route_controls(self):

        for widget in self.route_frame.winfo_children():
            widget.destroy()

        ttk.Label(
            self.route_frame, text="Start:"
        ).grid(row=0, column=0)

        self.source_box = ttk.Combobox(
            self.route_frame,
            values=self.locations,
            state="readonly",
            width=15
        )
        self.source_box.grid(row=0, column=1, padx=5)
        self.source_box.set(self.locations[0])

        ttk.Label(
            self.route_frame, text="Destination:"
        ).grid(row=0, column=2)

        self.destination_box = ttk.Combobox(
            self.route_frame,
            values=self.locations,
            state="readonly",
            width=15
        )
        self.destination_box.grid(row=0, column=3, padx=5)
        self.destination_box.set(self.locations[-1])

        ttk.Button(
            self.route_frame,
            text="Find Route",
            command=self.find_route
        ).grid(row=0, column=4, padx=8)

        ttk.Label(
            self.route_frame,
            text="Block Road:"
        ).grid(row=1, column=0, pady=8)

        self.block_box = ttk.Combobox(
            self.route_frame,
            state="readonly",
            width=25
        )
        self.block_box.grid(
            row=1, column=1, columnspan=2, padx=5
        )

        ttk.Button(
            self.route_frame,
            text="Block Selected Road",
            command=self.block_road
        ).grid(row=1, column=3, padx=5)

        ttk.Button(
            self.route_frame,
            text="Reset Graph",
            command=self.reset_graph
        ).grid(row=1, column=4, padx=5)

        self.update_block_options()

    # STEP 6: A* algorithm

    def astar(self, start, goal):

        if start not in self.graph or goal not in self.graph:
            return None, 0, []

        if start == goal:
            return [start], 0, [start]

        sequence = count()

        open_list = [
            (
                self.heuristics[start],
                next(sequence),
                start,
                [start],
                0
            )
        ]

        best_cost = {start: 0}
        explored = []

        while open_list:

            f, _, current, path, g = heapq.heappop(open_list)

            if g != best_cost.get(current):
                continue

            explored.append(current)

            if current == goal:
                return path, g, explored

            for neighbour, road_cost in self.graph[current].items():

                new_g = g + road_cost

                if new_g < best_cost.get(
                    neighbour, float("inf")
                ):

                    best_cost[neighbour] = new_g

                    new_f = (
                        new_g + self.heuristics[neighbour]
                    )

                    heapq.heappush(
                        open_list,
                        (
                            new_f,
                            next(sequence),
                            neighbour,
                            path + [neighbour],
                            new_g
                        )
                    )

        return None, 0, explored

    # STEP 7: Find route

    def find_route(self):

        start = self.source_box.get()
        goal = self.destination_box.get()

        route, cost, explored = self.astar(start, goal)

        if route:

            self.result_label.config(
                text=(
                    f"Optimal Route: {' -> '.join(route)}\n"
                    f"Total Travel Cost: {cost}\n"
                    f"Explored Locations: {', '.join(explored)}"
                )
            )

        else:

            self.result_label.config(
                text=(
                    "No route available.\n"
                    f"Explored Locations: {', '.join(explored)}"
                )
            )

        self.draw_graph(route)

    # STEP 8: Block road

    def update_block_options(self):

        roads = []

        for start in self.graph:

            for end in self.graph[start]:

                if self.locations.index(start) < self.locations.index(end):
                    roads.append(f"{start} - {end}")

        self.block_box["values"] = roads

        if roads:
            self.block_box.set(roads[0])
        else:
            self.block_box.set("")

    def block_road(self):

        selected = self.block_box.get()

        if not selected:
            messagebox.showwarning(
                "Warning", "No road available to block."
            )
            return

        start, end = selected.split(" - ", 1)

        del self.graph[start][end]
        del self.graph[end][start]

        self.update_block_options()
        self.draw_graph()

        self.result_label.config(
            text=f"Road {start} - {end} blocked. Find route again."
        )

    # STEP 9: Reset

    def reset_graph(self):

        if not self.original_graph:
            return

        self.graph = {
            node: neighbours.copy()
            for node, neighbours in self.original_graph.items()
        }

        self.update_block_options()
        self.draw_graph()

        self.result_label.config(
            text="Original road network restored."
        )

    # STEP 10: Draw graph

    def draw_graph(self, route=None):

        self.canvas.delete("all")

        if not self.locations:
            return

        self.root.update_idletasks()

        width = max(self.canvas.winfo_width(), 700)
        height = max(self.canvas.winfo_height(), 280)

        cx = width / 2
        cy = height / 2
        radius = min(width, height) * 0.34

        self.positions = {}

        n = len(self.locations)

        for i, node in enumerate(self.locations):

            angle = 2 * math.pi * i / n - math.pi / 2

            self.positions[node] = (
                cx + radius * math.cos(angle),
                cy + radius * math.sin(angle)
            )

        route_edges = set()

        if route:
            for i in range(len(route) - 1):
                route_edges.add(
                    frozenset((route[i], route[i + 1]))
                )

        # Draw roads
        for start in self.graph:

            for end, cost in self.graph[start].items():

                if self.locations.index(start) >= self.locations.index(end):
                    continue

                x1, y1 = self.positions[start]
                x2, y2 = self.positions[end]

                is_route = (
                    frozenset((start, end)) in route_edges
                )

                color = "green" if is_route else "gray"
                line_width = 4 if is_route else 2

                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color,
                    width=line_width
                )

                self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2 - 10,
                    text=str(cost),
                    fill="blue",
                    font=("Arial", 10, "bold")
                )

        # Draw locations
        for node, (x, y) in self.positions.items():

            self.canvas.create_oval(
                x - 25, y - 25,
                x + 25, y + 25,
                fill="lightblue",
                outline="navy",
                width=2
            )

            self.canvas.create_text(
                x, y,
                text=node,
                font=("Arial", 9, "bold")
            )


if __name__ == "__main__":

    root = tk.Tk()
    app = TrafficNavigationUI(root)
    root.mainloop()
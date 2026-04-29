"""Visualization of the simulation."""

import plotly.graph_objects as go
from plotly.colors import validate_colors
from src.graph import Graph


class Visualization:
    """Create class Visualization."""

    def __init__(self, graph: Graph, turns: list[list[str]], filename: str):
        """Initialize class Visualization.

        Args:
            graph (Graph): the graph where the drone moves.
            turns (list[list[str]]): the list of all the turns.
            filename (str): the configuration file in input.
        """
        self.graph = graph
        self.turns = turns
        self.filename = filename

    def _build_nodes(self) -> go.Scatter:
        x = []
        y = []
        labels = []
        colors: list[str] = []
        for i, (name, data) in enumerate(self.graph.zones.items()):
            x.append(data["x"])
            y.append(data["y"])
            labels.append(name)
            RAINBOW = ["red", "orange", "yellow", "green", "blue", "purple"]
            color = data["color"].lower()
            if color != "none":
                # 👇 1. gérer explicitement rainbow AVANT tout
                if color == "rainbow":
                    colors.append(RAINBOW[i % len(RAINBOW)])
                else:
                    try:
                        validate_colors([color])
                        colors.append(color)
                    except ValueError:
                        colors.append("gray")
            else:
                if data["hub_type"] == "start_hub":
                    colors.append("green")
                elif data["hub_type"] == "end_hub":
                    colors.append("yellow")
                elif data["zone"] == "restricted":
                    colors.append("red")
                else:
                    colors.append("blue")
        return go.Scatter(
            x=x,
            y=y,
            mode="markers",
            text=labels,
            hovertext=labels,
            hoverinfo="text",
            opacity=0.8,
            textposition="top center",
            marker=dict(size=40, color=colors),
            name="zones"
        )

    def _build_edges(self) -> go.Scatter:
        edge_x = []
        edge_y = []

        for c in self.graph.connections:
            x0 = self.graph.zones[c["from"]]["x"]
            y0 = self.graph.zones[c["from"]]["y"]
            x1 = self.graph.zones[c["to"]]["x"]
            y1 = self.graph.zones[c["to"]]["y"]

            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        return go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=3, color="gray"),
            hoverinfo="none",
            name="Connections"
        )

    def _build_frame(self) -> list[go.Frame]:
        frames = []
        drone_positions = {}
        start = self.graph.start

        drone_ids = set()
        for turn in self.turns:
            # appliquer les mouvements
            for move in turn:
                drone, _ = move.split("-")
                drone_ids.add(drone)
        drone_positions = {drone: start for drone in drone_ids}
        x = []
        y = []
        labels = []
        for drone, zone in drone_positions.items():
            x.append(self.graph.zones[zone]["x"])
            y.append(self.graph.zones[zone]["y"])
            labels.append(f"<b>{drone}</b>")
        frames.append(
            go.Frame(
                name="0",
                data=[
                    go.Scatter(
                        x=x,
                        y=y,
                        mode="markers+text",
                        text=labels,
                        textposition="top center",
                        textfont=dict(
                            size=16,
                            color="black"
                        ),
                        marker=dict(size=10,
                                    color="white",
                                    symbol='diamond',
                                    line=dict(width=2,
                                              color="black"))
                    )
                ],
                traces=[2]
            )
        )
        for turn in self.turns:
            restricted_hit = False
            for move in turn:
                drone, zone = move.split("-")
                drone_positions[drone] = zone

                if self.graph.zones[zone]["zone"] == "restricted":
                    restricted_hit = True
            x = []
            y = []
            labels = []
            for drone, zone in drone_positions.items():
                x.append(self.graph.zones[zone]["x"])
                y.append(self.graph.zones[zone]["y"])
                labels.append(drone)
            frame = go.Frame(
                    name=str(len(frames)),
                    data=[
                        go.Scatter(
                            x=x,
                            y=y,
                            mode="markers+text",
                            text=labels,
                            textposition="top center",
                            textfont=dict(
                                size=16,
                                color="black"
                            ),
                            marker=dict(size=10,
                                        color="white",
                                        symbol='diamond',
                                        line=dict(width=2, color="black"))
                        )
                    ],
                    traces=[2]
                )

            frames.append(frame)
            if restricted_hit:
                frames.append(frame)
        return frames

    def show(self) -> None:
        """Run the simulation."""
        edge_trace = self._build_edges()
        node_trace = self._build_nodes()
        frames = self._build_frame()
        initial_drones = frames[0].data[0] if frames else None
        fig = go.Figure(
            data=[edge_trace, node_trace, initial_drones],
            frames=frames
        )

        fig.update_layout(
            title=f"Drone Simulation - {self.filename}",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 1000}}]
                    }
                ]
            }],
            sliders=[{
                "active": 0,
                "currentvalue": {"prefix": "Turn: "},
                "steps": [
                    {
                        "method": "animate",
                        "label": f"{i}",
                        "args": [
                            [frame.name],
                            {"frame": {"duration": 300}, "mode": "immediate"}
                        ]
                    }
                    for i, frame in enumerate(frames)
                ]
            }]
        )

        fig.show()

import plotly.graph_objects as go
from src.graph import Graph


class Visualization:
    def __init__(self, graph: Graph, turns: list):
        self.graph = graph
        self.turns = turns
    
    def _build_nodes(self):
        x = []
        y = []
        labels = []
        colors = []

        for name, data in self.graph.zones.items():
            x.append(data["x"])
            y.append(data["y"])
            labels.append(name)

            # couleur selon le type
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
            mode="markers+text",
            text=labels,
            textposition="top center",
            marker=dict(size=12, color=colors),
            name="zones"
        )
    
    def _build_edges(self):
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
            line=dict(width=2, color="gray"),
            hoverinfo="none",
            name="Connections"
        )
    
    def _build_frame(self):
        drone_positions = {}
        frames = []

        for turn in self.turns:
            # appliquer les mouvements
            for move in turn:
                drone, zone = move.split("-")
                drone_positions[drone] = zone
        
            x = []
            y = []
            labels = []

            for drone, zone in drone_positions.items():
                x.append(self.graph.zones[zone]["x"])
                y.append(self.graph.zones[zone]["y"])
                labels.append(drone)
        
            frames.append(
                go.Frame(
                    data=[
                        go.Scatter(
                            x=x,
                            y=y,
                            mode="markers+text",
                            text=labels,
                            textposition="top center",
                            marker=dict(size=10, color="white"),
                            name="Drones"
                        )
                    ]
                )
            )

        return frames
    
    def show(self):
        edge_trace = self._build_edges()
        node_trace = self._build_nodes()
        frames = self._build_frame()

        initial_drones = frames[0].data[0] if frames else None

        fig = go.Figure(
            data=[edge_trace, node_trace, initial_drones],
            frames=frames
        )

        fig.update_layout(
            title="Drone Simulation",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"durations": 800}}]
                    }
                ]
            }]
        )
        fig.show()
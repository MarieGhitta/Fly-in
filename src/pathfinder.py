from src.graph import Graph
from typing import Any


class Pathfinder:
    def __init__(self, graph: Graph, zones: dict[str, dict[str, Any]],
                 start: str, end: str) -> None:
        self.graph = graph
        self.zones = zones
        self.start = start
        self.end = end

    def find_shortest_path(self) -> list[str]:
        distance: dict[str, float] = {}
        non_visited = []
        parents = {}
        path = []
        passed_priority = {}
        for name_zone in self.zones:
            if name_zone == self.start:
                distance[name_zone] = 0
            else:
                distance[name_zone] = float("inf")
            passed_priority[name_zone] = False
            non_visited.append(name_zone)
        while non_visited:
            min_cost = float("inf")
            for name_zone in non_visited:
                if distance[name_zone] < min_cost:
                    min_cost = distance[name_zone]
                    current_zone = name_zone
            # aucune zone accessible restante
            if min_cost == float("inf"):
                break
            for neighbors in self.graph.adjacency_list[current_zone]:
                if self.zones[neighbors]["zone"] == "normal":
                    neighbors_cost = 1
                elif self.zones[neighbors]["zone"] == "priority":
                    neighbors_cost = 1
                elif self.zones[neighbors]["zone"] == "restricted":
                    neighbors_cost = 2
                new_cost = min_cost + neighbors_cost
                new_has_priority = passed_priority[current_zone] or (
                    self.zones[neighbors]["zone"] == "priority"
                    )
                if new_cost < distance[neighbors]:
                    distance[neighbors] = new_cost
                    parents[neighbors] = current_zone
                    passed_priority[neighbors] = new_has_priority
                elif new_cost == distance[neighbors]:
                    if new_has_priority and not passed_priority[neighbors]:
                        parents[neighbors] = current_zone
                        passed_priority[neighbors] = new_has_priority
            index = non_visited.index(current_zone)
            non_visited.pop(index)
        current = self.end
        if current not in parents and current != self.start:
            raise ValueError("ERROR: map not possible.")
        while current != self.start:
            path.append(current)
            current = parents[current]
        path.append(self.start)
        return path[::-1]

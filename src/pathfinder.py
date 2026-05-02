"""Find the cheapest path."""


from src.graph import Graph
from typing import Any


class Pathfinder:
    """Create class Pathfinder."""

    def __init__(self, graph: Graph, zones: dict[str, dict[str, Any]],
                 start: str, end: str) -> None:
        """Initialize class Pathfinder.

        Args:
            graph (Graph): the grath create by class Graph.
            zones (dict[str, dict[str, Any]]): dict created with the parsing.
            start (str): start zone.
            end (str): end zone.
        """
        self.graph = graph
        self.zones = zones
        self.start = start
        self.end = end

    def find_cheapest_path(self) -> list[list[str]]:
        """Find cheapest path.

        Raises:
            ValueError: start zone not connected.

        Returns:
            list[str]: the path.
        """
        distance: dict[str, float] = {}
        non_visited = []
        parents: dict[str, list[str]] = {}
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
                    parents[neighbors] = [current_zone]
                    passed_priority[neighbors] = new_has_priority
                elif new_cost == distance[neighbors]:
                    if neighbors not in parents:
                        parents[neighbors] = []
                    parents[neighbors].append(current_zone)
                    passed_priority[neighbors] = (
                        passed_priority[neighbors] or new_has_priority
                    )
            index = non_visited.index(current_zone)
            non_visited.pop(index)
        if self.end not in parents and self.end != self.start:
            raise ValueError("ERROR: map not possible.")
        paths = self._build_paths(parents)
        priority_paths = []
        for p in paths:
            has_priority = False
            for zone in p:
                if self.zones[zone]["zone"] == "priority":
                    has_priority = True
                    break
            if has_priority:
                priority_paths.append(p)
        if priority_paths:
            return priority_paths
        return paths

    def _build_paths(self, parents: dict[str, list[str]], max_paths: int = 3
                     ) -> list[list[str]]:
        paths = []
        stack = [(self.end, [self.end])]  # quelle position dans quel chemin
        while stack:
            current, path = stack.pop()
            if current == self.start:
                paths.append(path[::-1])
                if len(paths) >= max_paths:
                    break
                continue
            for parent in parents.get(current, []):
                stack.append((parent, path + [parent]))
        return paths

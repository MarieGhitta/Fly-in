from src.graph import Graph


class Pathfinder:
    def __init__(self, graph: Graph, zones: dict, start: str, end: str):
        self.graph = graph
        self.zones = zones
        self.start = start
        self.end = end

    def find_shortest_path(self, usage: dict[str, int] | None = None) -> list:
        if usage is None:
            usage = {}
        distance = {}
        non_visited = []
        parents = {}
        path = []
        for name_zone in self.zones:
            if name_zone == self.start:
                distance[name_zone] = 0
            else:
                distance[name_zone] = float("inf")
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
                    bonus_priority = 0
                elif self.zones[neighbors]["zone"] == "priority":
                    neighbors_cost = 1
                    bonus_priority = -0.1
                elif self.zones[neighbors]["zone"] == "restricted":
                    neighbors_cost = 2
                    bonus_priority = 0
                neighbors_cost += usage.get(neighbors, 0)
                new_cost = min_cost + neighbors_cost + bonus_priority
                if new_cost < distance[neighbors]:
                    distance[neighbors] = new_cost
                    parents[neighbors] = current_zone
                elif new_cost == distance[neighbors]:
                    if self.zones[neighbors]["zone"] == "priority":
                        parents[neighbors] = current_zone
            index = non_visited.index(current_zone)
            non_visited.pop(index)
        current = self.end
        while current != self.start:
            path.append(current)
            current = parents[current]
        path.append(self.start)
        return path[::-1]


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
                if (self.zones[neighbors]["zone"] == "normal" or
                    self.zones[neighbors]["zone"] == "priority"):
                    neighbors_cost = 1
                elif self.zones[neighbors]["zone"] == "restricted":
                    neighbors_cost = 2
                neighbors_cost += usage.get(neighbors, 0)
                new_cost = min_cost + neighbors_cost
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
    
    def find_multiple_paths(self) -> list[list]:
        paths = []
        usage = {}
        while len(paths) < 5:
            path = self.find_shortest_path(usage)
            if path in paths:
                break
            paths.append(path)
            for zone in path:
                usage[zone] = usage.get(zone, 0) + 1
        return paths




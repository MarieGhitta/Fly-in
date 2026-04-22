class Graph:
    def __init__(self, zones: dict, connections: list[dict]):
        self.zones = zones
        self.connections = connections
        self.adjacency_list = {}
        self.start = ""
        self.end = ""

        for name_zone in self.zones:
            if self.zones[name_zone]["hub_type"] == "start_hub":
                self.start = name_zone
            elif self.zones[name_zone]["hub_type"] == "end_hub":
                self.end = name_zone
            self.adjacency_list[name_zone] = []
        for connection in self.connections:
            name_from = connection["from"]
            name_to = connection["to"]
            if (self.zones[name_from]["zone"] == "blocked"
               or self.zones[name_to]["zone"] == "blocked"):
                continue
            else:
                self.adjacency_list[name_from].append(name_to)
                self.adjacency_list[name_to].append(name_from)

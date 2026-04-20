from src.drone import Drone
from src.graph import Graph

class Simulation:
    def __init__(self, graph: Graph, paths: list[list], nb_drones: int):
        self.graph = graph
        self.paths = paths
        self.nb_drones = nb_drones
        self.drones_per_path = []
    
    def add_drones_per_path(self) -> list[list]:
        ID = 1
        base = self.nb_drones // len(self.paths)
        rest = self.nb_drones % len(self.paths)
        for path in self.paths:
            drones = []
            nb = base
            if rest > 0:
                nb += 1
                rest -= 1
            while nb > 0:
                drone = Drone(ID, path)
                drones.append(drone)
                nb -= 1
                ID += 1
            self.drones_per_path.append(drones)
        return self.drones_per_path

    def get_link_capacity(self, current_zone, next_zone):
        for connect in self.graph.connections:
            if (current_zone == connect["from"] and next_zone == connect["to"]
                or current_zone == connect["to"] and next_zone == connect["from"]):
                max_link_capacity = connect["max_link_capacity"]
                return max_link_capacity
        return 1

    def run(self):
        count_turn = 0
        while True:
            count_turn += 1
            finished = True
            positions_reserved = {}
            moves = []
            link_usage = {}
            for drones_group in self.drones_per_path:
                for drone in drones_group:
                    is_finished = drone.current_position == len(drone.path) - 1
                    if not is_finished:
                        finished = False
                    else:
                        continue
                    if drone.nb_waiting_turn > 0:
                        drone.nb_waiting_turn -= 1
                        continue
                    if not is_finished:
                        current_zone = drone.path[drone.current_position]
                        next_zone = drone.path[drone.current_position + 1]
                        link = tuple(sorted([current_zone, next_zone]))
                        max_drones = self.graph.zones[next_zone].get("max_drones", 1)
                        max_link_capacity = self.get_link_capacity(current_zone, next_zone)
                        if (next_zone == drone.path[-1]
                           or (positions_reserved.get(next_zone, 0) < max_drones
                           and link_usage.get(link, 0) < max_link_capacity)):
                            drone.current_position += 1
                            if self.graph.zones[next_zone]["zone"] == "restricted":
                                drone.nb_waiting_turn = 1
                            moves.append(f"D{drone.ID}-{next_zone}")
                            positions_reserved[next_zone] = positions_reserved.get(next_zone, 0) + 1 
                            link_usage[link] = link_usage.get(link, 0) + 1  
            if finished:
                break
            if moves:
                print(" ".join(moves))
        print(count_turn)
        return self.drones_per_path




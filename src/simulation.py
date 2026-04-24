from src.drone import Drone
from src.graph import Graph


class Simulation:
    def __init__(self, graph: Graph, path: list, nb_drones: int):
        self.graph = graph
        self.path = path
        self.nb_drones = nb_drones
        self.drones = []

    def add_drones(self) -> list[list]:
        ID = 1
        nb = self.nb_drones
        while nb > 0:
            drone = Drone(ID, self.path)
            self.drones.append(drone)
            nb -= 1
            ID += 1
        return self.drones

    def get_link_capacity(self, current_zone, next_zone) -> int:
        for connect in self.graph.connections:
            if (current_zone == connect["from"] and next_zone == connect["to"]
                or current_zone == connect["to"]
               and next_zone == connect["from"]):
                max_link_capacity = connect["max_link_capacity"]
                return max_link_capacity
        return 1

    def run(self) -> list:
        count_turn = 0
        turns = []
        while True:
            finished = True
            positions_reserved = {}
            moves = []
            link_usage = {}
            for drone in self.drones:
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
                    max_drones = self.graph.zones[next_zone].get(
                        "max_drones", 1)
                    max_link_capacity = self.get_link_capacity(
                        current_zone, next_zone)
                    if (next_zone == drone.path[-1]
                        or (positions_reserved.get(
                        next_zone, 0) < max_drones
                        and link_usage.get(link, 0) < max_link_capacity)):
                        drone.current_position += 1
                        if self.graph.zones[next_zone][
                                "zone"] == "restricted":
                            drone.nb_waiting_turn = 1
                        moves.append(f"D{drone.ID}-{next_zone}")
                        positions_reserved[
                            next_zone] = positions_reserved.get(
                                next_zone, 0) + 1
                        link_usage[link] = link_usage.get(link, 0) + 1
            if finished:
                break
            count_turn += 1
            if moves:
                print(" ".join(moves))
                turns.append(moves.copy())
        print(f"Total turns: {count_turn}")
        return turns

class Simulation:
    def __init__(self, paths: list[list], nb_drones: int):
        self.paths = paths
        self.nb_drones = nb_drones
        self.drones_per_path = []
    
    def add_drones_per_path(self) -> list[list]:
        base = self.nb_drones // len(self.paths)
        rest = self.nb_drones % len(self.paths)
        for path in self.paths:
            drones = []
            nb = base
            if rest > 0:
                nb += 1
                rest -= 1
            while nb > 0:
                drones.append(0)
                nb -= 1
            self.drones_per_path.append(drones)
        return self.drones_per_path

    def run(self):
        while True:
            finished = True
            positions_reserved = []
            for index, path in enumerate(self.paths):
                drones = self.drones_per_path[index]
                for drone in drones:
                    if drone != len(path) - 1:
                        finished = False
                i = len(drones) - 1
                while i >= 0:
                    if drones[i] != len(path) - 1:
                        next = drones[i] + 1
                        if (next not in positions_reserved
                           or next == len(path) - 1):
                            drones[i] += 1
                            positions_reserved.append(next)    
                    i -= 1
            if finished:
                break
            print(self.drones_per_path)
        return self.drones_per_path




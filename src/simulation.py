class Simulation:
    def __init__(self, path: list, nb_drones: int):
        self.path = path
        self.nb_drones = nb_drones

        drones = []
        i = 0
        while i < nb_drones:
            drones.append(0)
            i += 1
        
        for drone in drones:
            while drones[drone] != (len(path) - 1):
                drones[drone] += 1
                if drone != 0 and drones[drone - 1] <= drones[drone]:
                    drones[drone - 1] += 1
                drone += 1
            print(drones)



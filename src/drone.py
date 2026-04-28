class Entity:
    def __init__(self, ID: int) -> None:
        self.ID = ID


class Drone(Entity):
    def __init__(self, ID: int, path: list[str]) -> None:
        super().__init__(ID)
        self.ID = ID
        self.path = path
        self.current_position = 0
        self.nb_waiting_turn = 0

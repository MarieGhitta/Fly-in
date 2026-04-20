class Drone:
    def __init__(self, ID: int, path: list):
        self.ID = ID
        self.path = path
        self.current_position = 0
        self.nb_waiting_turn = 0

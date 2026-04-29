"""Create Entity classes."""


class Entity:
    """Create Entity class."""

    def __init__(self, ID: int) -> None:
        """Initialize Entity class.

        Args:
            ID (int): identity of the Entity.
        """
        self.ID = ID


class Drone(Entity):
    """Create class child Drone.

    Args:
        Entity (class): Class parent of Drone.
    """

    def __init__(self, ID: int, path: list[str]) -> None:
        """Initialize class Drone.

        Args:
            ID (int):
            path (list[str]): Path in the graph.
        """
        super().__init__(ID)
        self.ID = ID
        self.path = path
        self.current_position = 0
        self.nb_waiting_turn = 0

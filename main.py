"""Main file."""

from src.parsing import Parser
from src.graph import Graph
from src.pathfinder import Pathfinder
from src.simulation import Simulation
from src.visualization import Visualization
from typing import Any
import sys


def main() -> None:
    """Create the simulation and vusualization.

    Raises:
        if no file given as map configuration.
    """
    try:
        if len(sys.argv) != 2:
            raise ValueError("ERROR: missing map file or two many arguments")

        filename = sys.argv[1]

        parser = Parser(filename)
        result = parser.parsing()

        zones: dict[str, dict[str, Any]] = result["zones"]
        connections: list[dict[str, Any]] = result["connections"]

        graph = Graph(zones, connections)

        pathfinder = Pathfinder(graph, zones, graph.start, graph.end)

        paths = pathfinder.find_cheapest_path()
        print("DEBUG PATHS:", paths)

        simulation = Simulation(graph, paths, parser.drone_count)
        simulation.add_drones()
        turns = simulation.run()

        viz = Visualization(graph, turns, filename)
        viz.show()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

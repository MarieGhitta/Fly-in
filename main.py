from src.parsing import Parser
from src.graph import Graph
from src.pathfinder import Pathfinder
from src.simulation import Simulation
from src.visualization import Visualization
import sys


def main():
    try:
        # if len(sys.argv) < 2:
            # raise ValueError("ERROR: missing map file")

        # filename = sys.argv[1]

        parser = Parser("maps/challenger/01_the_impossible_dream.txt")
        result = parser.parsing()

        zones = result["zones"]
        connections = result["connections"]

        graph = Graph(zones, connections)

        pathfinder = Pathfinder(graph, zones, graph.start, graph.end)

        path = pathfinder.find_shortest_path()

        simulation = Simulation(graph, path, parser.drone_count)
        simulation.add_drones()
        turns = simulation.run()

        viz = Visualization(graph, turns)
        viz.show()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

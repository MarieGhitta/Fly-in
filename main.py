from src.parsing import Parser
from src.graph import Graph
from src.pathfinder import Pathfinder
from src.simulation import Simulation


def main():
    try:
        parser = Parser("maps/challenger/01_the_impossible_dream.txt")
        result = parser.parsing()

        zones = result["zones"]
        connections = result["connections"]

        graph = Graph(zones, connections)

        pathfinder = Pathfinder(graph, zones, graph.start, graph.end)

        path = pathfinder.find_multiple_paths()

        simulation = Simulation(graph, path, parser.drone_count)
        simulation.add_drones_per_path()
        simulation.run()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

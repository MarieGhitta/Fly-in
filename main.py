from src.parsing import Parser
from src.graph import Graph
from src.pathfinder import Pathfinder
from src.simulation import Simulation

parser = Parser("maps/challenger/01_the_impossible_dream.txt")
result = parser.parsing()

if isinstance(result, str):
    print(result)
    exit()
zones = result["zones"]
connections = result["connections"]

graph = Graph(zones, connections)

pathfinder = Pathfinder(graph, zones, graph.start, graph.end)

path = pathfinder.find_multiple_paths()

simulation = Simulation(graph, path, parser.drone_count)
simulation.add_drones_per_path()
simulation.run()


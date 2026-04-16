from src.parsing import Parser
from src.graph import Graph
from src.pathfinder import Pathfinder
from src.simulation import Simulation

parser = Parser("src/test.txt")
result = parser.parsing()

zones = result["zones"]
connections = result["connections"]

graph = Graph(zones, connections)

pathfinder = Pathfinder(graph, zones, graph.start, graph.end)

path = pathfinder.find_shortest_path()

simulation = Simulation(path, 3)




*This project has been created as part of the 42 curriculum by mghitta.*

# Fly-in — Drone Routing Simulation

## Description
Fly-in is a Python project that simulates the routing of multiple drones across a network of interconnected zones.  
The objective is to move all drones from a **start hub** to an **end hub** in the **fewest possible turns**, while respecting strict constraints such as:

- Zone capacity limits
- Connection capacity limits
- Movement costs (normal, restricted, priority)
- Collision and deadlock avoidance

The project is based on a graph representation of zones and connections, combined with a pathfinding algorithm and a simulation engine.

---

## Features

- Custom **file parser** for map configuration
- Graph-based **network modeling**
- **Shortest path algorithm** with cost handling
- Multi-drone **simulation engine**
- **Turn-by-turn output**
- Interactive **visualization using Plotly**
- Full error handling and validation

---

## Project Structure

```
.
├── main.py
├── src/
│   ├── parsing.py
│   ├── graph.py
│   ├── pathfinder.py
│   ├── simulation.py
│   ├── drone.py
│   └── visualization.py
├── Makefile
└── README.md
```

---

## How It Works

### 1. Parsing
The parser reads a map file and extracts:
- Number of drones
- Zones (type, coordinates, metadata)
- Connections

It validates the file format strictly and raises errors if needed.

### 2. Graph Construction
The graph:
- Stores zones and connections
- Builds an adjacency list
- Ignores blocked zones

### 3. Pathfinding
A Dijkstra-like algorithm is used:
- Normal zone → cost 1
- Priority zone → cost 1 (favored)
- Restricted zone → cost 2

The algorithm also prioritizes paths passing through priority zones.

### 4. Simulation
- All drones follow the computed path
- Movement is done turn by turn
- Constraints handled:
  - Zone capacity (`max_drones`)
  - Connection capacity (`max_link_capacity`)
  - Restricted zones require 2 turns

### 5. Visualization
Using Plotly:
- Zones are displayed with colors
- Drones move dynamically
- Interactive timeline with play button

---

## Installation

```bash
make install
```

Or manually:

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
make run FILE=map.txt
```

Or:

```bash
python main.py map.txt
```

---

## Example Output

```
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB
D1-goal D2-goal
Total turns: 3
```

---

## Pathfinding Algorithm (Dijkstra)

### Overview

This project uses a modified version of the **Dijkstra algorithm** to compute the shortest path from the `start_hub` to the `end_hub`.

The goal is to minimize the **total number of simulation turns**, taking into account:
- Zone types (normal, restricted, priority)
- Movement costs
- Graph structure

---

### Core Principle

Dijkstra’s algorithm computes the shortest path by iteratively selecting the node with the smallest known distance and updating its neighbors.

The main formula is:

d(v) = min(d(u) + w(u, v))

Where:
- `d(v)` is the shortest distance to node `v`
- `u` is a neighbor of `v`
- `w(u, v)` is the cost to move from `u` to `v`

---

### Initialization

- The start node is initialized with a distance of `0`
- All other nodes are initialized with `∞` (infinity)
- A list of non-visited nodes is maintained

---

### Node Selection

At each step, the algorithm selects the **non-visited node with the smallest distance**.

This ensures that the most promising path is always explored first.

---

### Edge Relaxation

For each neighbor of the current node:
1. The movement cost is calculated based on the zone type:
   - `normal` → cost = 1
   - `priority` → cost = 1
   - `restricted` → cost = 2
2. A new potential distance is computed
3. If this distance is smaller than the current one, it is updated

---

### Priority Zone Optimization

This implementation includes a custom optimization:

- If two paths have the **same cost**, the algorithm prefers the one that passes through a `priority` zone.

This improves path quality without increasing total cost.

---

### Path Reconstruction

Once the algorithm reaches the destination:
- The path is reconstructed by following parent nodes from `end_hub` back to `start_hub`
- The final path is then reversed to get the correct order

---

### Complexity

- Time complexity: **O(V²)**
- Space complexity: **O(V)**

Where `V` is the number of zones.

---

### Limitations

- The algorithm computes **only one shortest path**
- It does not distribute drones across multiple paths
- This can lead to congestion in the simulation

---

### Possible Improvements

- Implement **multi-path routing**
- Use a **priority queue (heap)** to improve performance → O((V + E) log V)
- Replace Dijkstra with **A\*** for faster convergence
- Add **traffic-aware routing** based on congestion

---

### Summary

This implementation of Dijkstra:
- Computes the shortest path based on movement cost
- Integrates zone-specific constraints
- Adds a custom priority optimization
- Serves as the foundation for the drone simulation

---

## Simulation Engine

### Overview

The simulation engine is responsible for moving all drones from the `start_hub` to the `end_hub` while respecting all constraints defined in the subject.

The simulation runs in **discrete turns**, where each drone may:
- Move to the next zone
- Wait if movement is not possible
- Handle multi-turn movement for restricted zones

The main objective is to minimize the **total number of turns**.

---

### Drone Model

Each drone is represented by:
- A unique ID
- A predefined path (computed by the pathfinding algorithm)
- Its current position in the path
- A waiting counter (`nb_waiting_turn`) for restricted zones

---

### Turn-Based Execution

The simulation runs in a loop until all drones reach the destination.

At each turn:
1. All drones are evaluated
2. Valid movements are computed
3. Constraints are checked
4. Movements are applied simultaneously
5. The turn is recorded and printed

---

### Movement Rules

A drone can move from its current zone to the next zone in its path if:

- The destination zone has available capacity (`max_drones`)
- The connection has not exceeded its capacity (`max_link_capacity`)
- The drone is not currently waiting (restricted zone handling)

If movement is not possible, the drone stays in place.

---

### Zone Capacity Management

- By default, a zone can contain only **one drone**
- Some zones allow more via `max_drones`
- The simulation uses a `positions_reserved` structure to:
  - Track how many drones will occupy a zone in the current turn
  - Prevent exceeding capacity

Special cases:
- The **start zone** allows all drones initially
- The **end zone** can receive multiple drones

---

### Connection Capacity Management

Each connection may define a maximum number of drones that can traverse it simultaneously.

The simulation tracks this using a `link_usage` structure:
- Each movement increments usage
- No more drones can use the connection once the limit is reached

---

### Restricted Zones Handling

Restricted zones require **2 turns to enter**.

Implementation:
- When a drone enters a restricted zone:
  - It moves immediately
  - A waiting counter (`nb_waiting_turn = 1`) is set
- During the next turn:
  - The drone cannot move
  - It completes the required delay

This ensures compliance with the subject rule:
> A drone cannot wait on a connection — it must complete the move.

---

### Conflict Avoidance

The simulation prevents:
- Multiple drones entering a zone beyond capacity
- Multiple drones exceeding link capacity
- Movement conflicts during the same turn

All decisions are made **before applying movements**, ensuring consistency.

---

### Output Format

Each turn prints all drone movements:


## Constraints Handling

- One drone per zone (unless specified)
- Multiple drones allowed in:
  - Start zone
  - End zone
- Link capacity enforced
- No movement through blocked zones

---

## Visual Representation

The visualization enhances understanding by:
- Showing drone movements step-by-step
- Highlighting zone types with colors
- Providing an interactive timeline

---

## Resources

- Python documentation
- Plotly documentation
- Graph theory (Dijkstra algorithm)

### AI Usage
AI was used for:
- Structuring the README
- Improving documentation clarity
- Reviewing algorithm explanations

All generated content was reviewed and understood before use.

## Conclusion

This project demonstrates:
- Graph algorithms
- Simulation design
- Constraint handling
- Clean code architecture

It highlights how algorithmic choices directly impact performance and efficiency.

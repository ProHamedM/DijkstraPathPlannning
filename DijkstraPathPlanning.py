# Importing the heapq library to use a priority queue
import heapq

# Node class represents each point in the graph
class Node:
    def __init__(self, name):
        self.name = name
        self.adjacents = {}  # Dictionary of neighbor nodes and edge weights

    # Add a neighboring node with an associated weight
    def add_neighbor(self, neighbor, weight):
        self.adjacents[neighbor] = weight

    # Less than method to compare nodes in the priority queue
    def __lt__(self, other):
        return self.name < other.name

# Graph class to manage the network of nodes
class Graph:
    def __init__(self):
        self.nodes = {}

    # Adds a new node to the graph if it doesn't exist
    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    # Creates an undirected edge between two nodes with a weight
    def add_edge(self, from_node, to_node, weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.nodes[from_node].add_neighbor(self.nodes[to_node], weight)
        self.nodes[to_node].add_neighbor(self.nodes[from_node], weight)  # Undirected graph

    # Dijkstra's algorithm to find the shortest path from start node to all other nodes
    def dijkstra(self, start_name):
        # Set initial distances to infinity and previous nodes to None
        distances = {node: float('inf') for node in self.nodes}
        previous_nodes = {node: None for node in self.nodes}
        distances[start_name] = 0

        # Use a priority queue to explore the closest node next
        priority_queue = [(0, self.nodes[start_name])]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Skip if we already have a better distance recorded
            if current_distance > distances[current_node.name]:
                continue

            # Explore each neighbor of the current node
            for neighbor, weight in current_node.adjacents.items():
                new_distance = current_distance + weight
                # If a shorter path to neighbor is found
                if new_distance < distances[neighbor.name]:
                    distances[neighbor.name] = new_distance
                    previous_nodes[neighbor.name] = current_node.name
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        return distances, previous_nodes

    # Reconstructs the shortest path from start to end node using results from Dijkstra
    def get_shortest_path(self, start, end):
        distances, previous_nodes = self.dijkstra(start)
        path_result = []
        current = end

        # Backtrack from end node to start node to build the path
        while current is not None:
            path_result.insert(0, current)
            current = previous_nodes[current]

        return path_result, distances[end]

# Simulated scenario: Robot cleaning windows of a 4-floor apartment
if __name__ == "__main__":
    graph = Graph()

    # Let's name windows using floor and position: F1W1, F1W2, ..., F4W3
    windows = [f"F{floor}W{window}" for floor in range(1, 5) for window in range(1, 4)]

    # Add windows to graph and connect horizontally on the same floor (adjacent windows)
    for floor in range(1, 5):
        for window in range(1, 4):
            current = f"F{floor}W{window}"
            if window < 3:
                right = f"F{floor}W{window+1}"
                graph.add_edge(current, right, 1)  # Horizontal movement
            if floor < 4:
                below = f"F{floor+1}W{window}"
                graph.add_edge(current, below, 2)  # Vertical movement between floors (takes more time)

    # Simulate cleaning path from bottom-left to top-right
    start = "F1W1"
    end = "F4W3"

    path_result, total_distance = graph.get_shortest_path(start, end)
    print(f"Robot cleaning path from {start} to {end}: {path_result} with total cost: {total_distance}")

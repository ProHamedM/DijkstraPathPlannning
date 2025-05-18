import heapq

class Node:
    def __init__(self, name):
        self.name = name
        self.adjacents = {}  # Dictionary of neighbor nodes and edge weights

    def add_neighbor(self, neighbor, weight):
        self.adjacents[neighbor] = weight

    def __lt__(self, other):
        return self.name < other.name


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def add_edge(self, from_node, to_node, weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.nodes[from_node].add_neighbor(self.nodes[to_node], weight)
        self.nodes[to_node].add_neighbor(self.nodes[from_node], weight)  # Undirected graph

    def dijkstra(self, start_name):
        # Initialize distances and priority queue
        distances = {node: float('inf') for node in self.nodes}
        previous_nodes = {node: None for node in self.nodes}
        distances[start_name] = 0
        priority_queue = [(0, self.nodes[start_name])]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node.name]:
                continue

            for neighbor, weight in current_node.adjacents.items():
                distance = current_distance + weight
                if distance < distances[neighbor.name]:
                    distances[neighbor.name] = distance
                    previous_nodes[neighbor.name] = current_node.name
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, previous_nodes

    def get_shortest_path(self, start, end):
        distances, previous_nodes = self.dijkstra(start)
        path = []
        current = end

        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]

        return path, distances[end]


# Example usage
if __name__ == "__main__":
    graph = Graph()

    # Example grid or map connections
    graph.add_edge('A', 'B', 1)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('B', 'D', 5)
    graph.add_edge('C', 'D', 1)

    path, distance = graph.get_shortest_path('A', 'D')
    print(f"Shortest path from A to D: {path} with total distance: {distance}")

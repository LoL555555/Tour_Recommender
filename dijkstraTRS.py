import heapq

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.priority = {}

    def add_node(self, value, priority):
        self.nodes.add(value)
        self.edges[value] = []
        self.priority[value] = priority

    def add_edge(self, from_node, to_node, distance, cost):
        self.edges[from_node].append((to_node, distance, cost))
        self.edges[to_node].append((from_node, distance, cost))

def dijkstra(graph, start, budget):
    # Priority queue to store nodes with their distances
    priority_queue = [(0, 0, 0, start, [])]  # (total_distance, total_cost, priority, current_node, route)
    visited = set()
    distances = {node: (float('infinity'), float('infinity'), []) for node in graph.nodes}
    distances[start] = (0, 0, [])  # (total_distance, total_cost, route)

    while priority_queue:
        (current_distance, current_cost, current_priority, current_node, current_route) = heapq.heappop(priority_queue)

        if current_node not in visited:
            visited.add(current_node)

            for (neighbor, distance, cost) in graph.edges[current_node]:
                if neighbor not in visited:
                    new_distance = distances[current_node][0] + distance
                    new_cost = distances[current_node][1] + cost

                    if new_distance < distances[neighbor][0] and new_cost <= budget:
                        new_route = current_route + [(current_node, neighbor)]
                        distances[neighbor] = (new_distance, new_cost, new_route)
                        heapq.heappush(priority_queue, (new_distance, new_cost, graph.priority[neighbor], neighbor, new_route))

    return distances

def print_full_route(route):
    route_str = ""
    for edge in route:
        route_str += f"  {edge[0]} -> {edge[1]}\n"
    return route_str

def tourism_recommender():
    # Create a sample graph
    g = Graph()

    num_nodes = int(input("Enter the number of tourist destinations: "))

    for i in range(num_nodes):
        node_name = input(f"Enter the name of tourist destination {i + 1}: ")
        priority = int(input(f"Enter the priority of tourist destination {i + 1} (lower values indicate higher priority): "))
        g.add_node(node_name, priority)

    num_edges = int(input("Enter the number of connections between destinations: "))

    for i in range(num_edges):
        from_node = input(f"Enter the starting destination of connection {i + 1}: ")
        to_node = input(f"Enter the ending destination of connection {i + 1}: ")
        distance = float(input(f"Enter the travel distance between {from_node} and {to_node}: "))
        cost = float(input(f"Enter the travel cost between {from_node} and {to_node}: "))
        g.add_edge(from_node, to_node, distance, cost)

    start_node = input("Enter the starting destination: ")
    budget = float(input("Enter your budget: "))

    # Run Dijkstra's algorithm from the starting node
    distances = dijkstra(g, start_node, budget)

    # Display recommended path with remaining budget
    print(f"\nRecommended path from {start_node} within budget {budget} (ordered by priority):")
    sorted_destinations = sorted(distances.keys(), key=lambda x: g.priority[x])
    for destination in sorted_destinations:
        distance, cost, route = distances[destination]
        remaining_budget = budget - cost
        priority = g.priority[destination]
        full_route = print_full_route(route)
        print(f"  {destination}: Distance - {distance}, Cost - {cost}, Remaining Budget - {remaining_budget}, Priority - {priority}")
        print("Full Route:")
        print(full_route)

if __name__ == "__main__":
    tourism_recommender()

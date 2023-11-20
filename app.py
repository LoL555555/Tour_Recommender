from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import heapq
import math
import random

class City:
    def __init__(self, name, coordinates, interest):
        self.name = name
        self.coordinates = coordinates
        self.interest = interest

    def __str__(self):
        return f"{self.name} - Interest: {self.interest}"

class Graph:
    def __init__(self):
        self.graph = {}

    def add_city(self, city):
        self.graph[city.name] = {'city': city, 'neighbors': {}}

    def add_connection(self, city1, city2):
        distance = self.calculate_distance(city1, city2)
        self.graph[city1.name]['neighbors'][city2.name] = distance
        self.graph[city2.name]['neighbors'][city1.name] = distance

    def calculate_distance(self, city1, city2):
        x1, y1 = city1.coordinates
        x2, y2 = city2.coordinates
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def generate_random_city(name):
    coordinates = (random.uniform(0, 10), random.uniform(0, 10))
    interest = random.randint(1, 10)
    return City(name, coordinates, interest)

def generate_all_connections(graph, cities):
    for city1 in cities:
        for city2 in cities:
            if city1 != city2:
                graph.add_connection(city1, city2)

def heuristic(city1, city2, interest_weight, distance_weight):
    # Custom heuristic function considering a single interest and distance
    interest_score = city2.interest  # Directly prioritize interest values

    distance_score = math.sqrt((city2.coordinates[0] - city1.coordinates[0])**2 +
                               (city2.coordinates[1] - city1.coordinates[1])**2)

    return interest_weight * interest_score - distance_weight * (1/distance_score)

def astar_search(graph, start_city, goal_city, min_cities_to_visit, interest_weight, distance_weight):
    open_set = [(0, start_city.name, [start_city.name])]
    closed_set = set()

    while open_set:
        current_cost, current_city_name, path = heapq.heappop(open_set)

        if current_city_name == goal_city.name and len(set(path)) >= min_cities_to_visit:
            return f"Goal reached! Total cost: {current_cost}, Path: {path}"

        if current_city_name in closed_set:
            continue

        closed_set.add(current_city_name)

        current_city = graph.graph[current_city_name]['city']
        for neighbor_name, distance in graph.graph[current_city_name]['neighbors'].items():
            if neighbor_name not in closed_set:
                neighbor_city = graph.graph[neighbor_name]['city']
                neighbor_cost = current_cost + distance
                neighbor_path = path + [neighbor_name]
                heuristic_value = heuristic(neighbor_city, goal_city, interest_weight, distance_weight)
                heapq.heappush(open_set, (neighbor_cost + heuristic_value, neighbor_name, neighbor_path))

    return "Goal not reached with the specified minimum cities."



cities = []















@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_path', methods=['POST'])
def calculate_path():
    data = request.json

    # Extract data from the JSON request
    interest_weight = data.get('interest_weight', 0.7)
    distance_weight = data.get('distance_weight', 0.3)
    start_city_name = data.get('start_city', '')
    goal_city_name = data.get('goal_city', '')
    min_cities_to_visit = data.get('min_cities_to_visit', 2)
    selected_cities = data.get('cities', [])

    for city_data in selected_cities:
        # Assuming city_data is in the format {'name': 'City1', 'coordinates': {'x': 1, 'y': 2}, 'interest': 7}
        name = city_data.get('name', '')
        coordinates = city_data.get('coordinates', {})
        interest = city_data.get('interest', 0)

        # Create a City object and add it to the cities list
        city = City(name, (coordinates.get('x', 0), coordinates.get('y', 0)), interest)
        cities.append(city)

    # Create a graph and add cities
    graph = Graph()
    for city in cities:
        graph.add_city(city)

    # Generate random connections between cities
    generate_all_connections(graph, cities)

    start_city = next((city for city in cities if city.name == start_city_name), None)
    goal_city = next((city for city in cities if city.name == goal_city_name), None)

    if not start_city or not goal_city:
        return jsonify({'error': 'Invalid start or goal city'}), 400


    # Perform A* search
    result = astar_search(graph, start_city, goal_city, min_cities_to_visit, interest_weight, distance_weight)

    # Display the result
    print(result)

    # Return the result as JSON
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
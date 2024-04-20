import math
import numpy as np
import random
def calculate_distance(city1, city2):
    return math.sqrt((city2[0] - city1[0])**2 + (city2[1] - city1[1])**2) 

def calculate_tour_length_nearest_neighbor(distance_matrix):
    num_cities = len(distance_matrix)
    visited = [False] * num_cities  
    start_city = 0  
    current_city = start_city
    tour_length = 0

    for _ in range(num_cities - 1):  
        nearest_city = None
        min_distance = float('inf')

        for next_city in range(num_cities):
            if next_city != current_city and not visited[next_city]:
                distance = distance_matrix[current_city][next_city]
                if distance < min_distance:
                    min_distance = distance
                    nearest_city = next_city

        tour_length += distance_matrix[current_city][nearest_city]
        visited[current_city] = True
        current_city = nearest_city

    
    tour_length += distance_matrix[current_city][start_city]

    return tour_length
def choose_next_node(current_node, visited, pheromone, eta ,num_nodes,alpha,beta):
    probabilities = []
    not_visited=[]
    for i in range(num_nodes):
        if i not in visited:
            not_visited.append(i)

    for i in range(num_nodes):
        if i not in visited:
            probabilities.append(pheromone[current_node][i]**alpha * eta[current_node][i]**beta)
    probabilities = probabilities / sum(probabilities)
    next_node_index = np.random.choice(range(len(not_visited)), p=probabilities)
    
    return not_visited[next_node_index]
# MAIN
city_coordinates = []
with open('TSPDATA.txt', 'r') as file:
    c=1
    for line in file:
        coordinates = list(map(float, line.split()))
        coordinates.remove(c)
        c+=1
        city_coordinates.append(coordinates)
nodes= c-1
distance_matrix = []
for city1 in city_coordinates:
    row = []
    for city2 in city_coordinates:
        distance = calculate_distance(city1, city2)
        row.append(distance)
    distance_matrix.append(row)
eta_matrix = []
for row in distance_matrix:
    eta_row = []
    for distance in row:
        if distance != 0:
            eta_row.append(1/distance)
        else:
            eta_row.append(0)
    eta_matrix.append(eta_row)

lnn= calculate_tour_length_nearest_neighbor(distance_matrix)
tao=np.ones((nodes,nodes))/(nodes*lnn)
alpha=1.0
beta=2.0
best_distance=9999999999
evaporation_rate=0.5
num_iterations = int(input("enter number of iterations"))
#num_ants = int(input("enter number of ants"))
num_ants=nodes
all_nodes=[]
for i in range(nodes):
    all_nodes.append(i)
for iteration in range(num_iterations):
    
    for ant in range(num_ants):
        #tour = [random.randint(0, nodes - 1)]
        tour=[]
        tour.append(ant)
        c=0
        distance = 0.0
        while len(tour) < nodes:
            next_node = choose_next_node(tour[c],tour,tao,eta_matrix,nodes,alpha,beta)
            tour.append(next_node)
            distance += distance_matrix[tour[c]][next_node] 
            c+=1
        distance += distance_matrix[tour[c]][tour[0]] 
        tour.append(tour[0])
        if distance <= best_distance:
            best_distance = distance
            best_tour = tour
    tao *= (1 - evaporation_rate)
    for i in range(len(best_tour) - 1):
        tao[best_tour[i]][best_tour[i+1]] += 1.0 / best_distance
        
print(f"Best tour: {best_tour}")
print(f"Best distance: {best_distance}")
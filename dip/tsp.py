from math import sqrt

def distance_of_path(path):
    return sum(distance(path[i], path[i+1]) for i in range(-1, len(path)-1))

def distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def tsp(coordinates):
    n = len(coordinates)
    tour = list(range(n))
    improved = True
    while improved:
        improved = False
        for i in range(0, n-2):
            for j in range(i+1, n-1):
                if  distance(coordinates[tour[i-1]], coordinates[tour[i]]) + distance(coordinates[tour[j]], coordinates[tour[j+1]])\
                    >\
                    distance(coordinates[tour[i-1]], coordinates[tour[j]]) + distance(coordinates[tour[i]], coordinates[tour[j+1]]):
                        tour[i:j+1] = reversed(tour[i:j+1])
                        improved = True
    return [coordinates[i] for i in tour]

def mean_point(screen, points):
    point = min(points, key = lambda x: distance(tuple(map(lambda x: x//2, screen.get_size())), x))
    return point

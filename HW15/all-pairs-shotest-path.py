#!/usr/bin/python

# All pairs shortest path algorithm

# In this assignment you will implement one or more algorithms for the all-pairs shortest-path problem.
# Here are data files describing three graphs:

# The first line indicates the number of vertices and edges, respectively.
# Each subsequent line describes an edge (the first two numbers are its tail and head, respectively)
# and its length (the third number).
# NOTE: some of the edge lengths are negative.
# NOTE: These graphs may or may not have negative-cost cycles.

# Your task is to compute the "shortest shortest path". Precisely, you must first identify which,
# if any, of the three graphs have no negative cycles. For each such graph, you should compute
# all-pairs shortest paths and remember the smallest one
# (i.e., compute minu,vExistVd(u,v), where d(u,v) denotes the shortest-path distance from u to v).

# If each of the three graphs has a negative-cost cycle, then enter "NULL" in the box below.
# If exactly one graph has no negative-cost cycles, then enter the length of its shortest shortest
# path in the box below. If two or more of the graphs have no negative-cost cycles, then enter the
# smallest of the lengths of their shortest shortest paths in the box below.

# OPTIONAL: You can use whatever algorithm you like to solve this question. If you have extra time,
# try comparing the performance of different all-pairs shortest-path algorithms!

GRAPH_test_1_FILENAME = "data/tests/all-pairs-shortest-path-graph-test-1.txt" # result: negative cycle
GRAPH_test_2_FILENAME = "data/tests/all-pairs-shortest-path-graph-test-2.txt" # result: negative cycle
GRAPH_test_3_FILENAME = "data/tests/all-pairs-shortest-path-graph-test-3.txt" # result: -3

GRAPH_1_FILENAME = "data/all-pairs-shortest-path-graph-1.txt" # result: negative cycle
GRAPH_2_FILENAME = "data/all-pairs-shortest-path-graph-2.txt" # result: negative cycle
GRAPH_3_FILENAME = "data/all-pairs-shortest-path-graph-3.txt" # result: -19

# graphs = [GRAPH_1_FILENAME, GRAPH_2_FILENAME, GRAPH_3_FILENAME] # result: -19
graphs = [GRAPH_test_1_FILENAME, GRAPH_test_2_FILENAME, GRAPH_test_3_FILENAME] # result: -3


def initialize(graph, source):
    destination = {}
    predecessor = {}
    for vertice in graph:
        destination[vertice] = float('Inf')
        predecessor[vertice] = None
    destination[source] = 0
    return destination, predecessor

def relax(vertice, previous, graph, distance, predecessor):
    if distance[previous] > distance[vertice] + graph[vertice][previous]:
        distance[previous] = distance[vertice] + graph[vertice][previous]
        predecessor[previous] = vertice

def bellman_ford(graph, source):
    global has_cycle

    distance, predecessor = initialize(graph, source)
    for i in range(len(graph)-1):
        for u in graph:
            for v in graph[u]:
                relax(u, v, graph, distance, predecessor)

    # check for negative cycles
    for u in graph:
        for v in graph[u]:
            if distance[v] > distance[u] + graph[u][v]:
                has_cycle = True

    return distance, predecessor

def getSmallest(distances, smallest):
    for idx in distances:
        if not smallest or distances[idx] < smallest:
            smallest = distances[idx]

    return smallest

smallest = False

for g in graphs:

    small = False
    has_cycle = False
    inFile = open(g, 'r')

    num_vertices = 0
    num_edges = 0
    graph = {}
    vertices = []

    # initializing the graph with an array of edges [tale, head]
    for f in inFile:
        if(num_vertices == 0):
            num_vertices, num_edges = map(int, f.split())
        else:
            tale, head, length = map(int, f.split())
            if tale not in vertices:
                vertices.append(tale)
            if head not in vertices:
                vertices.append(head)
            if tale not in graph:
                graph[tale] = {}
            graph[tale][head] = length

    vertices = sorted(vertices)

    # adding vertices without outgoing edges
    for vertice in vertices:
        if vertice not in graph:
            graph[vertice] = {}

    for vertice in vertices:
        d, p = bellman_ford(graph, vertice)
        small = getSmallest(d, small)

    if has_cycle:
        continue
    elif not smallest or smallest > small:
        smallest = small


if not smallest:
    print('result: NULL')
else:
    print('result: ' + str(smallest))
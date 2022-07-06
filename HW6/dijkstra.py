#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#The file contains an adjacency list representation of an undirected weighted graph with 200 vertices labeled 1 to 200.
# Each row consists of the node tuples that are adjacent to that particular vertex along with the length of that edge. For example, the 6th row has 6 as the first entry indicating that this row corresponds to the vertex labeled 6. The next entry of this row "141,8200" indicates that there is an edge between vertex 6 and vertex 141 that has length 8200.
# The rest of the pairs of this row indicate the other vertices adjacent to vertex 6 and the lengths of the corresponding edges.

# Your task is to run Dijkstra's shortest-path algorithm on this graph, using 1 (the first vertex) as the source vertex, and to compute the shortest-path distances between 1 and every other vertex of the graph. If there is no path between a vertex vv and vertex 1, we'll define the shortest-path distance between 1 and vv to be 1000000.
#You should report the shortest-path distances to the following ten vertices, in order: 7,37,59,82,99,115,133,165,188,197.
# You should encode the distances as a comma-separated string of integers. So if you find that all ten of these vertices except 115 are at distance 1000 away from vertex 1 and 115 is 2000 distance away, then your answer should be 1000,1000,1000,1000,1000,2000,1000,1000,1000,1000. Remember the order of reporting DOES MATTER, and the string should be in the same order in which the above ten vertices are given. The string should not contain any spaces.  Please type your answer in the space provided.
#IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn)O(mn) time implementation of Dijkstra's algorithm should work fine.
# OPTIONAL: For those of you seeking an additional challenge, try implementing the heap-based version.  Note this requires a heap that supports deletions, and you'll probably need to maintain some kind of mapping between vertices and their positions in the heap.


shortest_path ={}

def dijkstra(graph , Node):
    global shortest_path
    shortest_path[Node] = 0
    growing_node = {Node}
    while (len(growing_node) != len(graph) ):
        mini = 1000000
        mini_edge = (None , None)
        for node in growing_node:
            for edge in graph[node]:
                head_node = edge.split(",")[0]
                length = int(edge.split(",")[1])
                if head_node not in growing_node:
                    if shortest_path[node]+ length < mini:
                        mini_edge = (node ,head_node)
                        mini = shortest_path[node] + length
        if mini_edge != (None , None):
            growing_node.add(mini_edge[1])
            shortest_path[mini_edge[1]] = mini
        else:
            for key in graph.keys():
                if key not in growing_node:
                    growing_node.add(key)
                    shortest_path[key] = mini

graph = {}
with open('dijkstraData.txt') as f:
    data = f.readlines()
    for line in data:
        elements = list(map(str,line.split('\t')[:-1]))
        graph[str(elements[0])] = elements[1:]
f.close()

dijkstra(graph , "1")

ans = ''
for i in ['7','37','59','82','99','115','133','165','188','197']:
    ans += str(shortest_path[i]) + ","

ans = ans[:-1]

print(ans)
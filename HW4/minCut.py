#!/usr/binlocal/python

import sys
import random
import copy

# graph is going to be a hash:
# in which every entry is a vertex and the value is a list that represent the vertexes is linked to
# graph[1] = [2,3,4,5]

def buildGraphFromFile(_file):
    graph = {}
    f = open(_file)
    for l in f:
        items = map(int, l.split())
        vertex = items[0]
        edges = items[1:len(items)]
        graph[vertex] = edges
    return graph


def computeMinimunCut(graph):
    # if we only have two vertexes we are done
    if len(graph.keys()) <= 2:
        return graph

    # build list of edges to pick one at random
    E = []

    for k in graph.keys():
        for e in graph[k]:
            edge = (k,e)
            E.append(edge)

    t = random.choice(E)
    v = t[0]
    v_to_merge = t[1]
    edges1 = graph[v]

    # "collapse" to one vertex
    merged_vertex_name = v
    edges2 = graph[v_to_merge]

    # calculate union of the two edges lists
    # we are only contracting one edge at a time
    # this edge is (v,v_to_merge)
    final_edges = filter(lambda x: x!= v and x!=v_to_merge, list(edges1 + edges2 ))

    # delete original vertexes
    del graph[v]
    del graph[v_to_merge]

    # traverse graph, change references to v and v_to_merge with references to merged_vertex_name
    for k in graph.keys():
        tmp_edges  = []
        # rebuilding whole edges list
        for edge in graph[k]:
            if edge == v or edge == v_to_merge:
                tmp_edges.append(merged_vertex_name)
            else:
                tmp_edges.append(edge)
        # reset edges on current vertex to new list
        graph[k] = tmp_edges

    # enter new vertex
    graph[merged_vertex_name] = final_edges
    return computeMinimunCut(graph)


graph = buildGraphFromFile("adjancencyRepresentation.txt")
#print graph

# start number of crossing edges to 2m, m being number of vertexes
num_vertexes = len(graph.keys())
crossing_edges = 2 * num_vertexes

i  =  30
minimun_cut = graph

while i > 0:
    _graph = copy.deepcopy(graph)
    local_minimum = computeMinimunCut(_graph)
    keys = local_minimum.keys();
    local_min_crossing_edges = len(local_minimum[keys[0]])
    # now count crossing edges
    if crossing_edges > local_min_crossing_edges:
        crossing_edges = local_min_crossing_edges
        minimun_cut = local_minimum
    i = i - 1


print ("crossing edges {0}"). format(crossing_edges)
print minimun_cut
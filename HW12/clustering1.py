# Clustering with Kruskal's using a Union Find Datastructure

TARGET_CLUSTERS_K = 4

class UnionFind():

    def __init__(self, edges):
        self.node_to_leader = {}
        self.leader_to_size = {}
        self.num_leaders = 0

        for edge in edges:
            if edge[0] not in self.node_to_leader:
                self.node_to_leader[edge[0]] = edge[0]
                self.leader_to_size[edge[0]] = 1
                self.num_leaders += 1
            if edge[1] not in self.node_to_leader:
                self.node_to_leader[edge[1]] = edge[1]
                self.leader_to_size[edge[1]] = 1
                self.num_leaders += 1

    def get_leader(self, node):
        return self.node_to_leader[node]

    def have_same_leader(self, node1, node2):
        if self.get_leader(node1) == self.get_leader(node2):
            return True
        else:
            return False

    # merges groups that those two nodes belong to
    def merge(self, node1, node2):
        if self.leader_to_size[node1] > self.leader_to_size[node2]:
            old_leader = self.get_leader(node2)
            new_leader = self.get_leader(node1)

        else:
            old_leader = self.get_leader(node1)
            new_leader = self.get_leader(node2)

        for key in self.node_to_leader:
            if self.node_to_leader[key] == old_leader:
                self.node_to_leader[key] = new_leader
                self.leader_to_size[old_leader] -= 1
                self.leader_to_size[new_leader] += 1

        self.num_leaders -= 1


def select_pivot_idx(edges):
    size = len(edges)

    return size/2

def qsort_edges(edges):
    if len(edges) <= 1:
        return edges

    pivot_idx = select_pivot_idx(edges)

    pivot = edges.pop(pivot_idx)

    less = []
    greater = []

    for edge in edges:
        if edge[2] <= pivot[2]:
            less.append(edge)
        else:
            greater.append(edge)

    pivot_list = []
    pivot_list.append(pivot)

    return qsort_edges(less) + pivot_list + qsort_edges(greater)




#(1) Read file
f = open('clustering1.txt', 'r')
#f = open('cluster_TC1.txt', 'r') #k=4, ans=7
#f = open('cluster_TC2.txt', 'r') #k=2, ans=2
#f = open('cluster_TC3.txt', 'r') #k=4, ans=8
lines = f.readlines()
f.close()

edges = []
num_nodes = int(lines[0])

for line in lines[1:]:
    #node1, node2, cost
    edge = [0, 0, 0]
    edge[0], edge[1], edge[2] = line.split(' ')
    edge[0], edge[1], edge[2] = int(edge[0]), int(edge[1]), int(edge[2])

    edges.append(edge)

#(2) Sort edges
edges = qsort_edges(edges)

#(3) Build Union Find DS
union = UnionFind(edges)

#(4) Run the algorithm
done = 0
for edge in edges:
    # at this point we stop clustering, and try to find the min cost
    if done == 1:
        if union.have_same_leader(edge[0], edge[1]):
            continue
        else:
            print "Max spacing of %d-clustering is %d" %(TARGET_CLUSTERS_K, edge[2])
            break
    if not union.have_same_leader(edge[0], edge[1]):
        union.merge(edge[0], edge[1])
        if union.num_leaders <= TARGET_CLUSTERS_K:
            done = 1



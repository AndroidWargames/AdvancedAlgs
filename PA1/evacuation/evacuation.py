# python3

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def read_data_debug(a):
    vertex_count, edge_count = map(int, a[0].split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, a[_+1].split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def max_flow(graph, from_, to):
    done = True
    flow = 0
    while done:
        new = [True] * len(graph.graph)
        queue = [[from_,-1, -1]]
        new[from_] = False
        i = 0
        done = False
        while i < len(queue):
            a = graph.get_ids(queue[i][0])
            for j in a:
                e = graph.get_edge(j)
                if e.capacity - e.flow > 0 and new[e.v]:
                    queue.append([e.v, i, j])
                    new[e.v] = False
                    if e.v == to:
                        done = True
                        break
            if done:
                clean_ids(graph, queue)
                break
            i += 1
    for i in graph.get_ids(to):
        if i % 2 == 1:
            flow += graph.get_edge(i-1).flow
    return flow


def clean_ids(graph, queue):
    i = len(queue) - 1
    path = []
    edges = []
    while i > 0:
        path.append(queue[i][2])
        edges.append(graph.get_edge(queue[i][2]))
        i = queue[i][1]

    path.reverse()
    edges.reverse()

    min = 100000000
    for i in edges:
        a = i.capacity - i.flow
        if a < min:
            min = a
    for i in path:
        graph.add_flow(i, min)



# this code allows automated testing of the three sample tests, rather than relying on the standard in
"""
import os
dir_path = os.path.dirname(os.path.realpath(__file__)) + '/tests/'
for i in os.listdir(dir_path):
    if i.find('.a') == -1:
        print(i)
        with open(dir_path + i, 'r') as f:
            content = f.readlines()
        f.close()
        f = open(dir_path + i + '.a', 'r')
        c = f.read()
        c = int(c)
        graph = read_data_debug(content)
        d = max_flow(graph, 0, graph.size() - 1)
        if d == c:
            print(True)
        else:
            print([c,d])
        f.close()
exit(14)
"""
if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))

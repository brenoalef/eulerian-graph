import sys


class Graph:
    def __init__(self, vertices=None, edges=None):
        self.vertices, self.adj = [], {}
        if vertices is not None:
            for v in vertices:
                self.add_vertex(v)
        if edges is not None:
            for e in edges:
                self.add_edge(*e)
    
    def __iter__(self):
        return iter(self.vertices)
    
    def __getitem__(self, item):
        return iter(self.adj[item])
    
    def __str__(self):
        return 'V: %s\nE: %s' % (self.vertices, self.adj)
    
    def __len__(self):
        return len(self.vertices)
    
    def __contains__(self, item):
        return item in self.vertices
    
    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.append(v)
            self.adj[v] = []
    
    def add_edge(self, u, v):
        self.adj[u] = self.adj.get(u, []) + [v]
        self.adj[v] = self.adj.get(v, []) + [u]

    def number_of_vertices(self):
        return len(self.vertices)
    
    def number_of_edges(self):
        return sum(len(l) for _, l in self.adj.items()) // 2
    
    def dfs_util(self, vertex, visited):
        visited[vertex] = True
        for v in self.adj[vertex]:
            if not visited[v]:
                self.dfs_util(v, visited)
        
    def is_connected(self):
        visited = {}
        for v in self.vertices:
            visited[v] = False
        self.dfs_util(self.vertices[0], visited)
        for v in self.vertices:
            if not visited[v]:
                return False
        return True


def read_graph(file_path):
    graph_file = open(file_path, "r")
    graph = Graph()
    for line in graph_file.read().splitlines():
        edge = line.split(" ")
        graph.add_vertex(edge[0])
        graph.add_vertex(edge[1])
        graph.add_edge(edge[0], edge[1])
    return graph


def hierholzer(graph):
    if not graph.is_connected():
        print("Disconnected graph")
        return None
    for v in graph:
        if len(list(graph[v])) % 2 == 1:
            print("Vertex with odd degree: " + v)
            return None
    edge_count = {}
    for v in graph:
        edge_count[v] = len(graph.adj[v])
    if not len(edge_count):
        print("Empty graph")
        return None
    curr_path = []
    circuit = []
    curr_path.append(graph.vertices[0])
    curr_v = graph.vertices[0]
    while len(curr_path):
        if edge_count[curr_v]:
            curr_path.append(curr_v)
            next_v = graph.adj[curr_v][-1]
            edge_count[curr_v] = edge_count[curr_v] - 1
            edge_count[next_v] = edge_count[next_v] - 1
            graph.adj[curr_v].pop()
            graph.adj[next_v].remove(curr_v)
            curr_v = next_v
        else:
            circuit.append(curr_v)
            curr_v = curr_path[-1]
            curr_path.pop()
    return circuit


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 2:
        print("Usage: %s <graph file path>" % argv[0])
        quit()
    
    graph = read_graph(argv[1])
    
    circuit = hierholzer(graph)
    
    if circuit is not None:
        print(circuit)
    else:
        print("Not an eulerian graph")

from graph.edge import Edge
'''
Need to implement connects_vertex
'''


class DirectedGraph:

    def __init__(self):
        self.edges = []
        self.vertices = []
        self.start_vertices = []
        self.terminal_vertices = []

    # Receives a pair of vertex

    def add_edge(self, s, t):
        edge = Edge(s, t)
        self.edges.append(edge)
        self.start_vertices.append(s)
        self.terminal_vertices.append(t)
        return edge

    def add_vertex(self, v):
        self.vertices.append(v)

    def get_edge(self, s, t):
        if s not in self.vertices:
            return None
        for edge in self.edges:
            if edge.connects_vertex(s) and edge.connects_vertex(t):
                return edge
        return None

    def get_incoming_edges(self, v):
        results = []
        edges = self.get_vertex_edges(v)
        for e in edges:
            if e.has_target(v):
                results.append(e)
        return results

    def get_outgoing_edges(self, v):
        results = []
        edges = self.get_vertex_edges(v)
        for e in edges:
            if e.has_source(v):
                results.append(e)

        return results

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_vertex_edges(self, v):
        edges = []
        for e in self.edges:
            if e.contains(v):
                edges.append(e)
        return edges

    def remove_edge(self, e):
        self.edges.remove(e)

    def count_vertices(self):
        return len(self.vertices)
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
        self.vertices[s]=[]
        self.vertices[t]=[]
        edge = Edge(s, t)
        self.edges.append(edge)
        self.start_vertices.append(s)
        self.terminal_vertices.append(t)
        return edge
    def add_edge_abs(self, s, t):
        ss = []
        ss.append(s)
        ts = []
        ts.append(t)
        if self.check_edge(ss,ts)==False:
            return None
        
        edge = Edge.Edge(s, t)
        self.edges[edge] = edge
        self.start_vertices.append(s)
        self.terminal_vertices.append(t)
        return edge
    def add_vertex(self, v):
        if v is None:
            return None
        if self.contains(v):
            return None
        if v not in self.vertices:
            self.vertices[v]=[]
        return v

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
        result = list(self.vertices.keys())
        for i in result:
            print(i)
        if result is None:
            return {}
        else:
            return result
#        return self.vertices

    def get_edges(self):
        result = list(self.edges.keys())
        re ={}
        if result is None:
            return re
        else:
            return result
#        return self.edges
    def get_edges2(self, v):
        if v is None:
            return None
        if  v in self.vertices:
            return self.vertices[v]
        else:
            return None

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

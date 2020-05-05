from graph.edge import Edge
'''
Need to implement connects_vertex
'''


class DirectedGraph:

    def __init__(self):
        self.edges = {}
        self.vertices = {}
        self.start_vertices = []
        self.terminal_vertices = []

    # Receives a pair of vertex

    def add_edge(self, s, t):
        self.vertices[s] = []
        self.vertices[t] = []
        edge = Edge(s, t)
        self.edges[edge] = edge
        self.start_vertices.append(s)
        self.terminal_vertices.append(t)
        return edge

    def add_edge_abs(self, s, t):
        ss = []
        ss.append(s)
        ts = []
        ts.append(t)
        if self.check_edge(ss, ts) == False:
            return None

        edge = Edge(s, t)
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
            self.vertices[v] = []
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
        #for i in result:
        #    print(i)
        if result is None:
            return {}
        else:
            return result
#        return self.vertices

    def get_vertices_t(self):
        return self.vertices

    def get_edges_t(self):
        return self.edges

    def get_edges(self):
        result = list(self.edges.keys())
        re = {}
        if result is None:
            return re
        else:
            return result
#        return self.edges

    def get_edges2(self, v):
        if v is None:
            return None
        if v in self.vertices:
            return self.vertices[v]
        else:
            return None

    def get_vertex_edges(self, v):
        edges = []
        for e, val in self.edges.items():
            if v == e.get_source() or v == e.get_target():
                edges.append(val)
        return edges

#        edges = []
#        for e in self.edges:
#            if e.contains(v):
#                edges.append(e)
#        return edges
    def get_vertex_edges2(self, v):
        edges = []
        for e, val in self.edges.items():
            if v == e.get_source():
                edges.append(val)
        return edges

    def remove_edge(self, e):
        if e is None:
            return None
        if self.contains2(e):
            return self.edges.pop(e)
        else:
            return None

    def remove_vertex(self, v):
        if v is None:
            return None
        if self.contains(v):
            es = self.get_edges2(v)
            for i in es:
                i.remove_vertex(v)
            self.vertices.pop(v)
            return v
        return None

    def count_vertices(self):
        return len(self.vertices)

    def conunt_edges(self):
        return len(self.edges)

    def contains(self, v):
        if v in self.get_vertices():
            return True
        return False

    def contains2(self, v):
        if v in self.get_edges():
            return True
        return False

    def check_edge(self, ss, ts):
        es = self.getEdgesWithSourcesAndTargets(ss, ts)
        for e in es:
            if len(e.getSourceVertices()) == len(ss) and len(e.getTargetVertices()) == len(ts):
                    return False
        return True

        # if len(es) > 0:
        #     i = iterator.HasNextIterator(es)
        #     while i.has_next():
        #         e = i.next()
        #         if len(e.getSourceVertices()) == len(ss) and len(e.getTargetVertices()) == len(ts):
        #             return False
        # return True

    def getEdgesWithSourcesAndTargets(self, ss, ts):
        result = set()
        for s in ss:
            for t in ts:
                result.union(self.getEdgesWithSourceAndTarget(s, t))
        return result

    def getEdgesWithSourceAndTarget(self, s, t):
        result = set()
        es = self.get_edges2(s)
        for e in es:
            if e.has_source(s) and e.has_target(t):
                result.add(e)
        # i = iterator.HasNextIterator(es)
        # while i.has_next():
        #     e = i.next()
        #     if e.hasSource(s) and e.hasTarget(t):
        #         result.add(e)
        return result

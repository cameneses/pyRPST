from graph.directed_graph import DirectedGraph 
from graph.vertex import Vertex 
from graph.edge import Edge 

from tctree.tctree import TCTree

class RPST:

    def __init__(self, graph):
        self.normalized_graph = DirectedGraph()
        self.extra_edges = []
        self.graph = graph
        self.ne2oe = {}
        self.ov2nv = {}

    def normalize_graph(self):
        sources = []
        sinks = []
        mixed = []

        for v in self.graph.get_vertices():
            if (len(self.graph.get_incoming_edges(v)) == 0 and len(self.graph.get_outgoing_edges(v)) == 0):
                continue
            elif (len(self.graph.get_incoming_edges(v)) == 0):
                sources.append(v)
            elif (len(self.graph.get_outgoing_edges(v)) == 0):
                sinks.append(v)
            elif (len(self.graph.get_incoming_edges(v)) > 1 and len(self.graph.get_outgoing_edges(v)) > 1):
                mixed.append(v)

            vertex = Vertex(v.name)
            self.normalized_graph.add_vertex(vertex)
            self.ov2nv[v] = vertex

        for e in self.graph.get_edges():
            source = e.get_source()
            target = e.get_target()
            edge = Edge(source, target)
            self.ne2oe[source] = target
            self.normalized_graph.add_edge(self.ov2nv[e.get_source()], self.ov2nv[e.get_target()])

        src = Vertex("src")
        snk = Vertex("snk")

        self.normalized_graph.add_vertex(src)
        self.normalized_graph.add_vertex(snk)
        
        # This is not really useful
        for v in sources:
            edge = self.normalized_graph.add_edge(src, self.ov2nv[v])
            self.extra_edges.append(edge)

        for v in sinks:
            edge = self.normalized_graph.add_edge(self.ov2nv[v], snk)
            self.extra_edges.append(edge)

        for v in mixed:
            vertex = Vertex(v.name + "*")
            self.normalized_graph.add_vertex(vertex)
            for e in self.normalized_graph.get_incoming_edges(self.ov2nv[v]):
                self.normalized_graph.remove_edge(e)
                edge = self.ne2oe[e]
                del self.ne2oe[e]
                ee = self.normalized_graph.add_edge(self.ov2nv[edge.get_source()], vertex)
                self.ne2oe[ee] = edge
            self.extra_edges.append(self.normalized_graph.add_edge(vertex, self.ov2nv[v]))
        
        self.back_edge = self.normalized_graph.add_edge(snk, src)
        self.extra_edges.append(self.back_edge)

    def generate_tctree(self):
        tctree = TCTree(self.normalized_graph, self.back_edge)
        tctree.construct()


if __name__ == "__main__":
    # graph = DirectedGraph()
    # vertices = []
    # for i in range(5):
    #     v = Vertex(i)
    #     graph.add_vertex(v)
    #     vertices.append(v)
    # for v in vertices:
    #     for u in vertices:
    #         if v != u:
    #             graph.add_edge(v, u)
    
    # rpst = RPST(graph)
    # rpst.normalize_graph()

    # v = [Vertex(i) for i in range(5)]
    # graph = DirectedGraph()
    # for u in v:
    #     graph.add_vertex(u)
    # graph.add_edge(v[0], v[1])
    # graph.add_edge(v[2], v[1])
    # graph.add_edge(v[1], v[3])
    # graph.add_edge(v[1], v[4])
    # rpst = RPST(graph)
    # rpst.normalize_graph()
    # rpst.generate_tctree()

    graph = DirectedGraph()
    s = Vertex("s")
    u = Vertex("u")
    v = Vertex("v")
    w = Vertex("w")
    x = Vertex("x")
    y = Vertex("y")
    z = Vertex("z")
    t = Vertex("t")
    graph.add_vertex(s)
    graph.add_vertex(u)
    graph.add_vertex(v)
    graph.add_vertex(w)
    graph.add_vertex(x)
    graph.add_vertex(t)

    graph.add_edge(s, u)
    graph.add_edge(u, v)
    graph.add_edge(u, w)
    graph.add_edge(v, w)
    graph.add_edge(v, x)
    graph.add_edge(w, x)
    graph.add_edge(x, t)

    rpst = RPST(graph)
    rpst.normalize_graph()
    rpst.generate_tctree()




    
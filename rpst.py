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
            #source = e.get_source()
            #target = e.get_target()
            #edge = Edge(source, target)
            self.ne2oe[self.normalized_graph.add_edge(self.ov2nv[e.get_source()], self.ov2nv[e.get_target()])] = e
            

        src = Vertex("src")
        self.normalized_graph.add_vertex(src)
        # This is not really useful
        for v in sources:
            edge = self.normalized_graph.add_edge(src, self.ov2nv[v])
            self.extra_edges.append(edge)
            
        snk = Vertex("snk")
        self.normalized_graph.add_vertex(snk)
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
    
#    s = Vertex("s")
#    u = Vertex("u")
#    v = Vertex("v")
#    w = Vertex("w")
#    x = Vertex("x")
#    y = Vertex("y")
#    z = Vertex("z")
#    t = Vertex("t")
#    graph.add_vertex(s)
#    graph.add_vertex(u)
#    graph.add_vertex(v)
#    graph.add_vertex(w)
#    graph.add_vertex(x)
#    graph.add_vertex(t)
#
#    graph.add_edge(s, u)
#    graph.add_edge(u, v)
#    graph.add_edge(u, w)
#    graph.add_edge(v, w)
#    graph.add_edge(v, x)
#    graph.add_edge(w, x)
#    graph.add_edge(x, t)
    A = Vertex("A")
    B = Vertex("B")
    C = Vertex("C")
    D = Vertex("D")
    E = Vertex("E")
    F = Vertex("F")
    G = Vertex("G")
    H = Vertex("H")
    XOR1 = Vertex("XOR1")
    XOR2 = Vertex("XOR2")
    AND1 = Vertex("AND1")
    
    graph.add_vertex(H)
    graph.add_vertex(F)
    graph.add_vertex(XOR2)
    graph.add_vertex(D)
    graph.add_vertex(XOR1)    
    graph.add_vertex(AND1)
    graph.add_vertex(C)    
    graph.add_vertex(G)
    graph.add_vertex(A)
    graph.add_vertex(B)
    graph.add_vertex(E)

    


    graph.add_edge(A, AND1)
    graph.add_edge(AND1, B)
    graph.add_edge(AND1, XOR1)
    graph.add_edge(XOR1, C)
    graph.add_edge(XOR1, D)
    graph.add_edge(B, XOR2)
    graph.add_edge(XOR2, E)
    graph.add_edge(XOR2, F)
    graph.add_edge(E, H)
    graph.add_edge(F, G)
    graph.add_edge(C, G)
    graph.add_edge(D, G)
    graph.add_edge(G, H)
#    S = Vertex("S")
#    N = Vertex("N")
#    V = Vertex("V")
#    W = Vertex("W")
#    X = Vertex("X")
#    Y = Vertex("Y")
#    Z = Vertex("Z")
#    T = Vertex("T")
#    Q = Vertex("Q")
#    I = Vertex("I")
#    
#    graph.add_vertex(S)
#    graph.add_vertex(N)
#    graph.add_vertex(V)
#    graph.add_vertex(W)
#    graph.add_vertex(X)
#    graph.add_vertex(Y)
#    graph.add_vertex(Z)
#    graph.add_vertex(T)
#    graph.add_vertex(Q)
#    graph.add_vertex(I)
#    
#    graph.add_edge(S,N)
#    graph.add_edge(S,V)
#    graph.add_edge(N,W)
#    graph.add_edge(V,W)
#    graph.add_edge(W,X)
#    graph.add_edge(W,Q)
#    graph.add_edge(X,Y)
#    graph.add_edge(X,Z)
#    graph.add_edge(Y,I)
#    graph.add_edge(Z,I)
#    graph.add_edge(Q,I)
    
    rpst = RPST(graph)
    rpst.normalize_graph()
    rpst.generate_tctree()




    
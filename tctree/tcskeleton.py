from graph.directed_graph import DirectedGraph
import copy 
class TCSkeleton(DirectedGraph):

    def __init__(self, graph = None, e2o = None):
        super().__init__()
        if graph:
            self.graph = graph
            self.virtual_edges = []
            self.e2o = e2o
            self.o2e = {}
            self.map_edges()
            self.copy_graph()
        else:
            self.graph =[]
            self.virtual_edges = []
            self.e2o =  {}
            self.o2e =  {}

    def map_edges(self):
        for e in self.graph.get_edges():
#            se = self.add_edge(e.get_source(), e.get_target(), None)
            se = self.add_edge(e.get_source(), e.get_target())
            self.e2o[se] = e

    def add_virtual_edge(self, s, t, tag = None):
        e = super().add_edge(s, t)
        self.virtual_edges.append(e)
        if tag:
            e.set_tag(tag)
        return e

    def add_edge_t(self, v, w, o):
        e = super().add_edge(v, w)
        if e != None:
            self.e2o[e] = o
            self.e2o[o] = e
        return e

    def copy_graph(self):
        self.vertices = copy.copy(self.graph.get_vertices_t())
        self.edges = copy.copy(self.graph.get_edges_t())
#        self.vertices = self.graph.get_vertices().copy()
#        self.edges = self.graph.get_edges().copy()

    def remove_edge(self, e):
        self.virtual_edges.remove(e)
        if e in self.o2e:
            self.o2e.pop(self.e2o.get(e))
            self.e2o.pop(e)
        super().remove_edge(e)

    

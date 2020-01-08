from graph.directed_graph import DirectedGraph

class TCSkeleton(DirectedGraph):

    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.virtual_edges = []
        self.e2o = {}
        self.map_edges()
        self.copy_graph()

    def map_edges(self):
        for e in self.graph.get_edges():
            se = self.add_edge(e.get_source(), e.get_target())
            self.e2o[se] = e
        print(self.e2o)

    def add_virtual_edge(self, s, t):
        e = super().add_edge(s, t)
        self.virtual_edges.append(e)
        return e

    def copy_graph(self):
        self.vertices = self.graph.get_vertices().copy()
        self.edges = self.graph.get_edges().copy()

    def remove_edge(self, e):
        super().remove_edge(e)

    

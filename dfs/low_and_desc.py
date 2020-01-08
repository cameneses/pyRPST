from dfs.dfs import DFS

INVALID_NODE = None

class LowAndDesc(DFS):

    def __init__(self, graph, container, adj_map):
       super().__init__(graph, container, adj_map)
       self.lowpt1_num_map = {}
       self.lowpt2_num_map = {}
       self.lowpt1_vertex_map = {}
       self.lowpt2_vertex_map = {}
       self.num_desc_map = {}

       self.initialize()

    def initialize(self):
        super().initialize()

        for node in self.graph.get_vertices():
            self.lowpt1_num_map[node] = -1
            self.lowpt2_num_map[node] = -1
            self.lowpt1_vertex_map[node] = INVALID_NODE
            self.lowpt2_vertex_map[node] = INVALID_NODE
            self.num_desc_map[node] = -1

        self.meta["DFS_LOWPT1_NUM"] = self.lowpt1_num_map
        self.meta["DFS_LOWPT2_NUM"] = self.lowpt2_num_map
        self.meta["DFS_LOWPT1_VERTEX"] = self.lowpt1_vertex_map
        self.meta["DFS_LOWPT2_VERTEX"] = self.lowpt2_vertex_map
        self.meta["DFS_NUM_DESC"] = self.num_desc_map

    def pre_visit(self, v, dfs_number):
        self.lowpt1_num_map[v] = dfs_number
        self.lowpt2_num_map[v] = dfs_number
        self.lowpt1_vertex_map[v] = v
        self.lowpt2_vertex_map[v] = v
        self.num_desc_map[v] = 1

    def pre_traverse(self, e, w, is_tree_edge):
        super().pre_traverse(e, w, is_tree_edge)

        v = e.get_other_vertex(w)
        if not is_tree_edge:
            if self.dfs_num_map[w] < self.lowpt1_num_map[v]:
                self.lowpt2_num_map[v] = self.lowpt1_num_map[v]
                self.lowpt2_vertex_map[v] = self.lowpt1_vertex_map[v]

                self.lowpt1_num_map[v] = self.dfs_num_map[w]
                self.lowpt1_vertex_map[v] = w
            elif self.dfs_num_map[w] > self.lowpt1_num_map[v]:
                if self.dfs_num_map[w] < self.lowpt2_num_map[v]:
                    self.lowpt2_num_map[v] = self.dfs_num_map[w]
                    self.lowpt2_vertex_map[v] = w

    def post_traverse(self, e, w):
        v = e.get_other_vertex(w)

        if self.lowpt1_num_map[w] < self.lowpt1_num_map[v]:
            minimum = min(self.lowpt1_num_map[v], self.lowpt2_num_map[w])
            self.lowpt2_num_map[v] = minimum
            
            if minimum == self.lowpt1_num_map[v]:
                self.lowpt2_vertex_map[v] = self.lowpt1_vertex_map[v]
            else:
                self.lowpt2_vertex_map[v] = self.lowpt2_vertex_map[w]

            self.lowpt2_vertex_map[v] = self.lowpt1_num_map[w]
            self.lowpt1_vertex_map[v] = self.lowpt1_vertex_map[w]

        elif self.lowpt1_num_map[w] == self.lowpt1_num_map[v]:
            if self.lowpt2_num_map[w] < self.lowpt2_num_map[v]:
                self.lowpt2_num_map[v] = self.lowpt2_num_map[w]
                self.lowpt2_vertex_map[v] = self.lowpt2_vertex_map[w]

        else:
            if self.lowpt1_num_map[w] < self.lowpt2_num_map[v]:
                self.lowpt2_num_map[v] = self.lowpt1_num_map[w]
                self.lowpt2_vertex_map[v] = self.lowpt1_vertex_map[w]

        self.num_desc_map[v] = self.num_desc_map[v] + self.num_desc_map[w]



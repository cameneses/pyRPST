from dfs.dfs import DFS

INVALID_NODE = None


class Number(DFS):

    def __init__(self, graph, container, adj_map):
        super().__init__(graph, container, adj_map)
        self.highpt_map = {}
        self.num_v_map = {}
        self.num_tree_edges_map = {}
        self.lowpt1_num_map = {}
        self.lowpt2_num_map = {}
        self.num_vertices = -1
        self.initialize()

    def initialize(self):
        super().initialize()

        for node in self.graph.get_vertices():
            self.highpt_map[node] = []
            self.num_v_map[node] = -1
            self.num_tree_edges_map[node] = -1

        self.meta["DFS_LOWPT1_NUM"] = self.lowpt1_num_map
        self.meta["DFS_LOWPT2_NUM"] = self.lowpt2_num_map
        self.meta["DFS_HIGHPT_LISTS"] = self.highpt_map
        self.meta["DFS_NUM_V"] = self.num_v_map
        self.meta["DFS_NUM_TREE_EDGES"] = self.num_tree_edges_map

        self.num_vertices = self.graph.count_vertices()

    def pre_visit(self, v, dfs_number):
        self.num_v_map[v] = self.num_vertices - self.meta["DFS_NUM_DESC"][v] + 1
        self.num_tree_edges_map[v] = 0

    def pre_traverse(self, e, w, is_tree_edge):
        super().pre_traverse(e, w, is_tree_edge)

        if not is_tree_edge:
            self.highpt_map[w].append(e.get_other_vertex(w))

    def post_traverse(self, e, w):
        v = e.get_other_vertex(w)
        self.num_vertices -= 1
        self.num_tree_edges_map[v] += 1

    def post_visit(self, v, dfs_number, compl_number):
        self.lowpt1_num_map[v] = self.num_v_map[self.meta["DFS_LOWPT1_VERTEX"][v]]
        self.lowpt2_num_map[v] = self.num_v_map[self.meta["DFS_LOWPT2_VERTEX"][v]]


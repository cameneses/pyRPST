from abc import ABCMeta, abstractmethod
import copy
WHITE = 0
GRAY = 1
BLACK = 2

EDGE_NOT_VISITED = 0
TREE_EDGE = 1
BACK_EDGE = 2

INVALID_EDGE = None
INVALID_NODE = None

class DFS:

    __metaclass__ = ABCMeta

    def __init__(self, graph, container, adj_map):
        self.graph = graph
        self.adj_map = adj_map
        self.meta = container
        self.node_state_map = {}
        self.dfs_num_map = {}
        self.compl_num_map = {}
        self.edge_type_map = {}
        self.dfs_num = 0
        self.compl_num = 0
        self.is_new_path = True
        self.path_number =1
        self.parent_map = {}
        self.tree_arc_map = {}
        self.starts_new_path_map = {}
        self.path_num_map = {}

    def initialize(self):
        for node in self.graph.get_vertices():
            self.node_state_map[node] = WHITE
            self.dfs_num_map[node] = -1
            self.compl_num_map[node] = -1
            self.parent_map[node] = INVALID_NODE
            self.tree_arc_map[node] = INVALID_EDGE

        for edge in self.graph.get_edges():
            print(edge)
            self.edge_type_map[edge] = EDGE_NOT_VISITED
            self.path_num_map[edge] = -1
            self.starts_new_path_map[edge] = False

        self.meta["DFS_NUM"] = self.dfs_num_map
        self.meta["DFS_COMPL_NUM"] = self.compl_num_map
        self.meta["DFS_NODE_STATE"] = self.node_state_map
        self.meta["DFS_EDGE_TYPE"] = self.edge_type_map
        self.meta["DFS_PARENT"] = self.parent_map
        self.meta["DFS_PATH_NUMBER"] = self.path_num_map
        self.meta["DFS_STARTS_NEW_PATH"] = self.starts_new_path_map

    def start(self, root):
        self.dfs_num = 0
        self.compl_num = 0
        self.dfs(root)

    def dfs(self, v):
        self.dfs_num += 1
        self.dfs_num_map[v] = self.dfs_num
        self.node_state_map[v] = GRAY

        adj_v = copy.copy(self.adj_map[v])

        self.pre_visit(v, self.dfs_num_map[v])

        for e in adj_v:
            print("aaaaa")
            print(e)
            if (self.edge_type_map[e] == EDGE_NOT_VISITED):
                w = e.get_other_vertex(v)
                e.set_vertices(v, w)

                if (self.node_state_map[w] == WHITE):
                    self.edge_type_map[e] = TREE_EDGE

                    self.pre_traverse(e, w, True)

                    self.dfs(w)

                    self.post_traverse(e, w)

                else:
                    self.edge_type_map[e] = BACK_EDGE

                    self.pre_traverse(e, w, False)

        self.node_state_map[v] = BLACK
        self.compl_num += 1
        self.compl_num_map[v] = self.compl_num

        self.post_visit(v, self.dfs_num_map[v], self.compl_num_map[v])

    @abstractmethod
    def pre_traverse(self, e, w, is_tree_edge):
        v = e.get_other_vertex(w)
        if is_tree_edge:
            self.parent_map[w] = v
            self.tree_arc_map[w] = e
            self.path_num_map[e] = self.path_number

            if self.is_new_path:
                self.starts_new_path_map[e] = True
                self.is_new_path = False
        else:
            self.path_num_map[e] = self.path_number
            
            if self.is_new_path:
                self.starts_new_path_map[e] = True
            
            self.path_number += 1
            self.is_new_path = True

    @abstractmethod
    def post_traverse(self, e, w):
        pass

    @abstractmethod
    def pre_visit(self, v, dfs_number):
        pass

    @abstractmethod
    def post_visit(self, v, dfs_number, compl_number):
        pass


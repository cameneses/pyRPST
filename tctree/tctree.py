import math
from tctree.tcskeleton import TCSkeleton
from tctree.tctnode import TCTreeNode
from dfs import low_and_desc, number, split_components
from graph.directed_graph import DirectedGraph
import uuid 
TREE_EDGE = 1


class TCTree(DirectedGraph):

    def __init__(self, graph, back_edge):
        super().__init__()
        self.graph = graph
        self.back_edge = back_edge
        self.e2o = {}

    def construct(self):
        components = []
        virtual_edge_map = self.create_edge_map(self.graph)
        virtual_edge_map[self.back_edge] = True

        assigned_virtual_edge_map = self.create_edge_map(self.graph)
        is_hidden_map = self.create_edge_map(self.graph)

        container = {}
        container["VIRTUAL_EDGES"] = virtual_edge_map
        container["ASSIGNER_VIRTUAL_EDGES"] = assigned_virtual_edge_map
        container["HIDDEN_EDGES"] = is_hidden_map

        tcskeleton = TCSkeleton(self.graph, self.e2o)
        self.split_multitple_edges(
            tcskeleton, components, virtual_edge_map, assigned_virtual_edge_map, is_hidden_map)
        self.find_split_components(tcskeleton, components, virtual_edge_map,
                                   assigned_virtual_edge_map, is_hidden_map, self.back_edge.get_source(), container, self.back_edge.get_source())

        for el in components:
            if len(components) <= 1:
                continue
            node = TCTreeNode()
            for e in el:
                if virtual_edge_map[e]:
                    node.skeleton.add_virtual_edge(
                        e.get_source(), e.get_target(), e.get_id())
                else:
                    if e in self.e2o:
                        node.skeleton.add_edge_t(e.get_source(), e.get_target(), self.e2o[e])
                    else:
                        node.skeleton.add_edge_t(e.get_source(), e.get_target(), None)
            self.add_vertex(node)

        self.classify_components()

        ve2nodes = {}
        self.index_components(ve2nodes)

        self.merge_polgons_and_bonds(ve2nodes)

        # self.name_components()

        # self.construct_tree(ve2nodes)


    def create_edge_map(self, graph):
        edge_map = {}
        for e in graph.get_edges():
            edge_map[e] = False
        return edge_map

    def create_node_map(self, graph):
        node_map = {}
        for v in graph.get_vertices():
            node_map[v] = False
        return node_map

    def find_split_components(self, skeleton, components, vm, avm, hm, be, meta, root):
        adj_map = self.create_node_map(skeleton)
        for v in skeleton.get_vertices():
            adj=[]
            for e in skeleton.get_vertex_edges(v):
                adj.append(e) 
            adj_map[v] = adj

        meta["DFS_ADJ_LISTS"] = adj_map

        low_and_desc_dfs = low_and_desc.LowAndDesc(skeleton, meta, adj_map)
        low_and_desc_dfs.start(root)

        ordered_adj_map = self.order_adj_lists(skeleton, meta)

        copied_ordered_adj_map = {}
        for node in ordered_adj_map.keys():
            copied_ordered_adj_map[node] = ordered_adj_map[node].copy()

        number_dfs = number.Number(skeleton, meta, copied_ordered_adj_map)
        number_dfs.start(root)

        edge_count = {}
        for node in skeleton.get_vertices():
            edge_count[node] = len(skeleton.get_vertex_edges(node))

        meta["DFS_EDGE_COUNT"] = edge_count

        split_comp_dfs = split_components.SplitComponents(skeleton, meta,
                                                          copied_ordered_adj_map, components, hm, vm, avm)
        split_comp_dfs.add_dfs_maps(number_dfs.parent_map, number_dfs.tree_arc_map,
                                    number_dfs.highpt_map, number_dfs.edge_type_map)
        split_comp_dfs.initialize()
        split_comp_dfs.start(root)

    def order_adj_lists(self, graph, container):
        edges = graph.get_edges()
        bucket = []
        bucket_size = 3 * graph.count_vertices() + 2
        for _ in range(bucket_size):
            bucket.append([])
        for e in edges:
            phi = -1
            if container["DFS_EDGE_TYPE"][e] == TREE_EDGE:
                if container["DFS_LOWPT2_NUM"][e.get_target()] < container["DFS_NUM"][e.get_source()]:
                    phi = 3 * container["DFS_LOWPT1_NUM"][e.get_target()]
                else:
                    phi = 3 * container["DFS_LOWPT1_NUM"][e.get_target()] + 2
            else:
                phi = 3 * container["DFS_NUM"][e.get_target()] + 1

            bucket[phi - 1].append(e)

        ordered_adj_map = {}
        for node in graph.get_vertices():
            ordered_adj_map[node] = []

        container["DFS_ORDERED_ADJ_LISTS"] = ordered_adj_map

        for el in bucket:
            while len(el) > 0:
                e = el.pop()
                ordered_adj_map[e.get_source()].append(e)

        return ordered_adj_map

    def split_multitple_edges(self, skeleton, components, vm, avm, hm):
        edges = self.sort_consecutive_edges(skeleton)
        temp_comp = []
        last_edge, current_edge = None, None
        #temp_comp_size = 0
        for e in edges:
            current_edge = e
            if (last_edge):
                equal_source = current_edge.get_source() == last_edge.get_source()
                equal_target = current_edge.get_target() == last_edge.get_target()
                equal_s_t = current_edge.get_source() == last_edge.get_target()
                equal_t_s = last_edge.get_source() == current_edge.get_target()

                if equal_source and equal_target or equal_s_t and equal_t_s:
                    temp_comp.append(last_edge)
                    # temp_comp_size += 1
                else:
                    if len(temp_comp) > 0:
                        temp_comp.append(last_edge)
                        self.new_component(skeleton, components, temp_comp, vm,
                                           avm, hm, last_edge.get_source(), last_edge.get_target())
                        temp_comp = []
            last_edge = current_edge

        if len(temp_comp) > 0:
            temp_comp.append(last_edge)
            self.new_component(skeleton, components, temp_comp, vm,
                               avm, hm, last_edge.get_source(), last_edge.get_target())

    def new_component(self, skeleton, components, temp_comp, vm, avm, hm, s, t):
        for e in temp_comp:
            skeleton.remove_edge(e)
            hm[e] = True

        virtual_edge = skeleton.add_virtual_edge(s, t)
        vm[virtual_edge] = True
        temp_comp.insert(0, virtual_edge)

        for e in temp_comp:
            avm[e] = virtual_edge

        components.append(temp_comp)

    def sort_consecutive_edges(self, skeleton):
        indices = {}
        count = 1
        for v in self.graph.get_vertices():
            indices[v] = count
            count += 1

        edges = self.graph.get_edges()
        bucket = [[] for i in range(len(self.graph.get_vertices()))]

        for e in edges:
            i = min(indices[e.get_target()], indices[e.get_source()])
            bucket[i].append(e)

        sorted_edges = []
        for l in bucket:
            emap = {}
            for edge in l:
                i = indices[e.get_target()] + indices[e.get_source()]

                if not i in emap.keys():
                    el = []
                    el.append(edge)
                    emap[i] = el
                else:
                    emap[i].append(e)
                # if i in emap.keys():
                #     emap[i].append(e)
                # else:
                #     el = [edge]
                #     emap[i] = el
                #     emap[i].append(e)
            for el in emap.values():
                sorted_edges += el
        return sorted_edges

    def classify_components(self):
        for n in self.get_vertices():
            if n.skeleton.count_vertices() == 2:
                n.type = TCTreeNode.BOND
                continue

            is_polygon = True
            vs = n.skeleton.get_vertices()
            for v in vs:
                if len(n.skeleton.get_vertex_edges(v)) != 2:
                    is_polygon = False
                    break
            
            if is_polygon:
                n.type = TCTreeNode.POLYGON
            else:
                n.type = TCTreeNode.RIGID

    def index_components(self, ve2nodes):
        for node in self.get_vertices():
            for e in node.skeleton.get_virtual_edges():
                if e.get_tag() not in ve2nodes.keys():
                    nodes = set()
                    nodes.add(node)
                    ve2nodes[e] = nodes
                else:
                    ve2nodes[e].add(node)

    def merge_polgons_and_bonds(self, ve2nodes):
        to_remove = set()
        for key, value in ve2nodes.items():
            v1 = value[0]
            v2 = value[1]
            if v1.type != v2.type: continue
            if v1.type == TCTreeNode.RIGID: continue

            for e in v2.skeleton.get_edges():
                if v2.skeleton.is_virtual(e):
                    if e != key:
                        v1.skeleton.add_virtual_edge(
                            e.get_source(), e.get_target(), e.get_tag())
                    else:
                        v1.skeleton.add_edge(e.get_source(), e.get_target(
                            ), v2.skeleton.get_original_edge(e))
            
            ves = set(v1.skeleton.get_virtual_edges())
            for ve in ves:
                if ve == key:
                    v1.skeleton.remove_edge(ve)

            for i_key, i_value in ve2nodes.items():
                if v2 in i_value:
                    i_value.remove(v2)
                    i_value.add(v1)
                    if len(i_value) == 1:
                        to_remove.add(i_key)

            self.remove_vertex(v2)

        for ve in to_remove:
            del ve2nodes[ve]
            
    def name_components(self):
        namescomponets = {}
        Pc=0
        Bc=0
        Rc=0
        for node in self.get_vertices():
            if node.type==TCTreeNode.BOND:
                Bc = Bc+1
                namescomponets[node]=("B"+str(Bc))
            if node.type==TCTreeNode.POLYGON:
                Pc = Pc+1
                namescomponets[node]=("P"+str(Pc))
            if node.type==TCTreeNode.RIGID:
                Rc = Rc+1
                namescomponets[node]=("R"+str(Rc))
        return namescomponets     
    ##add construct_tree
    def construct_tree(self,ve2nodes,namescomponets):
        tobeRoot = None
        if len(self.get_vertices())==1:
            tobeRoot = iterator.HasNextIterator(self.get_vertices()).next()
        else:
            tobeRoot= None
            
        visited = set()
        for key, entry_1 in ve2nodes.items():
            i = iterator.HasNextIterator(entry_1)
            v1 = i.next()
            v2 = i.next()
            self.add_edge_abs(v1,v2)
            if tobeRoot is None and  v1 not in visited:
                if self.checkRoot(v1):
                    tobeRoot = v1
            visited.add(v1)
            if tobeRoot is None and v2 not in visited:
                if self.checkRoot(v2):
                    tobeRoot = v2
            visited.add(v2)
		#// construct trivial fragments
        for node in self.get_vertices():
            for edge in node.getSkeleton.get_original_edges():
                trivial = TCTreeNode()
                trivial.type = node = TCTreeNode.TCType.get("TRIVIAL")
                trivial.skeleton.add_edge_t(edge.get_source(), edge.get_target(), edge)
                namescomponets[trivial] = edge
                self.add_edge_abs(node,trivial)

        self.reRoot(tobeRoot)

import math
from tctree.tcskeleton import TCSkeleton
from tctree.tctnode import TCTreeNode
from dfs import low_and_desc, number, split_components
from graph.directed_graph import DirectedGraph
import uuid 
from collections import deque
from anytree import Node, RenderTree, AsciiStyle, PostOrderIter
import copy
TREE_EDGE = 1


class TCTree(DirectedGraph):

    def __init__(self, graph, back_edge):
        super().__init__()
        self.root = None
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
                if virtual_edge_map[e] and (e.get_source().name !="src" and e.get_target().name!="snk"):
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
        compo = self.name_components()
        tree,map_node = self.construct_tree(ve2nodes, compo)
        print(len(components))
        for pre, fill, node in RenderTree(tree):
            print("%s%s" % (pre, node.name))  
        for node in PostOrderIter(tree):
            print(node.name)
        return tree,map_node
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
            copied_ordered_adj_map[node] = copy.copy(ordered_adj_map[node])

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
        temp_comp_size = 0
        for e in edges:
            current_edge = e
            if last_edge != None:
                equal_source = current_edge.get_source() == last_edge.get_source()
                equal_target = current_edge.get_target() == last_edge.get_target()
                equal_s_t = current_edge.get_source() == last_edge.get_target()
                equal_t_s = last_edge.get_source() == current_edge.get_target()

                if (equal_source and equal_target) or (equal_s_t and equal_t_s):
                    temp_comp.append(last_edge)
                    temp_comp_size += 1
                else:
                    if temp_comp_size > 0:
                        temp_comp.append(last_edge)
                        self.new_component(skeleton, components, temp_comp, vm,
                                           avm, hm, last_edge.get_source(), last_edge.get_target())
                        temp_comp = []
                        temp_comp_size=0
            last_edge = current_edge

        if temp_comp_size > 0:
            temp_comp.append(last_edge)
            self.new_component(skeleton, components, temp_comp, vm,
                               avm, hm, last_edge.get_source(), last_edge.get_target())
        print("")
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
        count = 0
        for v in skeleton.get_vertices():
            indices[v] = count
            count += 1

        edges = skeleton.get_edges()
        bucket = [[] for i in range(len(skeleton.get_vertices()))]

        for e in edges:
            i = min(indices[e.get_source()],indices[e.get_target()])
            bucket[i].append(e)

        sorted_edges = []
        for l in bucket:
            emap = {}
            for edge in l:
                i = indices[edge.get_source()] + indices[edge.get_target()]
                el = []
                if not i in emap.keys():
                    el = None
                else:
                    el = emap[i]
                #if not i in emap.keys():
                if el == None:
                    el = []
                    el.append(edge)
                    emap[i] = el
                else:
                    el.append(edge)
                    #emap[i].append(e)
                # if i in emap.keys():
                #     emap[i].append(e)
                # else:
                #     el = [edge]
                #     emap[i] = el
                #     emap[i].append(e)
            for el in emap.values():
                if el !=None:
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
                if e.get_tag()=="":
                    continue
                if e.get_tag() not in ve2nodes.keys():
                    nodes = set()
                    nodes.add(node)
                    ve2nodes[e.get_tag()] = nodes
                else:
                    ve2nodes[e.get_tag()].add(node)
        print("")
    def merge_polgons_and_bonds(self, ve2nodes):
        to_remove = set()
        for key, value in ve2nodes.items():
            x = iter(value)
            v1 = next(x)
            v2 = next(x)
            if v1.type != v2.type: continue
            if v1.type == TCTreeNode.RIGID: continue

            for e in v2.skeleton.get_edges():
                if v2.skeleton.is_virtual(e):
                    if e.get_tag() != key:
                        v1.skeleton.add_virtual_edge(
                            e.get_source(), e.get_target(), e.get_tag())
                else:
                    v1.skeleton.add_edge_t(e.get_source(), e.get_target(
                            ), v2.skeleton.get_original_edge(e))
            
            ves = set(v1.skeleton.get_virtual_edges())
            for ve in ves:
                if ve.get_tag() == key:
                    v1.skeleton.remove_edge(ve)
                if ve.get_tag() =="":
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
                node.set_name("B"+str(Bc))
                namescomponets[node]=("B"+str(Bc))
            if node.type==TCTreeNode.POLYGON:
                Pc = Pc+1
                node.set_name("P"+str(Pc))
                namescomponets[node]=("P"+str(Pc))
            if node.type==TCTreeNode.RIGID:
                Rc = Rc+1
                node.set_name("R"+str(Rc))
                namescomponets[node]=("R"+str(Rc))
        return namescomponets   


    def re_root(self, v):
        if (v == None or not (v in self.get_vertices())) or v == self.root:
            return self.root
        self.root = v

        queue = deque()
        visited = set()
        queue.append(self.root)
        visited.add(self.root)

        while queue:
            c = queue.pop()
            adj_vertices = [x for x in self.get_adjacents(c) if x not in visited]
            for a in adj_vertices:
                self.remove_edges(self.get_edges(c, a))
                self.remove_edges(self.get_edges(a, c))
                self.add_edge_abs(c,a)
                visited.add(a)
                queue.append(a)
        
        return self.root

    def check_root(self, v):
        print(v.skeleton.get_original_edges())
        print(str(self.back_edge.get_source().name)+"->"+str(self.back_edge.get_target().name))
        for i in v.skeleton.get_original_edges():
            print(i)
            if self.back_edge.get_source().name == i.get_source().name and self.back_edge.get_target().name == i.get_target().name:
                return True
        return self.back_edge in v.skeleton.get_original_edges()

    def construct_tree(self,ve2nodes,namescomponets):
        to_be_root = self.get_vertices()[0] if len(self.get_vertices()) == 1  else None
            
        visited = set()
        for entry in ve2nodes.keys():
            i = iter(ve2nodes[entry])
            v1 = next(i)
            v2 = next(i)
            self.add_edge_abs(v1, v2)
            if to_be_root == None and v1 not in visited:
                if self.check_root(v1):
                    to_be_root = v1
            visited.add(v1)
            if to_be_root == None and v2 not in visited:
                if self.check_root(v2):
                    to_be_root = v2
            visited.add(v2)

        for node in self.get_vertices():
            for edge in node.get_skeleton().get_original_edges():
                trivial = TCTreeNode()
                trivial.type = TCTreeNode.TRIVIAL
                trivial.set_name=edge.get_name()
                trivial.skeleton.add_edge_t(edge.get_source(), edge.get_target(), edge)
                namescomponets[trivial] = edge.get_name()
                self.add_edge_abs(node,trivial)
        
        root= Node(to_be_root.name)
        Q = []
        Q.append(to_be_root.name)
        Qr = []
        Qr.append(to_be_root.name)
        map_node = {}
        map_node[to_be_root.name]=root
        while len(Q)>0:
            tag = Q.pop(0)
            for node in self.get_edges():
                if node.get_source().get_name() == tag and node.get_target().get_name() not in Qr:
                    if namescomponets[node.get_target()] !="":
                        Q.append(namescomponets[node.get_target()])
                        Qr.append(namescomponets[node.get_target()])
                        r = Node(namescomponets[node.get_target()], parent=map_node[node.get_source().get_name()])
                        map_node[namescomponets[node.get_target()]] = r
                        
                    else:
                        marc = Node(node.get_target(), parent=map_node[node.get_source().get_name()])
                        map_node[namescomponets[node.get_target()]] = marc
                if node.get_target().get_name() == tag and node.get_source().get_name() not in Qr:
                    if namescomponets[node.get_source()] !="":
                        Q.append(namescomponets[node.get_source()])
                        Qr.append(namescomponets[node.get_source()])
                        r = Node(namescomponets[node.get_source()], parent=map_node[node.get_target().get_name()])
                        map_node[namescomponets[node.get_source()]] = r
                        
                    else:
                        marc = Node(node.get_source(), parent=map_node[node.get_target().get_name()])
                        map_node[namescomponets[node.get_source()]] = marc
        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.name))  
        return [root,map_node]
         
             #   marc = Node("Marc", parent=udo)
            #nt("Source: "+str(node.get_source().get_name())+str("-")+str(node.get_source()) +" Target: "+str(node.name)+str("-")+str(node.get_target()))
        self.re_root(to_be_root)

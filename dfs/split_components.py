from dfs.dfs import DFS
import uuid

INVALID_NODE = None

TREE_EDGE = 1


def retain_all(l1, l2):
    lf = []
    for elem in l1:
        if elem in l2:
            lf.append(elem)
    return lf


class SplitComponents(DFS):

    def __init__(self, graph, meta, adj_map, components, hidden_map, virt_edge_map, assigned_virt_edge_map):
        super().__init__(graph, meta, adj_map)
        self.components = components
        self.hidden_map = hidden_map
        self.virt_edge_map = virt_edge_map
        self.assigned_virt_edge_map = assigned_virt_edge_map
        self.edge_stack = []
        self.ts_stack = []
        self.EOS = TSItem(-1, -1, -1, INVALID_NODE, INVALID_NODE)

    def add_dfs_maps(self, parent_map, tree_arc_map, higpt_map, edge_type_map):
        self.parent_map = parent_map
        self.tree_arc_map = tree_arc_map
        self.highpt_map = higpt_map
        self.edge_type_map = edge_type_map

    def initialize(self):
        super().initialize()
        self.num_not_visited_tree_edges = {}

        for node in self.graph.get_vertices():
            self.num_not_visited_tree_edges[node] = self.meta["DFS_NUM_TREE_EDGES"][node]
            self.parent_map[node] = self.meta["DFS_PARENT"][node]
            self.meta["DFS_ADJ_LISTS"][node] = retain_all(
                self.meta["DFS_ADJ_LISTS"][node], self.adj_map[node])

    def start(self, root):
        self.dfs_root = root
        self.ts_stack.append(self.EOS)
        super().start(root)

        if len(self.edge_stack) > 0:
            self.new_component(self.edge_stack)

    def pre_traverse(self, e, w, is_tree_edge):
        super().pre_traverse(e, w, is_tree_edge)
        v = e.get_other_vertex(w)

        self.num_not_visited_tree_edges[v] = self.num_not_visited_tree_edges[v] - 1

        if self.meta["DFS_STARTS_NEW_PATH"][e]:
            self.update_ts_stack(v, w, is_tree_edge)

        if not is_tree_edge:
            if w == self.parent_map[v]:
                el = [e, self.tree_arc_map[v]]
                component = self.new_component(el)
                virtual_edge = self.new_virtual_edge(component, w, v)

                for edge in component:
                    self.assigned_virt_edge_map[edge] = virtual_edge
                self.make_tree_edge(virtual_edge, w, v)
            else:
                self.edge_stack.append(e)

    def post_traverse(self, e, w):
        v = e.get_other_vertex(w)

        if self.hidden_map[e]:
            edge_to_push = self.assigned_virt_edge_map[e]
            while self.hidden_map[edge_to_push]:
                edge_to_push = self.assigned_virt_edge_map[edge_to_push]
            #Revisar si es correcta la identación que tenia.
            self.edge_stack.append(edge_to_push)
        else:
            self.edge_stack.append(e)
        print("e: "+str(e))
        print("v: "+str(v))
        print("w: "+str(w))
        self.check_type_2(e, v, w)
        self.check_type_1(e, v, w)
        
        if self.meta["DFS_STARTS_NEW_PATH"][e]:
            while len(self.ts_stack) > 0 and self.EOS != self.ts_stack[-1]:
                self.ts_stack.pop()
            if len(self.ts_stack) > 0:
                self.ts_stack.pop()

        if len(self.ts_stack) > 0:
            i = self.ts_stack[-1]
            high_v = self.get_h_num(v)
            while i != self.EOS and i.a != v and i.b != v and high_v > i.num_h:
                self.ts_stack.pop()
                i = self.ts_stack[-1]

    def check_type_1(self, edge_backtrack, v, w):
        # More descriptive names for variables
        cond1 = self.get_l2_num(w) >= self.get_num(v)
        cond2 = self.get_l1_num(w) < self.get_num(v)
        cond3 = (
            self.parent_map[v] != self.dfs_root or self.num_not_visited_tree_edges[v] > 0)
        if cond1 and cond2 and cond3:
            lowpt1_w = self.meta["DFS_LOWPT1_VERTEX"][w]
            print("edge_backtrack: "+str(edge_backtrack))
            component = self.new_component([])
            num_w = self.get_num(w)
            h = num_w + self.get_num_desc(w) - 1
            if len(self.edge_stack) > 0:
                e = self.edge_stack[-1]
            while len(self.edge_stack) > 0 and ((num_w <= self.get_num(e.get_source()) and self.get_num(e.get_source()) <= h) or (num_w <= self.get_num(e.get_target()) and self.get_num(e.get_target()) <= h)):
                e = self.edge_stack.pop()
                print("edge_backtrack: "+str(edge_backtrack))
                print("e: "+str(e))
                print("component")
                for ii in component:
                    print(ii)
                component = self.add_to_component([e], component)
                if len(self.edge_stack) > 0:
                    e = self.edge_stack[-1]

            virtual_edge = self.new_virtual_edge(component, v, lowpt1_w)
            for edge in component:
                self.assigned_virt_edge_map[edge] = virtual_edge

            if len(self.edge_stack) > 0:
                e = self.edge_stack[-1]
                if self.is_same_edge(e, v, lowpt1_w):
                    e = self.edge_stack.pop()
                    el = [e, virtual_edge]
                    component = self.new_component(el)
                    virtual_edge = self.new_virtual_edge(
                        component, v, lowpt1_w)

                    for edge in component:
                        self.assigned_virt_edge_map[edge] = virtual_edge

            if lowpt1_w != self.parent_map[v]:
                self.edge_stack.append(virtual_edge)
            else:
                tree_arc_of_v = self.tree_arc_map[v]
                el = [tree_arc_of_v]
                el.append(virtual_edge)
                component = self.new_component(el)
                virtual_edge = self.new_virtual_edge(component, lowpt1_w, v)
                for edge in component:
                    self.assigned_virt_edge_map[edge] = virtual_edge
                self.tree_arc_map[v] = virtual_edge

            self.meta["DFS_ORDERED_ADJ_LISTS"][v].append(virtual_edge)
            self.make_tree_edge(virtual_edge, lowpt1_w, v)

    def check_type_2(self, edge_backtrack, v, w):
        top_triple = None
        if len(self.ts_stack) > 0:
            top_triple = self.ts_stack[-1]
        adj_of_w = self.meta["DFS_ORDERED_ADJ_LISTS"][w]
        first_child_of_w = None
        if len(adj_of_w) > 0:
            first_child_of_w = adj_of_w[-1].get_other_vertex(w)
        edge_count_of_w = self.meta["DFS_EDGE_COUNT"][w]
        while (v != self.dfs_root) and (((top_triple != None) and (top_triple.a == v)) or (
            (edge_count_of_w == 2) and (first_child_of_w != None) and (self.get_num(
                first_child_of_w) > self.get_num(w)))):
            e_a_b = []
            if top_triple.a == v and self.parent_map[top_triple.b] == top_triple.a:
                self.ts_stack.pop()
                if len(self.ts_stack) > 0:
                    top_triple = self.ts_stack[-1]
                else:
                    top_triple = None
            else:
                component = self.new_component([])
                virtual_edge = None

                if edge_count_of_w == 2 and first_child_of_w != None and (
                        self.get_num(first_child_of_w) > self.get_num(w)):
                    el = [self.edge_stack.pop()]
                    el.append(self.edge_stack.pop())
                    print("el")
                    for iii in el:
                        print(iii)
                    print("component")
                    for ii in component:
                        print(ii)
                    self.add_to_component(el, component)
                    virtual_edge = self.new_virtual_edge(
                        component, v, first_child_of_w)

                    for edge in component:
                        self.assigned_virt_edge_map[edge] = virtual_edge

                    if len(self.edge_stack) > 0:
                        e = self.edge_stack[-1]
                        if self.is_same_edge(e, v, top_triple.b) or self.is_same_edge(e, v, first_child_of_w):
                            e_a_b.append(self.edge_stack.pop())
                else:
                    top_triple = self.ts_stack.pop()
                    e = None
                    if len(self.edge_stack) > 0:
                        e = self.edge_stack[-1]
                    while (e != None) and (top_triple.num_a <= self.get_num(e.get_source())) and (
                        top_triple.num_a <= self.get_num(e.get_target())) and (
                        self.get_num(e.get_source()) <= top_triple.num_h) and (
                            self.get_num(e.get_target()) <= top_triple.num_h):

                        e = self.edge_stack.pop()
                        if self.is_same_edge(e, top_triple.a, top_triple.b):
                            e_a_b.append(e)
                        else:
                            component = self.add_to_component([e], component)

                        if len(self.edge_stack) > 0:
                            e = self.edge_stack[-1]
                        else:
                            e = None
                    
                    virtual_edge = self.new_virtual_edge(component, top_triple.a, top_triple.b)  
                    for e in component:
                        self.assigned_virt_edge_map[e] = virtual_edge

                if len(e_a_b) > 0:
                    e_a_b.append(virtual_edge)
                    print("e_a_b")
                    for ii in e_a_b:
                        print(ii)
                    component = self.new_component(e_a_b)
                    b=None
                    if top_triple.b == INVALID_NODE or (
                        first_child_of_w != None and self.is_same_edge(e_a_b[-1], v, first_child_of_w)):
                        b = first_child_of_w
                    else:
                        b = top_triple.b 
                    virtual_edge = self.new_virtual_edge(component, v, b)
                    for edge in component:
                        self.assigned_virt_edge_map[edge] = virtual_edge

                self.edge_stack.append(virtual_edge)
                w = virtual_edge.get_other_vertex(v)
                self.make_tree_edge(virtual_edge, v, w)
                self.parent_map[w] = v

                if len(self.ts_stack) > 0:
                    top_triple = self.ts_stack[-1]
                else:
                    top_triple = None

                adj_of_w = self.meta["DFS_ORDERED_ADJ_LISTS"][w]
                if len(adj_of_w) > 0:
                    first_child_of_w = adj_of_w[-1].get_other_vertex(w)
                edge_count_of_w = self.meta["DFS_EDGE_COUNT"][w]


    def is_same_edge(self, e, v, w):
        if (e.get_source() == v and e.get_target() == w) or (
                e.get_source() == w and e.get_target() == v):
            return True
        return False

    def add_to_component(self, component_edges, component):
        self.remove_edges(component_edges)
        component += component_edges
        return component

    def new_virtual_edge(self, component, v, w):
        asd = w
        virtual_edge = self.graph.add_virtual_edge(v, w)
        virtual_edge.set_id(uuid.uuid1())
        self.update_edge_count(v, 1)
        self.update_edge_count(w, 1)
        self.virt_edge_map[virtual_edge] = True
        component.insert(0, virtual_edge)
        self.meta["DFS_ORDERED_ADJ_LISTS"][v].append(virtual_edge)
        return virtual_edge

    def make_tree_edge(self, e, v, w):
        e.set_vertices(v, w)
        self.edge_type_map[e] = TREE_EDGE

    def update_ts_stack(self, v, w, is_tree_edge):
        last_removed = None
        y = -1
        if is_tree_edge:
            ts_len = len(self.ts_stack)

            ts_not_empty = ts_len > 0
            top_different_EOS = self.ts_stack[ts_len - 1] != self.EOS
            num_a_greater = self.ts_stack[ts_len -
                                          1].num_a > self.get_l1_num(w)
            while ts_not_empty and top_different_EOS and num_a_greater:
                last_removed = self.ts_stack.pop()
                if last_removed.num_h > y:
                    y = last_removed.num_h
                ts_len = len(self.ts_stack)
                ts_not_empty = ts_len > 0
                top_different_EOS = self.ts_stack[ts_len - 1] != self.EOS
                num_a_greater = self.ts_stack[ts_len -1].num_a > self.get_l1_num(w)

            if last_removed == None:
                num_h = self.get_num(w) + self.get_num_desc(w) - 1
                lowpt_vertex = self.meta["DFS_LOWPT1_VERTEX"][w]
                item_to_push = self.create_ts_item(num_h, lowpt_vertex, v)
            else:
                num_h = max(y, self.get_num(w) + self.get_num_desc(w) - 1)
                lowpt_vertex = self.meta["DFS_LOWPT1_VERTEX"][w]
                item_to_push = self.create_ts_item(
                    num_h, lowpt_vertex, last_removed.b)

            self.ts_stack.append(item_to_push)
            self.ts_stack.append(self.EOS)

            #ts_not_empty = ts_len > 0
            #top_different_EOS = self.ts_stack[ts_len - 1] != self.EOS
            #num_a_greater = self.ts_stack[ts_len -1].num_a > self.get_l1_num(w)

        else:
            ts_len = len(self.ts_stack)

            ts_not_empty = ts_len > 0
            top_different_EOS = self.ts_stack[ts_len - 1] != self.EOS
            num_a_greater = self.ts_stack[ts_len - 1].num_a > self.get_num(w)

            while ts_not_empty and top_different_EOS and num_a_greater:
                last_removed = self.ts_stack.pop()
                if last_removed.num_h > y:
                    y = last_removed.num_h
                
                ts_len = len(self.ts_stack)
                ts_not_empty = ts_len > 0
                top_different_EOS = self.ts_stack[ts_len - 1] != self.EOS
                num_a_greater = self.ts_stack[ts_len -
                                              1].num_a > self.get_num(w)

            if last_removed == None:
                item_to_push = self.create_ts_item(self.get_num(v), w, v)
            else:
                item_to_push = self.create_ts_item(y, w, last_removed.b)
            self.ts_stack.append(item_to_push)

    def new_component(self, component_edges):
        self.remove_edges(component_edges)
        self.components.append(component_edges)
        return component_edges

    def remove_edges(self, edges):
        for e in edges:
            adj = self.meta["DFS_ORDERED_ADJ_LISTS"][e.get_source()]
            if len(adj) > 0:
                if e in adj:
                    adj.remove(e)
            try:
                self.graph.remove_edge(e)
                self.update_edge_count(e.get_source(), -1)
                self.update_edge_count(e.get_target(), -1)
                self.hidden_map[e] = True
            except ValueError:
                print("Edge already removed")

    def update_edge_count(self, node, i):
        self.meta["DFS_EDGE_COUNT"][node] = self.meta["DFS_EDGE_COUNT"][node] + i

    def get_num(self, node):
        return self.meta["DFS_NUM_V"][node]

    def get_num_desc(self, node):
        return self.meta["DFS_NUM_DESC"][node]

    def get_l1_num(self, node):
        return self.meta["DFS_LOWPT1_NUM"][node]

    def get_l2_num(self, node):
        return self.meta["DFS_LOWPT2_NUM"][node]

    def get_h_num(self, node):
        if len(self.highpt_map[node]) > 0:
            return self.get_num(self.highpt_map[node][0])
        else:
            return 0

    def create_ts_item(self, num_h, a, b):
        num_a = self.get_num(a)
        num_b = self.get_num(b)
        return TSItem(num_h, num_a, num_b, a, b)


class TSItem:

    def __init__(self, num_h, num_a, num_b, a, b):
        self.a = a
        self.b = b
        self.num_h = num_h
        self.num_a = num_a
        self.num_b = num_b

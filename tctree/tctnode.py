from tctree.tcskeleton import TCSkeleton


class TCTreeNode:
    TRIVIAL = 1
    POLYGON = 2
    BOND = 3
    RIGID = 4
    UNDEFINED = 5

    def __init__(self):
        self.type = TCTreeNode.UNDEFINED
        self.skeleton = TCSkeleton()
        self.name =""
    def getType(self):
        return self.type
    def get_skeleton(self):
        return self.skeleton
    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name =name
    def __str__(self):
        edges = ''
        for e in self.skeleton.get_edges():
            edges += '{} -> {} '.format(e.get_source(), e.get_target())
        return edges
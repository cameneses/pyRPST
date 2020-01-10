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

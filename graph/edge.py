class Edge:

    def __init__(self, source, target):
        self.source = ""
        self.target = ""
        self.set_vertices(source,target)
        self.tag = ""
        self.id = ""
        self.name = ""

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def has_source(self, v):
        return self.source == v

    def has_target(self, v):
        return self.target == v

    def set_vertices(self, v, w):
        self.source = v
        self.target = w

    def get_other_vertex(self, v):
        if v == self.source:
            return self.target
        elif v == self.target:
            return self.source
        else:
            return None
    def set_name(self,name):
        self.name=name
        
    def get_name(self):
        return self.name
    def contains(self, v):
        return self.has_target(v) or self.has_source(v)

    def __str__(self):
        return "{} -> {}".format(self.source, self.target)

    def set_id(self,idd):
        self.id = idd

    def get_id(self):
        return self.id

    def set_tag(self,tag):
        self.tag = tag

    def get_tag(self):
        return self.tag

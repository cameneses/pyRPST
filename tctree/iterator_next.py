class HasNextIterator:
    def __init__(self, it):
        self._it = iter(it)
        self._next = None
 
    def __iter__(self):
        return self
 
    def has_next(self):
        if self._next:
            return True
        try:
            self._next = next(self._it)
            return True
        except StopIteration:
            return False
 
    def next(self):
        if self._next:
            ret = self._next
            self._next = None
            return ret
        elif self.has_next():
            return self.next()
        else:
            raise StopIteration()

class LinkedNode:
    __slots__ = ['elem', 'next', 'back']
    def __init__(self, elem, back=None, next=None):
        self.elem = elem
        self.next = next
        self.back = back

    def isfirst(self):
        return False

    def islast(self):
        return False

class HeadNode:
    def __init__(self):
        self.next = None

    def isfirst(self):
        return True

class LastNode:
    def __init__(self):
        self.back = None

    def isfirst(self):
        return False

    def islast(self):
        return True

class LinkedList:
    def __init__(self):
        self.head = HeadNode()
        self.last = LastNode()
        self.head.next = self.last
        self.last.back = self.head

    def expand(self, elems):
        for ind in elems:
            self.append(ind)

    def append(self, elem):
        lnode = LinkedNode(elem, self.last.back, self.last)
        self.last.back.next = lnode
        self.last.back = lnode
        return lnode

    def appendleft(self, elem):
        lnode = LinkedNode(elem, self.head, self.head.next)
        self.head.next.back = lnode
        self.head.next = lnode
        return lnode

    def sub(self, index, lindex, elem):
        lnode = LinkedNode(elem, index.back, lindex)
        index.back.next = lnode
        lindex.back = lnode

    def insert(self, index, elem):
        lnode = LinkedNode(elem, index.back, index)
        index.back.next = lnode
        index.back = lnode
        return lnode

    def next(self, index):
        if index is self.last:
            return index
        else:
            return index.next

    def items(self, index, lindex):
        while index != lindex:
            yield index.elem
            index = index.next

    def back(self, index):
        if index.back is self.head:
            return index
        else:
            return index.back

    def delete(self, index, lindex):
        index.back.next = lindex
        lindex.back = index.back

    def empty(self):    
        return self.head.next == self.last

    def first(self):
        return self.head.next

    def __str__(self):
        data = self.items(self.head.next, self.last)
        data = list(data)
        return data.__str__()

    __repr__ = __str__


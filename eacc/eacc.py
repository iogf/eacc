from eacc.token import PTree, Sof, Eof, Token, TokType
from eacc.llist import LinkedList, Slice
from itertools import chain

class EaccError(Exception):
    pass

class Grammar:
    pass

class SymNode:
    def __init__(self):
        self.kmap = {}
        self.ops  = []

    def runops(self, eacc, data):
        for ind in self.ops:
            node  = ind.opexec(eacc, data)
            if node:
                return node

    def match(self, eacc, data=[]):
        token = eacc.tell()
        if not token:
            return self.runops(eacc, data)

        node = self.kmap.get(token.type)
        if not node:
            return self.runops(eacc, data)

        eacc.seek()
        node = node.match(eacc, data + [token])
        if node:
            return node

    def append(self, op):
        node = OpNode(op)
        self.ops.append(node)
        return node

    def __repr__(self):
        return self.kmap.__repr__()

class OpNode(SymNode):
    def __init__(self, op):
        super(OpNode, self).__init__()
        self.op = op

    def opexec(self, eacc, data):
        index = eacc.index
        token = self.op.opexec(eacc, data)

        if token:
            node = self.match(eacc, data + [token])
            if node:
                return node
        eacc.index = index

class SymTree(SymNode):
    def __init__(self, rules=[]):
        super(SymTree, self).__init__()
        self.rules = []

        for ind in rules:
            self.update(ind)

    def update(self, rule):
        pattern = iter(rule.args)
        node = self

        for ind in pattern:
            if not isinstance(ind, T):
                node = node.kmap.setdefault(ind, SymNode())
            else:
                node = node.append(ind)
        node.ops.append(rule)
        self.rules.append(rule)

class Eacc:
    def __init__(self, grammar, no_errors=False):
        self.root = grammar.root
        self.no_errors = no_errors
        self.symtree = SymTree(self.root)
        self.index  = None
        self.llist = LinkedList()
        self.hpos = None
        self.handles = {}

    def reset(self):
        self.index = self.llist.first()
        self.hpos = self.index

    def seek(self):
        self.index = self.llist.next(self.index)

    def get(self):
        if self.index == self.llist.last:
            return None

        elem = self.index.elem
        self.index = self.index.next
        return elem

    def shift(self):
        self.hpos = self.llist.next(self.hpos)
        self.index = self.hpos

    def lseek(self):
        if self.index != self.llist.head:
            self.index = self.index.back

    def tell(self):
        if self.index != self.llist.last:
            return self.index.elem

    def items(self):
        index = self.hpos
        while index != self.index:
            yield index.elem
            index = index.next

    def build(self, tseq):
        """
        """

        tseq = chain((Token('', Sof), ), 
        tseq, (Token('', Eof), ))

        self.llist.expand(tseq)
        self.index = self.llist.first()
        self.hpos  = self.index

        ptree = self.process()
        yield from ptree

        if not self.llist.empty() and not self.no_errors:
            self.handle_error(self.llist)

    def process(self):
        match = self.symtree.match

        while True:
            ptree = match(self)
            if ptree:
                self.reduce(ptree)
                yield ptree
            elif self.hpos.islast():
                break
            else:
                self.shift()

    def reduce(self, ptree):
        if ptree.type:
            self.llist.sub(self.hpos, self.index, ptree)
        else:
            self.llist.delete(self.hpos, self.index)
        self.reset()

    def extend(self, *rules):
        pass

    def handle_error(self, tokens):
        """
        """
        print('Crocs Eacc error!')
        print('Tokens:', tokens)
        raise EaccError('Unexpected struct!')

    def add_handle(self, rule, handle):
        """
        """

        self.handles[rule] = handle

    def del_handle(self, rule):
        """
        """

        del self.handles[rule] 

class Rule(TokType):
    def __init__(self, *args, up=(), type=None):
        """
        """
        self.args = args
        self.type = type
        self.up   = []

        self.up.extend(up)

    def startswith(self, eacc):
        for ind in self.args:
            token = ind.opexec(eacc)
            if not token:
                return False
        return True

    def precedence(self, eacc):
        for ind in self.up:
            index = eacc.index
            prec = ind.startswith(eacc)
            if prec:
                return False
            eacc.index = index
        return True
 
    def opexec(self, eacc, data):
        valid = self.precedence(eacc)
        if not valid: 
            return None

        ptree = PTree(self.type)
        ptree.extend(data)
        # print('ptree', ptree)
        # print('args:', self.args)
        # print(ptree)
        hmap = eacc.handles.get(self, None)
        if hmap:
            ptree.result = hmap(*ptree)
        return ptree

class T(TokType):
    def __init__(self, token, min=1, max=None):
        self.token = token
        self.min = min

        self.max = max

    def opexec(self, eacc, data):
        token = self.token
        ptree = PTree(None)

        while True:
            result = token.opexec(eacc, data)
            if not result:
                if self.max:
                    if self.min <= len(ptree) <= self.max:
                        return ptree
                if self.min <= len(ptree):
                    return ptree
            ptree.append(result)


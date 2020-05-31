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

    def validate(self, llist):
        for ind in self.ops:
            node  = ind.match(llist)
            if node:
                return node

        token = llist.get()
        if token:
            node  = self.kmap.get(token.type)
            if node:
                return node.match(llist)
        llist.lseek()

    def match(self, llist):
        index = llist.index
        token = self.validate(llist)
        if token:
            return token
        else:
            llist.index = index

    def __repr__(self):
        return self.kmap.__repr__()

class OpNode(SymNode):
    def __init__(self, op):
        self.op = op
        self.nodes = SymNode()

    def validate(self, llist):
        token = self.op.validate(llist)
        if token:
            return token

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
            node = node.kmap.setdefault(ind, SymNode())
        node.ops.append(rule)
        self.rules.append(rule)

class Eacc:
    def __init__(self, grammar, no_errors=False):
        self.root = grammar.root
        self.no_errors = no_errors
        self.symtree = SymTree(self.root)
        self.index  = None
        self.llist = LinkedList()

    def reset(self):
        self.index = self.llist.first()

    def seek(self):
        self.index = self.llist.next(self.index)

    def tell(self):
        return self.index

    def build(self, tseq):
        """
        """

        tseq = chain((Token('', Sof), ), 
        tseq, (Token('', Eof), ))

        self.llist.expand(tseq)
        self.index = self.llist.first()

        ptree = self.process()
        yield from ptree

        if not self.llist.empty() and not self.no_errors:
            self.handle_error(self.llist)

    def process(self):
        while True:
            lslc  = Slice(self.index, self.llist.last)
            ptree = self.symtree.match(lslc)
            if ptree:
                self.reduce(lslc.index, ptree)
                yield ptree
            elif self.index.islast():
                break
            else:
                self.seek()

    def reduce(self, lindex, ptree):
        self.llist.delete(self.index, lindex)

        if ptree.type:
            self.llist.insert(lindex, ptree)
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
        rule.hmap = handle

    def del_handle(self, rule, handle):
        """
        """
        rule.hmap = handle

class Rule(TokType):
    def __init__(self, *args, up=(), type=None):
        """
        """
        self.args = args
        self.type = type
        self.hmap = None
        self.up   = []

        self.up.extend(up)

    def startswith(self, llist):
        for ind in self.args:
            token = ind.validate(llist)
            if not token:
                return False
        return True

    def precedence(self, llist):
        for ind in self.up:
            slc = Slice(llist.index, llist.last)
            prec = ind.startswith(slc)
            if prec:
                return False
        return True
 
    def match(self, llist):
        valid = self.precedence(llist)
        if not valid: 
            return None

        ptree = PTree(self.type)
        ptree.extend(llist.items())
        # print('ptree', ptree)
        # print('args:', self.args)

        if self.hmap:
            ptree.result = self.hmap(*ptree)

        return ptree

class T:
    def __init__(self, token, min=1, max=9999999999999):
        self.token = token
        self.min = min

        self.max = max

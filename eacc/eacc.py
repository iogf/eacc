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

    def validate(self, eacc):
        for ind in self.ops:
            node  = ind.match(eacc)
            if node:
                return node

        token = eacc.get()
        if token:
            node  = self.kmap.get(token.type)
            if node:
                return node.match(eacc)
        # llist.lseek()

    def match(self, eacc):
        index = eacc.index
        token = self.validate(eacc)
        if token:
            return token
        else:
            eacc.index = index

    def __repr__(self):
        return self.kmap.__repr__()

class OpNode(SymNode):
    def __init__(self, op):
        self.op = op
        self.nodes = SymNode()

    def validate(self, eacc):
        token = self.op.validate(eacc)
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
        self.hpos = None

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
        return self.index

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
        while True:
            ptree = self.symtree.match(self)
            if ptree:
                self.reduce(ptree)
                yield ptree
            elif self.hpos.islast():
                break
            else:
                self.shift()

    def reduce(self, ptree):
        self.llist.delete(self.hpos, self.index)

        if ptree.type:
            self.llist.insert(self.index, ptree)
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

    def startswith(self, eacc):
        for ind in self.args:
            token = ind.validate(eacc)
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
 
    def match(self, eacc):
        valid = self.precedence(eacc)
        if not valid: 
            return None

        ptree = PTree(self.type)
        ptree.extend(eacc.items())
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

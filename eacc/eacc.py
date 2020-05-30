from eacc.token import PTree, Sof, Eof, Token, TokType
from eacc.llist import LinkedList, Slice
from itertools import chain

class EaccError(Exception):
    pass

class Grammar:
    pass

class SymTree:
    def __init__(self, rules=[]):
        self.rules = rules
        self.nodes = []

        for ind in rules:
            self.update(chain(iter(ind.args), (ind, )))
        # print(self.nodes)

    def match(self, llist):
        for ind in self.nodes:
            index = llist.index
            token = ind.validate(llist)
            if token:
                return token
            else:
                llist.index = index

    def update(self, pattern):
        op = next(pattern, None)
        if not op:
            return None

        for ind in self.nodes:
            if ind.istype(op):
                return ind.update(pattern)
        node = OpNode(op)
        self.nodes.append(node)
        node.update(pattern)

class OpNode(SymTree):
    def __init__(self, op):
        self.nodes = []
        self.op = op
        self.istype = op.istype

    def validate(self, llist):
        token = self.op.validate(llist)
        if not token: 
            return None

        if not self.nodes:
            return token

        return self.match(llist)

    def __repr__(self):
        return '(Op: %s\nChildren:%s)' % (repr(self.op), repr(self.nodes))

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
 
    def validate(self, llist):
        valid = self.precedence(llist)
        if not valid: 
            return None

        ptree = PTree(self.type)
        ptree.extend(llist.items())
        if self.hmap:
            ptree.result = self.hmap(*ptree)

        # print('ptree', ptree)
        # print('args:', self.args)
        return ptree

class T:
    def __init__(self, token, min=1, max=9999999999999):
        self.token = token
        self.min = min

        self.max = max

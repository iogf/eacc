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
        self.stack = []
        self.data  = []

        for ind in rules:
            self.update(chain(iter(ind.args), (ind, )))

    def match(self, llist, data=[]):
        self.stack.clear()
        self.data.clear()
        seq = self.find_opnode(llist, self.data)
        self.stack.append(seq)

        while True:
            seq = self.stack[-1]
            opnode, token = next(seq, (None, None))

            if opnode:
                if not opnode.nodes:
                    return token
                seq = opnode.find_opnode(llist, self.data)
                self.stack.append(seq)
                self.data.append(token)
            elif self.stack and len(self.stack) > 1:
                seq = self.stack.pop()
                if self.data:
                    self.data.pop()
            else:
                break

    def find_opnode(self, llist, data):
        index = llist.index
        for ind in self.nodes:
            token = ind.op.validate(llist, data)
            if token:
                yield (ind, token)
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
        if self.index != self.llist.last:
            self.index = self.index.next

    def get(self):
        if self.index == self.llist.last:
            return None
        else:
            self.index.elem

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

    def startswith(self, llist, data):
        for ind in self.args:
            token = ind.validate(llist, data)
            if not token:
                return False
        return True

    def precedence(self, llist, data):
        for ind in self.up:
            slc = Slice(llist.index, llist.last)
            prec = ind.startswith(slc, data)
            if prec:
                return False
        return True
 
    def validate(self, llist, data):
        valid = self.precedence(llist, data)
        if not valid: 
            return None
        # print(data)
        ptree = PTree(self.type)
        ptree.extend(data)
        ptree.eval(self.hmap)
        return ptree

class T:
    def __init__(self, token, min=1, max=9999999999999):
        self.token = token
        self.min = min

        self.max = max

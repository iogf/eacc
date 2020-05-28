from eacc.token import PTree, Sof, Eof, Token
from eacc.llist import LinkedList
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
            self.update(ind)

    def consume(self, llist):
        data = []
        for ind in self.nodes:
            data = ind.process(data, llist)
            if data:
                return data

    def update(self, rule):
        pattern = iter(rule.args)
        op = next(pattern)

        for ind in self.nodes:
            if ind.is_equal(op):
                return ind.append(op, pattern, rule)

        node = OpNode(op)
        node.append(pattern)
        self.nodes.append(node)
        return node

class OpNode:
    def __init__(self, op):
        self.op = op
        self.kmap = []

    def process(self, data, llist):
        self.consume(data, llist)

    def consume(self, data, llist):
        for ind in self.nodes:
            data = ind.process(data, llist)
            if data:
                return data

    def append(self, pattern):
        op = next(pattern)
        for ind in self.nodes:
            if ind.is_equal(op):
                return ind.append(op, pattern)

class Eacc:
    def __init__(self, grammar, no_errors=False):
        self.root = grammar.root
        self.no_errors = no_errors
        self.symtree = SymTree(self.root)

    def build(self, tseq):
        """
        """

        tseq = chain((Token('', Sof), ), 
        tseq, (Token('', Eof, ),))

        llist = LinkedList()
        llist.expnd(tseq)

        ptree = self.consume(tokens)
        yield from ptree

        if not (tokens.linked.empty() and self.no_errors):
            self.handle_error(tokens)

    def consume(self, llist):
        while True:
            index = llist.index
            ptree = self.symtree.consume(llist)
            if ptree:
                self.reduce(index, llist, ptree)
                yield ptree
            elif index.islast():
                break
            else:
                llist.get()

    def reduce(self, index, llist, ptree):
        self.delete(index, llindex)
        if ptree.type:
            self.insert(llindex, ptree)
        lindex.index = self.first()

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

class Rule:
    def __init__(self, *args, up=(), type=None):
        """
        """
        self.args = args
        self.type = type
        self.hmap = None
        self.up   = []

        self.up.extend(up)

    def startswith(self, llist):
        pass

    def precedence(self, llist):
        """
        """

        for ind in self.up:
            ptree = ind.startswith(llist)
            if ptree:
                return False
        return True
 
    def consume(self, data, llist):
        ptree = PTree(self.type)
        ptree.extend(data)
        return ptree

class T:
    def __init__(self, token, min=1, max=9999999999999):
        self.token = token
        self.min = min

        self.max = max

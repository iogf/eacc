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
            self.update(iter(ind.args), ind)

    def validate(self, llist, data):
        pass

    def consume(self, llist, data=[]):
        for ind in self.nodes:
            data = ind.validate(llist, data)
            if data:
                return data

    def append(self, pattern, rule):
        op = next(pattern, rule)

        for ind in self.nodes:
            if ind.istype(op):
                return ind.append(pattern)

        node = OpNode(op)
        node.append(pattern)
        self.nodes.append(node)
        return node

class OpNode(SymTree):
    def __init__(self, op):
        self.op = op
        self.kmap = []

    def validate(self, llist, data):
        token = self.op.validate(llist)
        if not token: 
            return None

        data.append(token)
        self.consume(llist, data)


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

        ptree = self.consume(llist)
        yield from ptree

        if not (llist.empty() and self.no_errors):
            self.handle_error(llist)

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
        self.delete(index, llist.index)
        if ptree.type:
            self.insert(llist.index, ptree)
        llist.index = self.first()

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

    def validate(self, llist):
        """
        """

        for ind in self.up:
            ptree = ind.startswith(llist)
            if ptree:
                return False
        return True
 
    def consume(self, llist, data):
        valid = self.validate(llist)
        if not valid: 
            return None

        ptree = PTree(self.type)
        ptree.extend(data)

        ## Warning.
        ptree.eval(self.hmap)
        return ptree

class T:
    def __init__(self, token, min=1, max=9999999999999):
        self.token = token
        self.min = min

        self.max = max

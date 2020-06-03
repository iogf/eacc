from eacc.token import PTree, Sof, Eof, Token, TokType, Operator
from eacc.llist import LinkedList
from itertools import chain

class EaccError(Exception):
    pass

class Grammar:
    pass

class Operator(TokType):
    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return True

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

    def is_equal(self, other):
        pass

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
            if not isinstance(ind, Operator):
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
        self.llist = LinkedList()
        self.hpos  = None
        self.index = None

        self.handles = {}

    def reset(self):
        self.index = self.llist.first()
        self.hpos = self.index

    def seek(self):
        self.index = self.llist.next(self.index)

    def shift(self):
        self.hpos = self.llist.next(self.hpos)
        self.index = self.hpos

    def lseek(self):
        self.index = self.llist.back(self.index)

    def tell(self):
        if self.index != self.llist.last:
            return self.index.elem

    def build(self, tseq):
        """
        """

        tseq = chain((Token('', Sof), ), 
        tseq, (Token('', Eof), ))

        self.llist.expand(tseq)
        self.reset()

        ptree = self.process()
        yield from ptree

        if not self.llist.empty() and not self.no_errors:
            self.handle_error(self.llist)
        self.hpos = self.index = None

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
        """
        """

        for ind in rules:
            self.symtree.update(ind)

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

    def startswith(self, eacc, data):
        for ind in self.args:
            token = ind.opexec(eacc, data)
            if not token:
                return False
        return True

    def precedence(self, eacc, data):
        for ind in self.up:
            index = eacc.index
            prec = ind.startswith(eacc, data)
            if prec:
                return False
            eacc.index = index
        return True
 
    def opexec(self, eacc, data):
        valid = self.precedence(eacc, data)
        if not valid: 
            return None

        ptree = PTree(self.type)
        ptree.extend(data)
        hmap = eacc.handles.get(self, None)
        if hmap:
            ptree.result = hmap(*ptree)
        return ptree

class Times(Operator):
    def __init__(self, token, min=1, max=None):
        self.token = token
        self.min = min

        self.max = max

    def opexec(self, eacc, data):
        ptree = PTree(None)

        while True:
            result = self.token.opexec(eacc, data)
            if not result:
                if self.max:
                    if self.min <= len(ptree) <= self.max:
                        return ptree
                if self.min <= len(ptree):
                    return ptree
            ptree.append(result)

    def __eq__(self, other):
        pass

class Except(Operator):
    def __init__(self, *args):
        self.args = args

    def opexec(self, eacc, data):
        token = eacc.tell()
        if not token: 
            return None

        if token.type in self.args: 
            return None

        eacc.seek()
        return token

    def __eq__(self, other):
        pass

class Only(Operator):
    def __init__(self, *args):
        self.args = args

    def opexec(self, eacc, data):
        pass

    def __eq__(self, other):
        pass

class TokVal(Operator):
    def __init__(self, data):
        self.data = data

    def opexec(self, eacc, data):
        token  = eacc.tell()
        if not token:
            return None

        if token.data != self.data:
            return None

        eacc.seek()
        return token

    def istype(self, tok):
        return self.type == tok.data

    def __repr__(self):
        return 'TokVal(%s)' % repr(self.data)
        
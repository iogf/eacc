from eacc.token import PTree, Sof, Eof, Token, TokType
from eacc.llist import LinkedList
from itertools import chain

class EaccError(Exception):
    pass

class Grammar:
    pass

class TokOp(TokType):
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

        index = eacc.index
        eacc.seek()
        ptree = node.match(eacc, data + [token])

        if not ptree:    
            eacc.index = index
        return ptree

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

    def consume(self, eacc, data=[]):
        token = eacc.tell()
        if not token:
            return None

        node = self.kmap.get(token.type)
        if not node:
            return self.runops(eacc, data)

        eacc.seek()
        ptree = node.match(eacc, data + [token])

        ntree = ptree
        while ptree and ptree.type == token.type:
            ntree = node.match(eacc, [ntree])
            if ntree:
                ptree = ntree
            else:
                break
        return ptree

    def update(self, rule):
        node = self
        for ind in rule.args:
            if not isinstance(ind, TokOp):
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
        self.llist = None
        self.hpos  = None
        self.index = None

        self.handles = {}
        self.stack = []

    def reset(self):
        self.index = self.llist.first()
        self.hpos = self.index

    def seek(self):
        self.index = self.llist.next(self.index)

    def shift(self):
        self.hpos = self.llist.next(self.hpos)
        self.index = self.hpos

    def tell(self):
        if self.index is not self.llist.last:
            return self.index.elem

    def push_state(self, tseq):
        self.stack.append((self.llist, self.hpos, self.index))

        self.llist = LinkedList()
        tseq = chain((Token('', Sof), ), 
        tseq, (Token('', Eof), ))

        self.llist.expand(tseq)
        self.index = self.llist.first()
        self.hpos  = self.index


    def pop_state(self):
        if not self.llist.empty():
            if not self.no_errors:
                self.handle_error(self.llist)    

        state = self.stack.pop()
        self.llist = state[0]
        self.hpos  = state[1]
        self.index = state[2]

    def chain(self, tseq):
        for ind in tseq:
            self.llist.insert(self.hpos, ind)

    def build(self, tseq, push=False):
        """
        """

        if self.llist and not push:
            self.chain(tseq)
        else:
            self.push_state(tseq)
        return self.process()

    def process(self):
        while self.index is not None:
            ptree = self.symtree.consume(self)
            if ptree is not None:
                self.reduce(ptree)
                yield ptree
            elif self.hpos.islast():
                self.pop_state()
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
        self.up   = up
        self.symtree = SymTree(self.up)

    def opexec(self, eacc, data):
        index = eacc.index
        ntree = self.symtree.match(eacc)
        eacc.index = index
        if ntree: 
            return None

        ptree = PTree(self.type)
        ptree.extend(data)
        hmap = eacc.handles.get(self, None)
        if hmap:
            ptree.result = hmap(*ptree)
        return ptree

class Times(TokOp):
    def __init__(self, token, min=1, max=None, type=None):
        self.token = token
        self.min = min
        self.max = max
        self.type = type

    def opexec(self, eacc, data):
        ptree = PTree(self.type)

        while True:
            result = self.token.opexec(eacc, data)
            if not result:
                if self.max:
                    if self.min <= len(ptree) <= self.max:
                        return ptree
                if self.min <= len(ptree):
                    return ptree
            ptree.append(result)

class Except(TokOp):
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

class DotTok(TokOp):
    def opexec(self, eacc, data):
        token = eacc.tell()
        if token:
            eacc.seek()
        return token

class Only(TokOp):
    def __init__(self, *args):
        self.args = args

    def opexec(self, eacc, data):
        token = eacc.tell()
        if not token: 
            return None

        if not (token.type in self.args): 
            return None

        eacc.seek()
        return token

class TokVal(TokOp):
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

        
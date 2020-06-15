from eacc.token import PTree, Sof, Eof, Token, TokType, TokOp, TokVal
from eacc.llist import LinkedList
from itertools import chain
from types import FunctionType

class EaccError(Exception):
    pass

class Grammar:
    pass

class SymNode:
    def __init__(self):
        self.kmap = {}
        self.ops  = []
        self.refs = None

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

        if ptree:    
            return ptree

        eacc.index = index
        if self.refs:
            ntree = self.refs.reduce(eacc)
            if ntree:
                ptree = node.match(eacc, data + [ntree])
                if ptree:    
                    return ptree
        eacc.index = index

    def make_refs(self, rule):
        if not self.refs:
            self.refs = SymTree()

        if rule.type in self.kmap:
            self.refs.update(rule)
        
        for ind in self.kmap.values():
            ind.make_refs(rule)

        for ind in self.ops:
            if isinstance(ind, OpNode):
                ind.make_refs(rule)

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
    def __init__(self):
        super(SymTree, self).__init__()
        self.rules = []

    def build(self, rules):
        for ind in rules:
            self.update(ind)

        for ind in rules:
            self.make_refs(ind)

        # for indi in rules:
            # for indj in self.kmap.values():
                # indj.make_refs(indi)
            # for indz in self.ops:
                # indz.make_refs(indi)

    def reduce(self, eacc, data=[]):
        index = eacc.index
        ptree = self.match(eacc)
        if ptree:
            eacc.llist.sub(index, eacc.index, ptree)

        # ptree = None
        # while True:
            # ptree = self.match(eacc)
            # if ptree:
                # eacc.llist.sub(index, eacc.index, ptree)
                # index = eacc.index.back
            # else:
# 
                # break

        # eacc.index= index
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
        self.symtree = SymTree()
        self.llist = None
        self.hpos  = None
        self.index = None

        self.handles = {}
        self.stack = []
        self.symtree.build(self.root)

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
            ptree = self.symtree.match(self)
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

        self.symtree.build(rules)

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
        self.symtree = SymTree()
        self.symtree.build(self.up)

    def opexec(self, eacc, data):
        index = eacc.index
        ntree = self.symtree.match(eacc)
        eacc.index = index
        if ntree: 
            return None

        type = self.type
        if isinstance(type, FunctionType):
            type = self.type(*data)

        ptree = PTree(type)
        ptree.extend(data)
        hmap = eacc.handles.get(self, None)
        if hmap:
            ptree.result = hmap(*ptree)
        return ptree

class Times(TokOp):
    def __init__(self, token, min=1, max=999999999, type=None):
        self.token = token
        self.min = min
        self.max = max
        self.type = type

    def opexec(self, eacc, data):
        ptree = PTree(self.type)
        opexec = self.token.opexec

        while True:
            result = opexec(eacc, data)
            if result:
                ptree.append(result)
            else:
                break

        if self.min <= len(ptree) <= self.max:
            return ptree
        return None

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

T = Times
E = Except
O = Only

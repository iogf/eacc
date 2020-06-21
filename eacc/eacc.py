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
        self.rules = []

    def runops(self, eacc, data=[]):
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

    def update(self, rule):
        node = self
        for ind in rule.args:
            if not isinstance(ind, TokOp):
                node = node.kmap.setdefault(ind, SymNode())
            else:
                node = node.append(ind)
        node.ops.append(ExecNode(rule))
        self.rules.append(rule)

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

class ExecNode(SymNode):
    def __init__(self, rule):
        super(ExecNode, self).__init__()
        self.rule = rule

        for ind in self.rule.up:
            self.update(ind)

    def copy(self):
        execnode = ExecNode(self.rule)
        return execnode

    def opexec(self, eacc, data):
        # if not self.rules:
            # ntree = self.match(eacc)
            # if ntree is None: 
                # return self.mktree(eacc, data)
# 
        # ptree = self.mktree(eacc, data)
        # node = self.kmap.get(ptree.type)
        # if node:
            # ntree = node.match(eacc, [ptree])
            # if ntree:
                # print('Return:', ntree)
                # return ntree
# 
        # return ptree
        ntree = self.match(eacc)
        if ntree is None:
            return self.rule.opexec(eacc, data)

class Rule(TokOp):
    def __init__(self, *args, up=(), type=None):
        """
        """
        self.args = args
        self.type = type
        self.up   = up

    def opexec(self, eacc, data):
        type = self.type
        if isinstance(type, FunctionType):
            type = self.type(*data)
    
        ptree = PTree(type)
        ptree.extend(data)
        hmap = eacc.handles.get(self, None)
        if hmap:
            ptree.result = hmap(*ptree)

        return ptree

class SymTree(SymNode):
    def __init__(self):
        super(SymTree, self).__init__()

    def build(self, rules):
        for ind in rules:
            self.update(ind)

        # for indi in rules:
            # for indj in rules:
                # if indi.args[0] == indj.type:
                    # if indi.up and not indj.up:
                        # self.mkrefs(indi, indj)

    def mkrefs(self, nrule, mrule):
        mrule.update(nrule.copy())

        # mrule.update(nrule)

    def reduce(self, eacc, data=[]):
        token = eacc.tell()
        ptree = self.match(eacc, data)
        if ptree:
            return self.swap(eacc, token.type, ptree)

    def swap(self, eacc, toktype, ptree):
        node  = self.kmap.get(toktype)
        match = node.match
        ntree = ptree

        while ntree and ntree.type == toktype:
            ntree = match(eacc, [ptree])
            if ntree:
                ptree = ntree
        return ptree

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

    def next_gap(self, index):
        while not index.isfirst():
            if index.elem.type in self.symtree.kmap:
                return index
            index = index.back
        return index

    def process(self):
        reduce = self.symtree.match
        while self.index is not None:
            ptree = reduce(self)
            if ptree is not None:
                self.replace(ptree)
                yield ptree
            elif self.hpos.islast():
                self.pop_state()
            else:
                self.shift()

    def replace(self, ptree):
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

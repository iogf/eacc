from eacc.lexer import Token, TokType, TokOp, Sof, Eof
from eacc.llist import LinkedList
from itertools import chain
from types import FunctionType

class EaccError(Exception):
    pass

class Grammar:
    pass

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

    def __repr__(self):
        return 'TokVal(%s)' % repr(self.data)

class PTree(list):
    """
    """
    __slots__ = ['type', 'result', 'data']

    def __init__(self, type):
        super(PTree, self).__init__()
        self.type = type
        self.data = type
        self.result = None

    def val(self):
        return self.result

    def __repr__(self):
        return '%s(%s=%s)' % (self.type.__name__ if self.type else None, 
        super(PTree, self).__repr__(), self.val())

class SymNode:
    def __init__(self, eacc):
        self.kmap = {}
        self.ops  = []
        self.rules = []
        self.eacc = eacc

    def runops(self, data=[]):
        for ind in self.ops:
            node  = ind.opexec(data)
            if node:
                return node

    def match(self, data=[]):
        token = self.eacc.tell()

        if not token:
            return self.runops(data)

        node = self.kmap.get(token.type)
        if not node:
            return self.runops(data)

        index = self.eacc.index
        self.eacc.seek()
        ptree = node.match(data + [token])

        if ptree:
            return ptree
        self.eacc.index = index

        ptree = self.runops(data)
        if ptree:
            return ptree

        self.eacc.index = index

    def bind_op(self, op):
        for ind in self.ops:
            if ind.op == op:
                return ind

        node = OpNode(self.eacc, op)
        self.ops.append(node)
        return node

    def expand(self, toktypes):
        node = self
        for ind in toktypes:
            if not isinstance(ind, TokOp):
                node = node.kmap.setdefault(ind, SymNode(self.eacc))
            else:
                node = node.bind_op(ind)
        return node

    def __repr__(self):
        return self.kmap.__repr__()

class OpNode(SymNode):
    def __init__(self, eacc, op):
        super(OpNode, self).__init__(eacc)
        self.op = op

    def opexec(self, data):
        index = self.eacc.index
        token = self.op.opexec(self.eacc, data)
        if token:
            node = self.match(data + [token])
            if node:
                return node
        self.eacc.index = index

class ExecNode(SymNode):
    def __init__(self, eacc, rule):
        super(ExecNode, self).__init__(eacc)
        self.op = rule

        for ind in self.op.up:
            ind.register(self)

    def opexec(self, data):
        ptree = self.op.opexec(self.eacc, data)
        ntree = self.match(data)
        if ntree:
            return None
        return ptree

class Struct(SymNode):
    def __init__(self, eacc, *args):
        super(Struct, self).__init__(eacc)
        self.args = args

    def register(self, ynode):
        pass

class Rule(TokOp):
    def __init__(self, *args, up=(), type=None):
        """
        """
        self.args = args
        self.type = type
        self.up   = up

    def register(self, ynode):
        node = ynode.expand(self.args)
        execnode = ExecNode(ynode.eacc, self)

        node.ops.append(execnode)
        node.rules.append(self)

        return execnode

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
    def __init__(self, eacc):
        super(SymTree, self).__init__(eacc)

    def build(self):
        for ind in self.eacc.root:
            ind.register(self)

    # def reduce(self, eacc, data=[]):
        # token = eacc.tell()
        # ptree = self.match(eacc, data)
        # if ptree:
            # return self.swap(eacc, token.type, ptree)
# 
    # def swap(self, eacc, toktype, ptree):
        # node  = self.kmap.get(toktype)
        # match = node.match
        # ntree = ptree
# 
        # while ntree and ntree.type == toktype:
            # ntree = match(eacc, [ptree])
            # if ntree:
                # ptree = ntree
        # return ptree

class Eacc:
    def __init__(self, grammar, no_errors=False):
        self.root = grammar.root
        self.no_errors = no_errors        
        self.symtree = SymTree(self)
        self.llist = None
        self.hpos  = None
        self.index = None

        self.handles = {}
        self.stack = []
        self.symtree.build()

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
        state = self.stack.pop()
        llist = self.llist
        
        # First set the previous state otherwise
        # it gets messed if Eacc.build is called again.
        self.llist = state[0]
        self.hpos  = state[1]
        self.index = state[2]

        if not llist.empty():
            if not self.no_errors:
                self.handle_error(llist)

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
        """
        Process the token sequence from Eacc.Build.
        """

        while self.index is not None:
            pattern = self.symtree.match()
            if pattern is not None:
                self.replace_node(pattern)
                yield pattern
            elif self.hpos.islast():
                self.pop_state()
            else:
                self.shift()

    def replace_node(self, pattern):
        if pattern.type:
            self.llist.sub(self.hpos, self.index, pattern)
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

    def __eq__(self, other):
        if self.token != other.token:
            return False
        elif self.min != other.min:
            return False
        elif self.max != other.max:
            return False
        elif self.type != other.type:
            return False
        return True

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

    def __eq__(self, other):
        if not isinstance(other, Except):
            return False
        elif self.args == other.args:
            return True
        return False

class DotTok(TokOp):
    def opexec(self, eacc, data):
        token = eacc.tell()
        if token:
            eacc.seek()
        return token

    def __eq__(self, other):
        return isinstance(other, DotTok)

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

    def __eq__(self, other):
        if not isinstance(other, Only):
            return False
        elif self.args == other.args:
            return True
        return False

T = Times
E = Except
O = Only

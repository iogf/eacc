from eacc.token import PTree, Sof, Eof, Token
from eacc.llist import LinkedList
from itertools import chain

class EaccError(Exception):
    pass

class Grammar:
    pass

class SymTree:
    def __init__(self, rules):
        pass

    pass

class SymNode:
    def __init__(self, sym):
        self.sym = sym
        self.op  = op
        self.kmap = {}

    def consume(self, sym):
        pass

class Eacc:
    def __init__(self, grammar, no_errors=False):
        self.root = grammar.root
        self.no_errors = no_errors

    def build(self, tseq):
        """
        """

        tseq = chain((Token('', Sof), ), 
        tseq, (Token('', Eof, ),))

        llist = LinkedList()

        ptree = self.process(tokens)

        if not (tokens.linked.empty() and self.no_errors):
            self.handle_error(tokens)

    def extend(self, *rules):
        pass

    def process(self, tokens):
        pass

    def consume(self, tokens):
        """
        """
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

class T:
    def __init__(self, token, min=1, max=9999999999999):
        self.token = token
        self.min = min

        self.max = max

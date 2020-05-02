from eacc.token import *
import re

class LexError(Exception):
    pass

class XSpec:
    pass

class Lexer:
    def __init__(self, xspec):
        """
        """
        self.root = xspec.root

    def feed(self, data):
        """
        """
        tseq = self.process(data)
        lmb  = lambda ind: not ind.discard
        tseq = filter(lmb, tseq)
        
        yield from tseq

    def process(self, data):
        pos = 0
        while True:
            tseq = self.consume(data, pos)
            if tseq:
                yield from tseq
                pos = tseq[-1].end
            elif pos != len(data):
                self.handle_error(data, pos)
            else:
                break

    def consume(self, data, pos):
        """
        """
        for ind in self.root:
            tseq = ind.consume(data, pos)
            if tseq:
                return tseq

    def handle_error(self, data, pos):
        msg = 'Unexpected token: %s' % repr(data[pos:pos+30])
        raise LexError(msg)

class LexMap(XNode):
    def __init__(self):
        """
        """
        self.children = []
        self.regstr   = ''
        self.regex    = None
        self.regdict  = {}
        self.regindex = {}

        super(LexMap, self).__init__()

    def build_regex(self):
        regdict = ((ind.mkgname(), ind) 
        for ind in self.children)

        self.regdict = dict(regdict)
        regstr = (ind.mkindex() for ind in self.children)

        self.regstr = '|'.join(regstr)
        self.regex  = re.compile(self.regstr, 0)

        groups   = self.regex.groupindex.items()
        regindex = ((ind[1], self.regdict[ind[0]]) 
        for ind in groups)

        self.regindex = dict(regindex)

    def add(self, *args):
        self.children.extend(args)
        self.build_regex()

    def consume(self, data, pos):
        """
        """
        regobj = self.regex.match(data, pos)
        if regobj:
            token = self.regindex[regobj.lastindex].mktoken(data, regobj)
            if token:
                return token

    def __repr__(self):
        return 'LexMap(%s)' % self.children

class R(XNode):
    def __init__(self, lex, min=1, max=9999999999999):
        """
        R stands for Repeat. It makes sure a given lexical
        condition happens n times where min < n < max or min < n.
        """

        self.lex = lex
        self.min = min
        self.max = max

    def consume(self, data, pos, exclude=()):
        pass

class LexNode(XNode):
    def __init__(self, regstr, type=TokVal, cast=None, discard=False):
        """
        """
        super(XNode, self).__init__()
        self.regstr = regstr
        self.type   = type

        # self.cast   = cast
        self.discard = discard

        self.cast = (lambda data, type, value, 
        start, end, discard: Token(data, type, cast(value), 
        start, end, discard)) if cast else Token

    def mkgname(self):
        gname = 'LN%s' % id(self)
        return gname

    def mkindex(self):
        gname = self.mkgname()
        return '(?P<%s>%s)' % (gname, self.regstr)

    def mktoken(self, data, regobj):
        return (self.cast(regobj.group(), self.type, 
                regobj.group(), regobj.start(), regobj.end(), self.discard), )

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqNode(LexNode):
    def __init__(self, regstr, type=TokVal, cast=None, discard=False):
        super(SeqNode, self).__init__(regstr, type, cast, discard)
        self.regex  = re.compile(regstr)

    def mkindex(self):
        return self.regstr

    def consume(self, data, pos):
        regobj = self.regex.match(data, pos)
        if regobj:
            return self.mktoken(data, regobj)

class LexSeq(XNode):
    def __init__(self, arg0, *args):
        self.arg0 = arg0
        self.args = args

    def mkgname(self):
        gname = 'LS%s' % id(self)
        return gname

    def mkindex(self):
        gname = self.mkgname()
        return '(?P<%s>%s)' % (gname, self.arg0.mkindex())

    def mktoken(self, data, regobj):
        tseq = TSeq()
        token = self.arg0.mktoken(data, regobj)
        tseq.extend(token)

        for ind in self.args:
            token = ind.consume(data, tseq[-1].end)
            if token:
                tseq.extend(token)
            else:
                return None
        return tseq

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes


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
        super(LexMap, self).__init__()

    def add(self, *args):
        self.children.extend(args)

    def is_rulemap(self):
        return True

    def consume(self, data, pos, exclude=()):
        """
        """
        for ind in self.children:
            if not ind in exclude:
                tseq = ind.consume(data, pos, exclude)
                if tseq:
                    return tseq

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

    def is_rulemap(self):
        return self.lex.is_rulemap()

    def consume(self, data, pos, exclude=()):
        tseq  = TSeq()
        count = 0
        while True:
            token = self.lex.consume(data, pos, exclude)
            if token:
                tseq.extend(token)
            elif self.min <= count < self.max:
                break
            else:
                return None
            pos = token[-1].end
            count += 1
        return tseq

class LexNode(XNode):
    def __init__(self, regstr, type=TokVal, cast=None, discard=False):
        """
        """
        super(XNode, self).__init__()
        self.regex  = re.compile(regstr)
        self.regstr = regstr
        self.type   = type
        self.cast   = cast
        self.match  = self.regex.match
        self.discard = discard

    def is_rulemap(self):
        return False

    def consume(self, data, pos, exclude=()):
        regobj = self.match(data, pos)
        if regobj:
            return TSeq((Token(regobj.group(), self.type, 
                self.cast, regobj.start(), regobj.end(), self.discard), ))
    
    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqNode(LexNode):
    def __init__(self, regstr, type=TokVal, cast=None, discard=False):
        super(SeqNode, self).__init__(regstr, type, cast, discard)

    def is_rulemap(self):
        return False

class LexSeq(XNode):
    def __init__(self, *args):
        self.args = args

    def fix_exclusion(self, exclude, index):
        if not index or self.args[index - 1].is_rulemap():
            return exclude + (self, )
        else:
            return ()

    def is_rulemap(self):
        return False
    
    def consume(self, data, pos, exclude=()):
        tseq  = TSeq()
        for ind in range(0, len(self.args)):
            token = self.args[ind].consume(data, 
            pos, self.fix_exclusion(exclude, ind))
            if token != None:
                tseq.extend(token)
            else:
                return None
            if tseq:
                pos = tseq[-1].end
        return tseq

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes


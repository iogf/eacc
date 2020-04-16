from eacc.token import XNode, TSeq, TokVal
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
        tseq = self.consume(data)
        lmb  = lambda ind: not ind.discard
        tseq = filter(lmb, tseq)

        yield from tseq

    def consume(self, data):
        """
        """
        pass

    def handle_error(self, tseq):
    
        raise LexError(msg)
        pass

class LexMap(XNode):
    def __init__(self):
        """
        """
        self.children = []
        super(LexMap, self).__init__()

    def add(self, *args):
        self.children.extend(args)

    def is_map(self):
        return True

    def search(self, data, tseq):
        tseq = TSeq()
        pass

    def match(self, data, pos, exclude=()):
        for ind in self.children:
            if not ind in exclude:
                tseq = ind.match(data, pos, exclude)
                if tseq:
                    return tseq

    def __repr__(self):
        return 'LexMap(%s)' % self.children


class LexNode(XNode):
    def __init__(self, regstr, type=TokVal, cast=None, discard=False):
        """
        """
        super(XNode, self).__init__()
        self.regex  = re.compile(regstr)
        self.regstr = regstr
        self.type   = type
        self.cast   = cast
        self.discard = discard

    def search(self, data, tseq):
        xseq = TSeq()

    def consume(self, data, start, end):
        pass

    def match(self, data, pos, exclude=()):
        # regobj = self.match(data, pos)
        # if regobj:
            # return TSeq((Token(regobj.group(), self.type, 
                # self.cast, regobj.start(), regobj.end(), self.discard), ))
        pass

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqNode(LexNode):
    def __init__(self, regstr, type=TokVal, cast=None, discard=False):
        super(SeqNode, self).__init__(regstr, type, cast, discard)

    def search(self, data, start, end):
        pass

    def match(self, data, pos, exclude=()):
        pass

class R(XNode):
    def __init__(self, lex, min=1, max=9999999999999):
        """
        R stands for Repeat. It makes sure a given lexical
        pattern happens n times where min < n < max or min < n.
        """

        self.lex = lex
        self.min = min
        self.max = max

    def is_map(self):
        return self.lex.is_map()

    def search(self, data, start, end):
        pass

    def match(self, data, pos, exclude=()):
        tseq  = TSeq()
        count = 0
        pass

class LexSeq(XNode):
    def __init__(self, *args):
        self.args = args

    def fix_exclusion(self, exclude, index):
        if not index or self.args[index - 1].is_map():
            return exclude + (self, )
        else:
            return ()

    def search(self, data, tseq):
        pass

    def consume(self, data, start, end):
        tseq = TSeq()
        pass

    def match(self, pos, exclude=()):
        tseq = TSeq()
        pass

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes


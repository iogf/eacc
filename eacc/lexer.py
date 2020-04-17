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

    def consume(self, data, tseq):
        tseq = TSeq()
        pass

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

    def consume(self, data, tseq):
        xseq = TSeq()

    def loop(self, data, start, end):
        pass

    def find(self, data, start, end):
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

    def find(self, data, start, end):
        pass

    def match(self, data, pos):
        pass

class LexSeq(XNode):
    def __init__(self, *args):
        self.args = args

    def consume(self, data, tseq):
        pass

    def loop(self, data, start, end):
        tseq = TSeq()
        pass

    def find(self, data, start, end):
        tseq = TSeq()
        pass

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes


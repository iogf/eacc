from eacc.token import Token, XNode, TSeq, TokVal
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
        tseq = []
        for ind in self.root:
            tseq = ind.consume(data, tseq)
        return tseq

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
        for ind in self.children:
            tseq = ind.consume(data, tseq)        
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
        self.finditer = self.regex.finditer

    def consume(self, data, tseq):
        xseq = TSeq()
        pos  = 0

        for ind in tseq:
            if pos < ind.start:
                xseq.extend(self.find(data, pos, ind.start))
            xseq.append(ind)
            pos = ind.end

        nseq = self.find(data, pos, len(data))
        xseq.extend(nseq)
        return xseq

    def find(self, data, start, end):
        regobjs = self.finditer(data, start, end)
        tokens  = (Token(ind.group(), self.type, self.cast, ind.start(), 
            ind.end(), self.discard) for ind in regobjs)

        return tokens

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqNode(LexNode):
    def __init__(self, regstr, type=TokVal, cast=None, discard=False):
        super(SeqNode, self).__init__(regstr, type, cast, discard)

    def match(self, data, start, end):
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


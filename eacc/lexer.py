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
        self.search = self.regex.search

    def consume(self, data, tseq):
        xseq = TSeq()
        if not tseq:
            xseq.extend(self.loop(data, 0, len(data)))
        else:
            xseq.extend(self.step(data, tseq))
        return xseq

    def step(self, data, tseq):
        xseq = TSeq()
        key  = lambda ind: (ind.start, ind.end)
        pos  = 0

        for ind in tseq:
            nseq = self.loop(data, pos, ind.start)
            xseq.extend(nseq)
            pos = ind.end

        end  = len(data) if tseq else xseq[-1]
        nseq = self.loop(data, pos, end)
        xseq.extend(nseq)

        xseq.extend(tseq)
        return sorted(xseq, key=key)

    def loop(self, data, start, end):
        pos = start
        while True:
            tokens = self.find(data, pos, end)
            if tokens != None:
                pos = tokens[-1].end
                yield from tokens
            else:
                break 
        pass

    def find(self, data, start, end):
        regobj = self.search(data, start, end)
        if regobj:
            return (Token(regobj.group(), self.type, 
                self.cast, regobj.start(), 
                    regobj.end(), self.discard), )

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


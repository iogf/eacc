import re

class LexError(Exception):
    pass

class XNode:
    pass

class XSpec:
    pass

class TSeq(list):
    pass

class Token:
    __slots__=['data', 'offset', 'type', 'value', 
    'start', 'end']

    def __init__(self, data, type=None, value=None, 
        start=None, end=None):

        self.data = data
        self.value = value
        self.type = type
        self.start = start
        self.end = end

    def val(self):
        return self.value
    
    def __repr__(self):
        return '%s(%s)' % (self.type.__name__, repr(self.data))


class TokType:
    @classmethod
    def opexec(cls, eacc, data):
        token  = eacc.tell()
        if not (token and token.type is cls):
            return None

        eacc.seek()
        return token

class Eof(TokType):
    pass

class Sof(TokType):
    pass

class TokOp(TokType):
    pass

class Lexer:
    def __init__(self, xspec, no_errors=False):
        """
        """
        self.root = xspec.root
        self.regstr   = ''
        self.regex    = None
        self.regdict  = {}
        self.build_regex()
        self.no_errors = no_errors

    def handle_error(self, data, pos):
        msg = 'Unexpected token: %s' % repr(data[pos:pos+30])
        raise LexError(msg)

    def feed(self, data):
        """
        """
        pos = 0
        regdict = self.regdict
        regobj  = self.regex.finditer(data)

        for ind in regobj:
            if pos != ind.start():
                if not self.no_errors:
                    raise self.handle_error(data, pos)
            pos = ind.end()
            mktoken = regdict.get(ind.lastgroup)
            if mktoken:
                yield from mktoken(ind)

        if not self.no_errors and pos != len(data):
            raise self.handle_error(data, pos)

    def build_regex(self):
        regdict = ((ind.gname, ind.mktoken)
        for ind in self.root)

        self.regdict = dict(regdict)
        regstr = (ind.mkindex() for ind in self.root)

        self.regstr = '|'.join(regstr)
        self.regex  = re.compile(self.regstr, 0)

    def __repr__(self):
        return 'LexMap(%s)' % self.children


class LexTok(XNode):
    def __init__(self, regstr, type=None, 
        cast=None, discard=False, wrapper=None):

        """
        """
        super(XNode, self).__init__()
        self.regstr  = regstr
        self.type    = type
        self.discard = discard
        self.gname   = self.mkgname()

        self.cast = (lambda data, type, value, 
        start, end: Token(data, type, cast(value), 
        start, end)) if cast else Token

        if wrapper:
            self.mktoken = lambda regobj: wrapper(self, regobj)

    def mkgname(self):
        gname = 'LN%s' % id(self)
        return gname

    def mkindex(self):
        gname = self.mkgname()
        if self.discard:
            return self.regstr
        else:
            return '(?P<%s>%s)' % (gname, self.regstr)

    def mktoken(self, regobj):
        mstr = regobj.group()

        return (self.cast(mstr, self.type, 
            mstr, regobj.start(), regobj.end()), )

    def __repr__(self):
        return 'SeqTok(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqTok(LexTok):
    def __init__(self, regstr, type=None, cast=None, discard=False):
        super(SeqTok, self).__init__(regstr, type, cast, discard)

    def mkgname(self):
        gname = 'SN%s' % id(self)
        return gname

    def mktoken(self, regobj):
        mstr = regobj.group(self.gname)
        start, end = regobj.span(self.gname)

        return (self.cast(mstr, self.type, 
            mstr, start, end), )

class LexSeq(XNode):
    def __init__(self, *args, wrapper=None):
        self.args = args
        self.gname = self.mkgname()

        if wrapper:
            self.mktoken = lambda regobj: wrapper(self, regobj)

    def mkgname(self):
        gname = 'LS%s' % id(self)
        return gname

    def mkindex(self):
        gname  = self.mkgname()
        regex  = ''.join((ind.mkindex() for ind in self.args))
        isdisc = all(map(lambda ind: ind.discard, self.args))

        if isdisc:
            return regex
        else:
            return '(?P<%s>%s)' % (gname, regex)

    def mktoken(self, regobj):
        tseq = TSeq()
        for ind in self.args:
            if not ind.discard:
                tseq.extend(ind.mktoken(regobj))
        return tseq

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes


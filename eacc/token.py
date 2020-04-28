class XNode:
    def __init__(self):
        pass

    def is_rulemap(self):
        return False

class PTree(list):
    """
    """
    __slots__ = ['type', 'result', 'data']

    def __init__(self, type):
        super(PTree, self).__init__()
        self.type = type
        self.data = type
        self.result = None

    def eval(self, handle):
        if handle:
            self.result = handle(*self)

    def val(self):
        return self.result

class Token:
    __slots__=['data', 'offset', 'type', 'value', 
    'pos', 'start', 'end', 'discard']

    def __init__(self, data, type=None, cast=None, 
        start=None, end=None, discard=False):

        self.data = data
        self.value = cast(data) if cast else data
        self.type = type
        self.pos = (start, end)
        self.start = start
        self.end = end
        self.discard = discard

    def val(self):
        return self.value
    
    def __repr__(self):
        return '%s(%s)' % (self.type.__name__, repr(self.data))

class TSeq(list):
    """
    """

class TokType:
    @classmethod
    def validate(cls, slc):
        tok = slc.get()
        if tok and cls.istype(tok):
            return tok

    @classmethod
    def istype(cls, tok):
        return tok.type is cls

class TokVal:
    def __init__(self, data):
        self.data = data
        self.type = TokVal

    def validate(self, slc):
        tok = slc.get()
        if tok and self.istype(tok):
            return tok

    def istype(self, tok):
        return self.data == tok.data

    def __repr__(self):
        return 'TokVal(%s)' % repr(self.data)

class Eof(TokType):
    pass

class Sof(TokType):
    pass

class Num(TokType):
    pass

class Plus(TokType):
    pass

class Minus(TokType):
    pass

class Div(TokType):
    pass

class Mul(TokType):
    pass

class RP(TokType):
    pass

class LP(TokType):
    pass

class Blank(TokType):
    pass

class Keyword(TokType):
    pass

class Identifier(TokType):
    pass

class Colon(TokType):
    pass

class DoubleQuote(TokType):
    pass

class Quote(TokType):
    pass

class Comma(TokType):
    pass

class LB(TokType):
    """
    Left bracket.
    """
    pass

class RB(TokType):
    """
    Right bracket.
    """
    pass

class LBR(TokType):
    """
    Left brace.
    """
    pass

class RBR(TokType):
    """    
    Right brace.
    """
    pass

class Word(TokType):
    pass

class UnkToken(TokType):
    pass

class Greater(TokType):
    pass

class Lesser(TokType):
    pass

class Question(TokType):
    pass

class BackSlash(TokType):
    pass

class Period(TokType):
    pass

class Char(TokType):
    pass

class Comment(TokType):
    pass

class Text(TokType):
    pass

class Error(TokType):
    pass

class Operator(TokType):
    pass

class Literal(TokType):
    pass

class Punctuation(TokType):
    pass

class Punctuation(TokType):
    pass

class Constant(TokType):
    pass

class Declaration(TokType):
    pass

class Name(TokType):
    pass

class Attribute(TokType):
    pass

class Builtin(TokType):
    pass

class Class(TokType):
    pass

class Class(TokType):
    pass

class Function(TokType):
    pass

class Variable(TokType):
    pass

class Backtick(TokType):
    pass

class Doc(TokType):
    pass

class Escape(TokType):
    pass

class String(TokType):
    pass

class Regex(TokType):
    pass

class Symbol(TokType):
    pass

class Integer(TokType):
    pass

class Hex(TokType):
    pass

class Caret(TokType):
    pass

class Dot(TokType):
    pass

class Dollar(TokType):
    pass

class Stick(TokType):
    pass

class Semicolon(TokType):
    pass

class Equal(TokType):
    pass

class Hash(TokType):
    pass

class Exclam(TokType):
    pass

class Letter(TokType):
    pass

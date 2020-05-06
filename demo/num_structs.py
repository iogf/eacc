"""
"""

from eacc.eacc import Eacc,  Rule, Grammar
from eacc.lexer import XSpec, Lexer, LexTok, TokVal
from eacc.token import TokType, Eof, Sof, Num, Plus, Blank

class Type0(TokType):
    pass

class Type1(TokType):
    pass

class NumTokens(XSpec):
    t_num = LexTok(r'[1-9]+', type=Num)
    t_plus = LexTok(r'\+', type=Plus)

    t_blank = LexTok(r' +', type=Blank, discard=True)

    root = [t_num, t_plus, t_blank]

class NumGrammar(Grammar):
    r_type0 = Rule(TokVal('1'), TokVal('+'), TokVal('2'), type=Type0)
    r_type1 = Rule(Type0, TokVal('+'), TokVal('2'), type=Type1)
    r_end   = Rule(Sof, Type1, Eof)

    root = [r_type0, r_type1, r_end]

data = '1 + 2 + 2'
lexer = Lexer(NumTokens)
eacc  = Eacc(NumGrammar)
tokens = lexer.feed(data)
ptree  = eacc.build(tokens)
print('Consumed:', list(ptree))


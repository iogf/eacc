"""
"""

from eacc.eacc import Eacc,  Rule, Grammar, Struct
from eacc.lexer import XSpec, Lexer, LexTok, TokVal
from eacc.token import Eof, Sof, Num, Plus, Blank

class NumTokens(XSpec):
    t_num = LexTok(r'[1-9]+', type=Num)
    t_plus = LexTok(r'\+', type=Plus)

    t_blank = LexTok(r' +', type=Blank, discard=True)

    root = [t_num, t_plus, t_blank]

class NumGrammar(Grammar):
    type0   = Struct()
    type1   = Struct()

    r_type0 = Rule(TokVal('1'), TokVal('+'), TokVal('2'), type=type0)
    type0.add(r_type0)

    r_type1 = Rule(type0, TokVal('+'), TokVal('2'), type=type1)
    r_end   = Rule(Sof, type1, Eof)
    type1.add(r_type1, r_end)

    root = [type0, type1]

data = '1 + 2 + 2'
lexer = Lexer(NumTokens)
eacc  = Eacc(NumGrammar)
tokens = lexer.feed(data)
ptree  = eacc.build(tokens)
print('Consumed:', list(ptree))


"""
"""

from eacc.fmt import Lexer, LexMap, SeqTok, R, LexSeq, LexTok, XSpec
from eacc.token import Num, LP, RP, Blank

class TupleTokens(XSpec):
    lexmap  = LexMap()
    t_paren = LexSeq(SeqTok(r'\(', LP), 
    R(lexmap, 0), SeqTok(r'\)', RP))

    t_blank = LexTok(r' +', Blank)
    t_elem  = LexTok(r'[0-9]+', Num)

    lexmap.add(t_paren, t_elem, t_blank)
    root = [lexmap]

print('Example 1')
lex = Lexer(TupleTokens)
data = '(1 1 2 (1 2))'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
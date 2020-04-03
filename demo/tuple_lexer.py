"""
"""

from eacc.lexer import Lexer, LexMap, SeqNode, R, LexSeq, LexNode, XSpec
from eacc.token import Num, LP, RP, Blank

class TupleTokens(XSpec):
    lexmap  = LexMap()
    t_paren = LexSeq(SeqNode(r'\(', LP), 
    R(lexmap, 0), SeqNode(r'\)', RP))

    t_blank = LexNode(r' +', Blank)
    t_elem  = LexNode(r'[0-9]+', Num)

    lexmap.add(t_paren, t_elem, t_blank)
    root = [lexmap]

print('Example 1')
lex = Lexer(TupleTokens)
data = '(1 1 2 (1 2))'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
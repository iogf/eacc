"""
"""

from eacc.lexer import Lexer, LexSeq, SeqNode, R, LexMap, LexNode, XSpec
from eacc.token import Blank, Num, LP, RP, RB, LB

class TupleTokens(XSpec):
    lex_tuple  = LexMap()
    lex_list  = LexMap()

    t_paren = LexSeq(SeqNode(r'\(', LP), 
    R(lex_tuple, 0), SeqNode(r'\)', RP))

    t_bracket = LexSeq(SeqNode(r'\[', LB), 
    R(lex_list, 0), SeqNode(r'\]', RB))

    t_blank = LexNode(r' +', Blank)
    t_elem  = LexNode(r'[0-9]+', Num)

    lex_tuple.add(t_paren, t_bracket, t_elem, t_blank)

    lex_list.add(t_bracket, t_elem, t_blank)

    root = [lex_tuple]

print('Example 1')
lexer  = Lexer(TupleTokens)
data = '((1 2) ([3 [1] 4] ([1 [1] 2]) 2))'
tokens = lexer.feed(data)
print('Consumed:', list(tokens))

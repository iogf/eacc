"""
"""

from eacc.fmt import Lexer, LexSeq, SeqTok, R, LexMap, LexTok, XSpec
from eacc.token import Blank, Num, LP, RP, RB, LB

class TupleTokens(XSpec):
    lex_tuple  = LexMap()
    lex_list  = LexMap()

    t_paren = LexSeq(SeqTok(r'\(', LP), 
    R(lex_tuple, 0), SeqTok(r'\)', RP))

    t_bracket = LexSeq(SeqTok(r'\[', LB), 
    R(lex_list, 0), SeqTok(r'\]', RB))

    t_blank = LexTok(r' +', Blank)
    t_elem  = LexTok(r'[0-9]+', Num)

    lex_tuple.add(t_paren, t_bracket, t_elem, t_blank)

    lex_list.add(t_bracket, t_elem, t_blank)

    root = [lex_tuple]

print('Example 1')
lexer  = Lexer(TupleTokens)
data = '((1 2) ([3 [1] 4] ([1 [1] 2]) 2))'
tokens = lexer.feed(data)
print('Consumed:', list(tokens))

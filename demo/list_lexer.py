"""
This example defines a lexer that tokenizes a list structure
and also checks for its format.

The definition allows lists like below to be valid:

    [1[1,2]]
    [1[1,2]3]
    [1,[1,2],3]
    [1,[1,2],3,]
    [1,[1,2],]

"""

from yacc.lexer import Lexer, LexMap, SeqNode, R, LexSeq, LexNode, XSpec
from yacc.token import Num, LB, RB, Blank, Comma

class TupleTokens(XSpec):
    lexmap  = LexMap()
    t_comma = LexNode(r'\,', Comma)
    t_num   = LexSeq(SeqNode(r'[0-9]+', Num), R(t_comma, 0))

    t_paren = LexSeq(SeqNode(r'\[', LB),
    R(lexmap), SeqNode(r'\]', RB), R(t_comma, 0))

    lexmap.add(t_num, t_paren)
    root = [lexmap]

print('Example 1')
lex = Lexer(TupleTokens)
data = '[1,[1,2,3,4,],1,3,[1,2[3,[1,2]2],],],'
tokens = lex.feed(data)
print('Consumed:', list(tokens))

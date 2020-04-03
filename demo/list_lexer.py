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

from eacc.lexer import Lexer, LexMap, SeqNode, R, LexSeq, LexNode, XSpec
from eacc.token import Num, LB, RB, Comma

class ListTokens(XSpec):
    lexmap  = LexMap()
    t_comma = LexNode(r'\,', Comma)
    t_num   = LexSeq(SeqNode(r'[0-9]+', Num), R(t_comma, 0, 2))

    t_paren = LexSeq(SeqNode(r'\[', LB),
    R(lexmap), SeqNode(r'\]', RB), R(t_comma, 0, 2))

    lexmap.add(t_num, t_paren)
    root = [lexmap]

print('Example 1')
lex = Lexer(ListTokens)
data = '[1,[1,2,3,4,],1,3,[1,2[3,[1,2]2],],],'
tokens = lex.feed(data)
print('Consumed:', list(tokens))

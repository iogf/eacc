"""
The example below shows how to tokenize and also validate
a sequence of arguments like:

    1,2,3,4, ...
"""

from eacc.lexer import Lexer, LexMap, SeqNode, R, LexSeq, XSpec
from eacc.token import Num, Comma

class ArgsTokens(XSpec):
    lexmap  = LexMap()
    t_comma = SeqNode(r'\,', Comma)
    t_num   = SeqNode(r'[0-9]+', Num)

    t_elem  = LexSeq(t_comma, t_num)
    t_args  = LexSeq(t_num, R(t_elem, 0))

    lexmap.add(t_args)
    root = [lexmap]

print('Example 1')
lex = Lexer(ArgsTokens)
data = '1,2,3,4,5'
tokens = lex.feed(data)
print('Consumed:', list(tokens))


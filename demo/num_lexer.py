"""
The example below  tokenizes numbers whose number of digits is 3 <= n < 6.

When the number of digits is not in that range then it raises an error.
Thus the string below would give a lexical error.

    12 31 445
"""

from eacc.lexer import Lexer, LexMap, SeqNode, R, LexSeq, LexNode, XSpec
from eacc.token import Num, Blank

class NumsTokens(XSpec):
    lexmap  = LexMap()
    t_blank = LexNode(r' +', Blank)
    t_num   = SeqNode(r'[0-9]', Num)

    t_elem  = LexSeq(R(t_num, 3, 6))

    lexmap.add(t_elem, t_blank)
    root = [lexmap]

print('Example 1')
lex = Lexer(NumsTokens)
data = '332 3445 11234'
tokens = lex.feed(data)
print('Consumed:', list(tokens))



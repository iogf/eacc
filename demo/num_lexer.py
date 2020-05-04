"""
The example below  tokenizes numbers whose number of digits is 3 <= n < 6.

When the number of digits is not in that range then it raises an error.
Thus the string below would give a lexical error.

    12 31 445
"""

from eacc.lexer import Lexer, SeqTok, LexSeq, LexTok, XSpec
from eacc.token import Num, Blank

class NumsTokens(XSpec):
    t_blank = LexTok(r' +', Blank)
    t_num   = LexTok(r'[0-9]{3,6}', Num)

    root = [t_num, t_blank]

print('Example 1')
lex = Lexer(NumsTokens)
data = '332 3445 11234'
tokens = lex.feed(data)
print('Consumed:', list(tokens))



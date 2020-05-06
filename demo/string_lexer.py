"""
"""

from eacc.lexer import Lexer, LexSeq, LexTok, SeqTok, XSpec
from eacc.token import DoubleQuote, String, Blank

class StringTokens(XSpec):
    t_dquote = LexSeq(SeqTok(r'\"', DoubleQuote),
    SeqTok(r'[^\"]+', String), SeqTok(r'\"', DoubleQuote))

    t_blank = LexTok(r' +', type=Blank)

    root = [t_dquote, t_blank]

lex = Lexer(StringTokens)
print('Example 1!')
data = '" This will"       "rock!"     "For sure!"'
tokens = lex.feed(data)
print('Consumed:', list(tokens))



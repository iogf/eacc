from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import Char

class CharTokens(XSpec):
    t_char  = LexTok(r'.', Char)
    root = [t_char]

data = 'abc'
lexer  = Lexer(CharTokens)
tokens = lexer.feed(data)

for ind in tokens:
    print('%s\nStart:%s\nEnd:%s\n' % (ind, ind.start, ind.end))

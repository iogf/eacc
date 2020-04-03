from eacc.lexer import Lexer, LexMap, LexNode, XSpec
from eacc.token import Char

class CharTokens(XSpec):
    lexmap = LexMap()

    t_char  = LexNode(r'.', Char)
    lexmap.add(t_char)

    root = [lexmap]

data = 'abc'
lexer  = Lexer(CharTokens)
tokens = lexer.feed(data)

for ind in tokens:
    print('%s\nStart:%s\nEnd:%s\n' % (ind, ind.start, ind.end))

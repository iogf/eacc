"""
This example tokenizes a document that is made up of sequences
of letters followed by blank characters. 

when a given set of non letter chars is used it generates
a lexical error. 

In the below example it generates an error due to mixing up
digits.
"""

from eacc.lexer import Lexer, LexMap, LexNode, XSpec
from eacc.token import Letter, Blank

class LetterTokens(XSpec):
    lexmap   = LexMap()
    t_blank  = LexNode(r' +', Blank)
    t_letter = LexNode(r'[a-zA-Z]', Letter)

    lexmap.add(t_letter, t_blank)
    root = [lexmap]

print('Example 1')
lex = Lexer(LetterTokens)
data = 'abc def uoc 123'
tokens = lex.feed(data)
print('Consumed:', list(tokens))




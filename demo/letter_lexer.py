"""
This example tokenizes a document that is made up of sequences
of letters followed by blank characters. 

when a given set of non letter chars is used it generates
a lexical error. 

In the below example it generates an error due to mixing up
digits.
"""

from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import Letter, Blank

class LetterTokens(XSpec):
    t_blank  = LexTok(r' +', Blank)
    t_letter = LexTok(r'[a-zA-Z]', Letter)

    root = [t_letter, t_blank]

print('Example 1')
lex = Lexer(LetterTokens)
data = 'abc def uoc 123'
tokens = lex.feed(data)
print('Consumed:', list(tokens))




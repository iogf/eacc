"""
"""

from eacc.lexer import XSpec, Lexer, SeqTok, LexTok, LexSeq
from eacc.token import Keyword, Identifier, RP, LP, Colon, Blank

class KeywordTokens(XSpec):
    t_if = LexSeq(SeqTok(r'if', type=Keyword),
    SeqTok(r'\s+', type=Blank))

    t_blank  = LexTok(r' +', type=Blank)
    t_lparen = LexTok(r'\(', type=LP)
    t_rparen = LexTok(r'\)', type=RP)
    t_colon  = LexTok(r'\:', type=Colon)

    # Match identifier only if it is not an if.
    t_identifier = LexTok(r'[a-zA-Z0-9]+', type=Identifier)

    root = [t_if, t_blank, t_lparen, 
    t_rparen, t_colon, t_identifier]

lex = Lexer(KeywordTokens)
data = 'if ifnum: foobar()'
tokens = lex.feed(data)
print('Consumed:', list(tokens))

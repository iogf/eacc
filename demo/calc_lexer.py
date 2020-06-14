"""
"""

from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank

class CalcTokens(XSpec):
    t_plus   = LexTok(r'\+', Plus)
    t_minus  = LexTok(r'\-', Minus)

    t_lparen = LexTok(r'\(', LP)
    t_rparen = LexTok(r'\)', RP)
    t_mul    = LexTok(r'\*', Mul)
    t_div    = LexTok(r'\/', Div)

    t_num    = LexTok(r'[0-9]+', Num, float)
    t_blank  = LexTok(r' +', Blank)


    root = [t_num, t_blank, t_plus, t_minus, t_lparen, 
    t_rparen, t_mul, t_div]

print('Example 1')
lex = Lexer(CalcTokens)
data = '1+1+(3*2+4)'
tokens = lex.feed(data)
tokens = list(tokens)
print('Consumed:', tokens)
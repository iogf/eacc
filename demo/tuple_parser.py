from eacc.lexer import Lexer, LexTok, XSpec
from eacc.eacc import Grammar, Rule, T, Eacc
from eacc.token import Blank, Num, Sof, Eof, LP, RP

class TupleTokens(XSpec):
    r_lparen = LexTok(r'\(', LP)
    r_rparen = LexTok(r'\)', RP)

    r_num    = LexTok(r'[0-9]+', Num)
    r_blank  = LexTok(r' +', Blank, discard=True)

    root = [r_lparen, r_rparen, r_num, r_blank]

class TupleGrammar(Grammar):
    # It means to accumulate as many Num tokens as possible.
    g_num = T(Num, min=1)

    # Then we trigge such a pattern in this rule.
    r_paren = Rule(LP, g_num, RP, type=Num)
    r_done  = Rule(Sof, Num, Eof)

    root = [r_paren, r_done]

def done(sof, expr, eof):
    print('Result:', expr)

print('Example 1')
lexer  = Lexer(TupleTokens)
eacc   = Eacc(TupleGrammar)
eacc.add_handle(TupleGrammar.r_done, done)

data   = '(1 (2 3) 4 (5 (6) 7))'
tokens = lexer.feed(data)
ptree  = eacc.build(tokens)
ptree  = list(ptree)
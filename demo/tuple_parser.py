from eacc.lexer import Lexer, LexTok, XSpec
from eacc.eacc import Grammar, Rule, Times, Eacc
from eacc.token import Blank, Num, Sof, Eof, LP, RP

class TupleTokens(XSpec):
    r_lparen = LexTok(r'\(', LP)
    r_rparen = LexTok(r'\)', RP)

    r_num    = LexTok(r'[0-9]+', Num)
    r_blank  = LexTok(r' +', Blank, discard=True)

    root = [r_lparen, r_rparen, r_num, r_blank]

class TupleGrammar(Grammar):
    # It means to accumulate as many Num tokens as possible.
    g_num = Times(Num, min=1, type=Num)

    # Then we trigge such a pattern in this rule.
    r_paren = Rule(LP, g_num, RP, type=Num)
    r_done  = Rule(Sof, Num, Eof)

    root = [r_paren, r_done]

def done(sof, expr, eof):
    print('Result:', expr)

if __name__ == '__main__':
    print('Example 1')
    data   = '(1 (1 1) ((((1)))))'
    
    lexer  = Lexer(TupleTokens)
    tokens = lexer.feed(data)
    eacc   = Eacc(TupleGrammar)
    
    ptree  = eacc.build(tokens)
    eacc.add_handle(TupleGrammar.r_done, done)
    
    ptree  = list(ptree)    
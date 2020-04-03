from eacc.lexer import Lexer, LexMap, LexNode, XSpec
from eacc.eacc import Grammar, Rule, T, Eacc, Struct
from eacc.token import Blank, Num, Sof, Eof, LP, RP

class TupleTokens(XSpec):
    lexmap = LexMap()
    r_lparen = LexNode(r'\(', LP)
    r_rparen = LexNode(r'\)', RP)

    r_num    = LexNode(r'[0-9]+', Num)
    r_blank  = LexNode(r' +', Blank, discard=True)

    lexmap.add(r_lparen, r_rparen, r_num, r_blank)
    root = [lexmap]

class TupleGrammar(Grammar):
    struct = Struct()

    # It means to accumulate as many Num tokens as possible.
    g_num = T(Num, min=1)

    # Then we trigge such a pattern in this rule.
    r_paren = Rule(LP, g_num, RP, type=Num)
    r_done  = Rule(Sof, Num, Eof)

    struct.add(r_paren, r_done)
    root = [struct]

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
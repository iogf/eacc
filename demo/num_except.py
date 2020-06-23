
from eacc.eacc import Rule, Grammar, Eacc, Except
from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import Sof, Eof, One, Two, Three, Four, Five, Blank

class ExprTokens(XSpec):
    t_one   = LexTok(r'1', One)
    t_two   = LexTok(r'2', Two)

    t_three = LexTok(r'3', Three)
    t_four  = LexTok(r'4', Four)
    t_five  = LexTok(r'5', Five)
    t_blank = LexTok(r' +', Blank, discard=True)

    root = [t_one, t_two, t_three, t_four, t_five, t_blank]

class ExprGrammar(Grammar):
    r_one = Rule(One, Except(Three), One)
    r_sof = Rule(Sof)
    r_eof = Rule(Eof)
    root  = [r_one, r_sof, r_eof]

if __name__ == '__main__':
    print('Example 1')
    lexer = Lexer(ExprTokens)
    eacc  = Eacc(ExprGrammar)
    data  = '121 141'
    
    tokens = lexer.feed(data)
    ptree  = eacc.build(tokens)
    ptree  = list(ptree)
    print(ptree)
    
    print('\nExample 2')
    data   = '1 2 1 1 3 1' # Will fail.
    tokens = lexer.feed(data)
    ptree  = eacc.build(tokens)
    ptree  = list(ptree)
    
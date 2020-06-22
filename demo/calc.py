
from eacc.eacc import Rule, Grammar, Eacc
from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

class CalcTokens(XSpec):
    # Used to extract the tokens.
    t_plus   = LexTok(r'\+', Plus)
    t_minus  = LexTok(r'\-', Minus)

    t_lparen = LexTok(r'\(', LP)
    t_rparen = LexTok(r'\)', RP)
    t_mul    = LexTok(r'\*', Mul)
    t_div    = LexTok(r'\/', Div)

    t_num    = LexTok(r'[0-9]+', Num, float)
    t_blank  = LexTok(r' +', Blank, discard=True)

    root = [t_plus, t_minus, t_lparen, t_num, 
    t_blank, t_rparen, t_mul, t_div]

class CalcGrammar(Grammar):
    # The token patterns when matched them become
    # ParseTree objects which have a type.
    r_paren = Rule(LP, Num, RP, type=Num)
    r_div   = Rule(Num, Div, Num, type=Num)
    r_mul   = Rule(Num, Mul, Num, type=Num)
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)
    o_plus   = Rule(Plus)

    r_plus  = Rule(Num, Plus, Num, type=Num, up=(o_mul, o_div))
    r_minus = Rule(Num, Minus, Num, type=Num, up=(o_mul, o_div))
    
    # The final structure that is consumed. Once it is
    # consumed then the process stops.
    r_done  = Rule(Sof, Num, Eof)

    root = [r_paren, r_plus, r_minus, r_mul, r_div, r_done]

# The handles mapped to the patterns to compute the expression result.
def plus(expr, sign, term):
    return expr.val() + term.val()

def minus(expr, sign, term):
    return expr.val() - term.val()

def div(term, sign, factor):
    return term.val()/factor.val()

def mul(term, sign, factor):
    return term.val() * factor.val()

def paren(left, expression, right):
    return expression.val()

def done(sof, num, eof):
    print('Result:', num.val())
    return num.val()

if __name__ == '__main__':
    data = '2 * 5 + 10 -(2 * 3 - 10 )+ 30/(1-3+ 4* 10 + (11/1))'
    lexer  = Lexer(CalcTokens)
    tokens = lexer.feed(data)
    eacc   = Eacc(CalcGrammar)
    
    # Link the handles to the patterns.
    eacc.add_handle(CalcGrammar.r_plus, plus)

    eacc.add_handle(CalcGrammar.r_minus, minus)
    eacc.add_handle(CalcGrammar.r_div, div)
    eacc.add_handle(CalcGrammar.r_mul, mul)
    eacc.add_handle(CalcGrammar.r_paren, paren)
    eacc.add_handle(CalcGrammar.r_done, done)

    ptree = eacc.build(tokens)
    ptree = list(ptree)
    
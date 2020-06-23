
from eacc.eacc import Rule, Grammar, Eacc
from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import TokType, Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

class Expr(TokType):
    pass

class CalcTokens(XSpec):
    # Token extractors. When it matches the regex's it instantiate
    # a Token class with the specified type.
    t_plus  = LexTok(r'\+', Plus)
    t_minus = LexTok(r'\-', Minus)

    t_lparen = LexTok(r'\(', LP)
    t_rparen = LexTok(r'\)', RP)
    t_mul    = LexTok(r'\*', Mul)
    t_div    = LexTok(r'\/', Div)

    # Automatically convert the token value to a float.
    t_num    = LexTok(r'[0-9]+', Num, float)

    # White spaces are discarded.
    t_blank  = LexTok(r' +', Blank, discard=True)

    root = [t_plus, t_minus, t_lparen, t_num, 
    t_blank, t_rparen, t_mul, t_div]

class CalcGrammar(Grammar):
    r_paren = Rule(LP, Expr, RP, type=Expr)
    r_div   = Rule(Expr, Div, Expr, type=Expr)
    r_mul   = Rule(Expr, Mul, Expr, type=Expr)

    # The lookahead rules to fix ambiguity.
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)
    r_plus  = Rule(Expr, Plus, Expr, type=Expr, up=(o_mul, o_div))
    r_minus = Rule(Expr, Minus, Expr, type=Expr, up=(o_mul, o_div))
    r_num   = Rule(Num, type=Expr)
    r_done  = Rule(Sof, Expr, Eof)

    root = [r_paren, r_plus, r_minus, 
    r_mul, r_div, r_num, r_done]

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

def num(num):
    """
    The result will be a ParseTree instance with type
    expression and value equal to the token num.
    """
    return num.val()

def done(sof, expression, eof):
    """
    When this pattern is trigged then the expression is
    fully evaluated. 
    """
    print('Result:', expression.val())
    return expression.val()

if __name__ == '__main__':
    data = '2 * 5 + 10 -(2 * 3 - 10 )+ 30/(1-3+ 4* 10 + (11/1))'
    lexer  = Lexer(CalcTokens)
    tokens = lexer.feed(data)
    eacc   = Eacc(CalcGrammar)
    
    # Map the patterns to handles to evaluate the expression.
    eacc.add_handle(CalcGrammar.r_plus, plus)
    eacc.add_handle(CalcGrammar.r_minus, minus)
    eacc.add_handle(CalcGrammar.r_div, div)
    eacc.add_handle(CalcGrammar.r_mul, mul)
    eacc.add_handle(CalcGrammar.r_paren, paren)
    eacc.add_handle(CalcGrammar.r_done, done)
    eacc.add_handle(CalcGrammar.r_num, num)
    
    # Finally build the AST.
    ptree = eacc.build(tokens)
    ptree = list(ptree)
    

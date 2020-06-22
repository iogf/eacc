from eacc.eacc import Rule, Grammar, Eacc
from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import TokType, Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

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

class Expr(TokType):
    pass

class Term(TokType):
    pass

class Factor(TokType):
    pass

class CalcGrammar(Grammar):
    r_plus  = Rule(Expr, Plus, Term, type=Expr)
    r_minus = Rule(Expr, Minus, Term, type=Expr)
    r_expr  = Rule(Term, type=Expr)

    r_div   = Rule(Term, Div, Factor, type=Term)
    r_mul   = Rule(Term, Mul, Factor, type=Term)
    r_term  = Rule(Factor, type=Term)

    r_factor = Rule(Num, type=Factor)
    r_paren = Rule(LP, Num, RP, type=Factor)
    r_done  = Rule(Sof, Expr, Eof)

    root = [r_plus, r_minus, r_expr, r_mul, r_div, r_factor, r_term, r_paren, r_done]

# The handles mapped to the patterns to compute the expression result.
def plus(expr, sign, term):
    return expr.val() + term.val()

def minus(expr, sign, term):
    return expr.val() - term.val()

def expr(term):
    return term.val()

def div(term, sign, factor):
    return term.val()/factor.val()

def mul(term, sign, factor):
    return term.val() * factor.val()

def term(num):
    return num.val()

def factor(num):
    return num.val()

def paren(left, expression, right):
    return expression.val()

def done(sof, num, eof):
    print('Result:', num.val())
    return num.val()

data = '2 * 5 + 10 -(2 * 3 - 10 )+ 30/(1-3+ 4* 10 + (11/1))'

lexer  = Lexer(CalcTokens)
tokens = lexer.feed(data)
eacc   = Eacc(CalcGrammar)

# Link the handles to the patterns.
eacc.add_handle(CalcGrammar.r_plus, plus)
eacc.add_handle(CalcGrammar.r_minus, minus)
eacc.add_handle(CalcGrammar.r_expr, expr)
eacc.add_handle(CalcGrammar.r_term, term)
eacc.add_handle(CalcGrammar.r_factor, factor)
eacc.add_handle(CalcGrammar.r_div, div)
eacc.add_handle(CalcGrammar.r_mul, mul)
eacc.add_handle(CalcGrammar.r_paren, paren)
eacc.add_handle(CalcGrammar.r_done, done)

ptree = eacc.build(tokens)
ptree = list(ptree)


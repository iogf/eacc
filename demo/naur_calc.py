
from eacc.eacc import Rule, Grammar, Struct, Eacc
from eacc.lexer import Lexer, LexMap, LexNode, XSpec
from eacc.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

class CalcTokens(XSpec):
    # The set of tokens that is used in the grammar.
    expression = LexMap()

    # Token extractors. When it matches the regex's it instantiate
    # a Token class with the specified type.
    t_plus  = LexNode(r'\+', Plus)
    t_minus = LexNode(r'\-', Minus)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)
    t_mul    = LexNode(r'\*', Mul)
    t_div    = LexNode(r'\/', Div)

    # Automatically convert the token value to a float.
    t_num    = LexNode(r'[0-9]+', Num, float)

    # White spaces are discarded.
    t_blank  = LexNode(r' +', Blank, discard=True)

    expression.add(t_plus, t_minus, t_lparen, t_num, 
    t_blank, t_rparen, t_mul, t_div)

    # You can model your lexer with multiple LexMap
    # instances and combine them with LexSeq it turns possible
    # and easy to validate documents in the lexical step.
    root = [expression]

class CalcGrammar(Grammar):
    # A mathematical expression is a structure
    # of data.
    expression = Struct()
    
    # The rules to parse the structure.
    r_paren = Rule(LP, expression, RP, type=expression)
        
    # The resulting parse tree will have type expression it will be
    # rematched again against all the rules.
    r_div   = Rule(expression, Div, expression, type=expression)
    r_mul   = Rule(expression, Mul, expression, type=expression)

    # The lookahead rules to fix ambiguity.
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)

    r_plus  = Rule(expression, Plus, expression, 
    type=expression, up=(o_mul, o_div))

    r_minus = Rule(expression, Minus, expression, 
    type=expression, up=(o_mul, o_div))

    # When a Num is matched it is associated to the type
    # expression then rematched against the previous rules
    r_num = Rule(Num, type=expression)

    # When a math expression is fully evaluated it will result
    # in the below pattern. This rule is used to consume the resulting
    # structure. Sof stands for stard of file. 
    #
    # The resulting structure will contain the math expression
    # value.
    r_done  = Rule(Sof, expression, Eof)

    expression.add(r_paren, r_plus, r_minus, 
    r_mul, r_div, r_num, r_done)

    # You can define multiple structures to simplify
    # handling more complex grammars and combine them
    # inside rules.
    root = [expression]

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


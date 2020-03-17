# Yacc

If it looks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck.

Python Yacc is a parsing library with a powerful Backus-Naur variation. It implements a powerful lexer
that can be used to validate documents. It also implements a parsing mechanism to build AST's for documents.

The notation to express grammar consists of defining token patterns in a similar fashion to Backus-Naur.
The similarity with Backus-Naur form is merely superficial because in yacc it is purely using python code
to express the token patterns.

A token has a type when a sequence of tokens is matched it evaluates to a specific type then rematcned
again against the existing rules. When a given token pattern is trigged it is possible
to attach a handle to be executed. The handle arguments are the tokens that were matched.

You can build more complex AST's using that approach with handles or you can just evaluate
the AST's resulting from your grammar specification at the time it is being parsed. It works fairly
well for simple grammars like basic mathematical expressions.

Characterization plays a basic role in human reasoning. it is necessary
to characterize first to reason. Knowing a duck is a duck it gives you the opportunity to trigger
more complex patterns like when the duck is with chickens or wolves to take an action.

The approach of defining types for basic structures of data then matching these against existing
rules it automatically handles the powerful recursivity that exists in Backus-Naur notation 
with a higher level of expressivity.

The parser has a lookahead mechanism to express precedence when matching rules. It is quite powerful
to implement parsers to handle document structures. The lookahead mechanism makes it possible
to handle ambiguous grammar in a similar fashion to Backus-Naur in a succinct approach.

### Yacc-like/Parser

The parser syntax is consistent and concrete. It allows you to link handles to token patterns and
evaluate these rules according to your necessities.

The approach of associating a token pattern to a type it makes possible to specify ambiguous
grammar in a Backus-Naur form essentially.

The below code specifies a lexer and a parsing approach for a simple expression calculator.

~~~python

from yacc.yacc import Rule, Grammar, Struct, Yacc
from yacc.lexer import Lexer, LexMap, LexNode, XSpec
from yacc.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

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
yacc   = Yacc(CalcGrammar)

# Map the patterns to handles to evaluate the expression.
yacc.add_handle(CalcGrammar.r_plus, plus)
yacc.add_handle(CalcGrammar.r_minus, minus)
yacc.add_handle(CalcGrammar.r_div, div)
yacc.add_handle(CalcGrammar.r_mul, mul)
yacc.add_handle(CalcGrammar.r_paren, paren)
yacc.add_handle(CalcGrammar.r_done, done)
yacc.add_handle(CalcGrammar.r_num, num)

# Finally build the AST.
ptree = yacc.build(tokens)
ptree = list(ptree)
~~~

That would give you:

~~~
[tau@archlinux demo]$ python calc.py 
Result: 24.612244897959183
~~~

That is basically.

~~~
expression : expression PLUS expression
            | expression MINUS expression
            | expression TIMES expression
            | expression DIVIDE expression
            | LPAREN expression RPAREN
            | NUMBER
~~~

The parser has a lookahead mechanism based on rules as well.

~~~python
    r_plus  = Rule(Num, Plus, Num, type=Num, up=(o_mul, o_div))
~~~

The above rule will be matched only if the below rules aren't matched ahead.

~~~python
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)
~~~

When a mathematical expression is well formed it will result to the following structure.

~~~
Sof expression Eof
~~~

Which is matched by the rule below.

~~~python
    r_done  = Rule(Sof, expression, Eof)
~~~

That is mapped to the handle below. It will merely print the resulting value.

~~~python
def done(sof, expression, eof):
    print('Result:', expression.val())
    return expression.val()
~~~

In case it is not a valid mathematical expression then it raises an exception. 
When a given document is well formed, the defined rules will consume it entirely.

The idea behind yacc arouse when i was working to abstract a set of existing tools to improve 

https://github.com/vyapp/vy

That is my vim-like thing in python.

# Install

**Note:** Work with python3 only.

~~~
pip install yacc
~~~

Documentation
=============

[Wiki](https://github.com/iogf/yacc/wiki)


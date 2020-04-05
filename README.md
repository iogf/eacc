# Eacc

Python Eacc is a parsing tool it implements a flexible lexer and a straightforward approach
to build AST's from documents. 

Documents are split into tokens and a token has a type when a sequence of tokens is matched 
it evaluates to a specific type then rematcned again against the existing rules. 

When a given token pattern is trigged it is possible to attach a handle to be executed. 
The handle arguments are the tokens that were matched.

You can build more complex AST's using that approach with handles or you can just evaluate
the AST's resulting from your grammar specification at the time it is being parsed. It works fairly
well for simple grammars like basic mathematical expressions.

The approach of defining types for basic structures of data then matching these against existing
rules it automatically handles the powerful recursivity that exists in Backus-Naur notation 
with a higher level of expressivity.

The parser has a lookahead mechanism to express precedence when matching rules. It is quite powerful
to implement parsers to handle document structures. The lookahead mechanism makes it possible
to handle ambiguous grammar in a similar fashion to Backus-Naur in a succinct approach.

The code below specifies a lexer and a parsing approach for a simple expression calculator.
When one of the mathematical operations +, -, * or / is executed then the result is a number

Based on such a simple assertion it is possible to implement our calculator. 

~~~python
from eacc.eacc import Rule, Grammar, Struct, Eacc
from eacc.lexer import Lexer, LexMap, LexNode, XSpec
from eacc.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

class CalcTokens(XSpec):
    # The set of tokens that is used in the grammar.
    expression = LexMap()

    # Used to extract the tokens.
    t_plus   = LexNode(r'\+', Plus)
    t_minus  = LexNode(r'\-', Minus)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)
    t_mul    = LexNode(r'\*', Mul)
    t_div    = LexNode(r'\/', Div)

    t_num    = LexNode(r'[0-9]+', Num, float)
    t_blank  = LexNode(r' +', Blank, discard=True)

    expression.add(t_plus, t_minus, t_lparen, t_num, 
    t_blank, t_rparen, t_mul, t_div)

    root = [expression]

class CalcGrammar(Grammar):
    # The grammar struct.
    expression = Struct()

    # The token patterns when matched them become
    # ParseTree objects which have a type.
    r_paren = Rule(LP, Num, RP, type=Num)
    r_div   = Rule(Num, Div, Num, type=Num)
    r_mul   = Rule(Num, Mul, Num, type=Num)
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)

    r_plus  = Rule(Num, Plus, Num, type=Num, up=(o_mul, o_div))
    r_minus = Rule(Num, Minus, Num, type=Num, up=(o_mul, o_div))

    # The final structure that is consumed. Once it is
    # consumed then the process stops.
    r_done  = Rule(Sof, Num, Eof)

    expression.add(r_paren, r_plus, r_minus, r_mul, r_div, r_done)
    root = [expression]

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
~~~

That outputs:

~~~
[tau@archlinux demo]$ python calc.py 
Result: 24.612244897959183
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

In case the above rule is matched then the result has type Num it will be rematched
against the existing rules and so on.

When a mathematical expression is well formed it will result to the following structure.

~~~
Sof Num Eof
~~~

Which is matched by the rule below.

~~~python
    r_done  = Rule(Sof, Num, Eof)
~~~

That rule is mapped to the handle below. It will merely print the resulting value.

~~~python
def done(sof, num, eof):
    print('Result:', num.val())
    return num.val()
~~~

The Sof and Eof are start of file and end of file tokens. These are automatically inserted
by the parser.

In case it is not a valid mathematical expression then it raises an exception. 
When a given document is well formed, the defined rules will consume it entirely.

The lexer is really flexible it can handle some interesting cases in a short and simple manner.

~~~python
from yacc.lexer import XSpec, Lexer, LexMap, SeqNode, LexNode, LexSeq
from yacc.token import Token, Keyword, Identifier, RP, LP, Colon, Blank

class KeywordTokens(XSpec):
    lexmap = LexMap()
    t_if = LexSeq(SeqNode(r'if', type=Keyword),
    SeqNode(r'\s+', type=Blank))

    t_blank  = LexNode(r' +', type=Blank)
    t_lparen = LexNode(r'\(', type=LP)
    t_rparen = LexNode(r'\)', type=RP)
    t_colon  = LexNode(r'\:', type=Colon)

    # Match identifier only if it is not an if.
    t_identifier = LexNode(r'[a-zA-Z0-9]+', type=Identifier)

    lexmap.add(t_if, t_blank, t_lparen, 
    t_rparen, t_colon, t_identifier)
    root = [lexmap]

lex = Lexer(KeywordTokens)
data = 'if ifnum: foobar()'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
~~~

That would output:

~~~
Consumed: [Keyword('if'), Blank(' '), Identifier('ifnum'), Colon(':'),
Blank(' '), Identifier('foobar'), LP('('), RP(')')]
~~~

The above example handles the task of tokenizing keywords correctly. The SeqNode class 
works together with LexSeq to extract the tokens based on a given regex while LexNode works 
on its own to extract tokens that do not demand a lookahead step.

# Install

**Note:** Work with python3 only.

~~~
pip install eacc
~~~

Documentation
=============

[Wiki](https://github.com/iogf/eacc/wiki)


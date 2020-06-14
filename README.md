# Eacc

Python Eacc is a parsing tool it implements a flexible lexer and a straightforward approach
to analyze documents. It uses Python code to specify both lexer and grammar for a given
document. Eacc can handle succinctly most parsing cases that existing Python parsing tools
propose to address. 

Documents are split into tokens and a token has a type when a sequence of tokens is matched 
it evaluates to a specific type then rematcned again against the existing rules. The types
can be function objects it means patterns can be evaluated based on extern conditions. 

The fact of it being possible to have a grammar rule associated to a type and the
type being variable in the context of the program it makes eacc useful for some text analysis problems.

A document grammar is written mostly in an ambiguous manner. The parser has a lookahead 
mechanism to express precedence when matching rules. 

It is possible to extend the document grammar at the time it is being parsed. Such
a feature is interesting to handle some edge cases.

# Features

- **Fast and flexible Lexer**
    * Use class inheritance to extend/modify your existing lexers.

- **Handle broken documents.**
    * Useful in some edge cases.

- **Short implementation**
    * You can easily extend or modify functionalities.

- **Powerful but easy to learn**
    * Learn a few classes workings to implement a parser.

- **Pythonic notation for grammars**
    * No need to dig deep into grammar theory.


**Note:** For a real and more sophisticated example of eacc usage check out.

Crocs is capable of reading a regex string then generating possible matches for the
inputed regex.

https://github.com/iogf/crocs

# Basic Example

The code below specifies a lexer and a parsing approach for a simple expression calculator.
When one of the mathematical operations +, -, * or / is executed then the result is a number

Based on such a simple assertion it is possible to implement our calculator. 

~~~python

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

~~~

The defined rule below fixes precedence in the above ambiguous grammar.

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
from eacc.lexer import XSpec, Lexer, SeqTok, LexTok, LexSeq
from eacc.token import Keyword, Identifier, RP, LP, Colon, Blank

class KeywordTokens(XSpec):
    t_if = LexSeq(SeqTok(r'if', type=Keyword),
    SeqTok(r'\s+', type=Blank))

    t_blank  = LexTok(r' +', type=Blank)
    t_lparen = LexTok(r'\(', type=LP)
    t_rparen = LexTok(r'\)', type=RP)
    t_colon  = LexTok(r'\:', type=Colon)

    # Match identifier only if it is not an if.
    t_identifier = LexTok(r'[a-zA-Z0-9]+', type=Identifier)

    root = [t_if, t_blank, t_lparen, 
    t_rparen, t_colon, t_identifier]

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

The above example handles the task of tokenizing keywords correctly. The SeqTok class 
works together with LexSeq to extract the tokens based on a given regex while LexNode works 
on its own to extract tokens that do not demand a lookahead step.

# Install

**Note:** Work with python3 only.

~~~
pip install eacc
~~~

## [Documentation](https://github.com/iogf/eacc/wiki)



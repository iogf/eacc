"""
"""

from eacc.eacc import Eacc, Rule, Grammar, Struct
from eacc.lexer import XSpec, Lexer, LexMap, LexNode
from eacc.token import Blank, Word, TokVal, Sof, Eof

class WordTokens(XSpec):
    lexmap  = LexMap()
    t_word  = LexNode(r'[a-zA-Z]+', Word)
    t_blank = LexNode(r' +', type=Blank, discard=True)

    lexmap.add(t_word, t_blank)
    root = [lexmap]

class WordGrammar(Grammar):
    struct     = Struct()
    r_phrase0  = Rule(TokVal('alpha'), TokVal('beta'))
    r_phrase1  = Rule(TokVal('gamma'), TokVal('zeta'))
    r_sof      = Rule(Sof)
    r_eof      = Rule(Eof)

    struct.add(r_phrase1, r_phrase0, r_sof, r_eof)
    root = [struct]

data = 'alpha beta gamma zeta' 
lexer = Lexer(WordTokens)
eacc  = Eacc(WordGrammar)
tokens = lexer.feed(data)
ptree  = eacc.build(tokens)
print(list(ptree))

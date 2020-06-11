"""
"""

from eacc.eacc import Eacc, Rule, Grammar, TokVal
from eacc.lexer import XSpec, Lexer, LexTok
from eacc.token import Blank, Word, Sof, Eof

class WordTokens(XSpec):
    t_word  = LexTok(r'[a-zA-Z]+', Word)
    t_blank = LexTok(r' +', type=Blank, discard=True)

    root = [t_word, t_blank]

class WordGrammar(Grammar):
    r_phrase0  = Rule(TokVal('alpha'), TokVal('beta'))
    r_phrase1  = Rule(TokVal('gamma'), TokVal('zeta'))
    r_sof      = Rule(Sof)
    r_eof      = Rule(Eof)

    root = [r_phrase1, r_phrase0, r_sof, r_eof]

if __name__ == '__main__':
    data = 'alpha beta gamma zeta' 
    lexer = Lexer(WordTokens)
    eacc  = Eacc(WordGrammar)
    tokens = lexer.feed(data)
    ptree  = eacc.build(tokens)
    print(list(ptree))
    
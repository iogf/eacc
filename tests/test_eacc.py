import unittest
from eacc.eacc import Rule, Grammar, Eacc, Except, TokVal, Only
from eacc.lexer import Lexer, LexTok, XSpec

from eacc.token import Sof, Eof

class TestTokOp(unittest.TestCase):
    def setUp(self):
        pass

class TestOnly(unittest.TestCase):
    class ExprTokens(XSpec):
        pass

    class ExprGrammar(Grammar):
        pass

    def setUp(self):
        self.lexer  = Lexer(self.ExprTokens)
        self.eacc   = Eacc(self.ExprGrammar)

    def test_opexec(self):
        data   = '121 141'
        tokens = lexer.feed(data)
        ptree = list(eacc.build(tokens))
        
if __name__ == '__main__':
    unittest.main()
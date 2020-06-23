import unittest
from eacc.eacc import Rule, Grammar, Eacc, EaccError, TokVal, \
Except, Times, Only, DotTok
from eacc.lexer import Lexer, LexTok, XSpec
from eacc.token import Word, Plus, Minus, LP, RP, Mul, Div, \
Num, Blank, Sof, Eof, One, Two, Three, Four, Five

class TestRule(unittest.TestCase):
    class CalcTokens(XSpec):
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
        r_paren = Rule(LP, Num, RP, type=Num)
        r_div   = Rule(Num, Div, Num, type=Num)
        r_mul   = Rule(Num, Mul, Num, type=Num)
        o_div   = Rule(Div)
        o_mul   = Rule(Mul)
    
        r_plus  = Rule(Num, Plus, Num, type=Num, up=(o_mul, o_div))
        r_minus = Rule(Num, Minus, Num, type=Num, up=(o_mul, o_div))
    
        r_done  = Rule(Sof, Num, Eof)
        root = [r_paren, r_plus, r_minus, r_mul, r_div, r_done]
    
    def plus(self, expr, sign, term):
        return expr.val() + term.val()
    
    def minus(self, expr, sign, term):
        return expr.val() - term.val()
    
    def div(self, term, sign, factor):
        return term.val()/factor.val()
    
    def mul(self, term, sign, factor):
        return term.val() * factor.val()
    
    def paren(self, left, expression, right):
        return expression.val()
    
    def done(self, sof, num, eof):
        print('Result:', num.val())
        return num.val()
    
    def setUp(self):
        self.lexer  = Lexer(self.CalcTokens)
        self.eacc   = Eacc(self.CalcGrammar)
        
        # Link the handles to the patterns.
        self.eacc.add_handle(self.CalcGrammar.r_plus, self.plus)
        self.eacc.add_handle(self.CalcGrammar.r_minus, self.minus)
        self.eacc.add_handle(self.CalcGrammar.r_div, self.div)
        self.eacc.add_handle(self.CalcGrammar.r_mul, self.mul)
        self.eacc.add_handle(self.CalcGrammar.r_paren, self.paren)
        self.eacc.add_handle(self.CalcGrammar.r_done, self.done)
        
    def test0(self):
        data = '1+2/3*(3*2 - 1) /(1-1-2-3-1+2)*3/ (1 - 2)*10'
        tokens = self.lexer.feed(data)
        ptree = self.eacc.build(tokens)
        ptree = list(ptree)
        print('Expr:', data)
        self.assertEqual(ptree[-1].val(), eval(data))

    def test1(self):
        data = '(1+2/3*(3*2 - 1)) + ((1 - 2)*10)'
        tokens = self.lexer.feed(data)
        ptree = self.eacc.build(tokens)
        ptree = list(ptree)
        print('Expr:', data)
        self.assertEqual(ptree[-1].val(), eval(data))

    def test2(self):
        data = '((1+2/3*(3*2 - 1)) + ((1 - 2)*10))'
        tokens = self.lexer.feed(data)
        ptree = self.eacc.build(tokens)
        ptree = list(ptree)
        print('Expr:', data)
        self.assertEqual(ptree[-1].val(), eval(data))

    def test3(self):
        data = '(1/2) * (3/4) * (5/2/3/5/2*1)/((((((1))))))'
        tokens = self.lexer.feed(data)
        ptree = self.eacc.build(tokens)
        ptree = list(ptree)
        print('Expr:', data)
        self.assertEqual(ptree[-1].val(), eval(data))

    def test4(self):
        data = '(1/2) * (3/4) * (5 2)'
        tokens = self.lexer.feed(data)
        print('Expr:', data)
        ptree = self.eacc.build(tokens)

        with self.assertRaises(EaccError):
            ptree = list(ptree)

    def test4(self):
        data = '(1/2) * 3/4) * (512)'
        tokens = self.lexer.feed(data)
        print('Expr:', data)
        ptree = self.eacc.build(tokens)

        with self.assertRaises(EaccError):
            ptree = list(ptree)

    def test5(self):
        data = '1+2*2/2 - 2/2 - 2*2/2+1'
        tokens = self.lexer.feed(data)
        ptree = self.eacc.build(tokens)
        ptree = list(ptree)
        print('Expr:', data)
        self.assertEqual(ptree[-1].val(), eval(data))

class TestTokVal(unittest.TestCase):
    class Wordtokens(XSpec):
        t_word  = LexTok(r'[a-zA-Z]+', Word)
        t_blank = LexTok(r' +', type=Blank, discard=True)
    
        root = [t_word, t_blank]
    
    class WordGrammar(Grammar):
        r_phrase0  = Rule(TokVal('alpha'), TokVal('beta'))
        r_phrase1  = Rule(TokVal('gamma'), TokVal('zeta'))
        r_phrase2  = Rule(TokVal('abc'), TokVal('def'))

        r_sof      = Rule(Sof)
        r_eof      = Rule(Eof)
    
        root = [r_phrase1, r_phrase0, r_phrase2, r_sof, r_eof]
    
    def setUp(self):
        self.lexer = Lexer(self.Wordtokens)
        self.eacc  = Eacc(self.WordGrammar)
        
    def test0(self):
        data = 'alpha beta gamma zeta'
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)
        ptree = list(ptree)
    
    def test1(self):
        data = 'gamma zeta     abc      def     alpha beta '  
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)
        ptree = list(ptree)

    def test2(self):
        data = 'gamma zeta'  
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)
        ptree = list(ptree)

    def test3(self):
        data = 'gamma zeta'  
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)
        ptree = list(ptree)

    def test4(self):
        data = 'gamma zeta abc'  
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

        with self.assertRaises(EaccError):
            ptree = list(ptree)

class TestOps0(unittest.TestCase):
    class ExprTokens(XSpec):
        t_one   = LexTok(r'1', One)
        t_two   = LexTok(r'2', Two)
    
        t_three = LexTok(r'3', Three)
        t_four  = LexTok(r'4', Four)
        t_five  = LexTok(r'5', Five)
        t_blank = LexTok(r' +', Blank, discard=True)
    
        root = [t_one, t_two, t_three, t_four, t_five, t_blank]
    
    class ExprGrammar(Grammar):
        r_num = Rule(One, Except(Three), One)

        r_sof = Rule(Sof)
        r_eof = Rule(Eof)
    
        root = [r_num, r_sof, r_eof]
    
    def setUp(self):
        self.lexer = Lexer(self.ExprTokens)
        self.eacc  = Eacc(self.ExprGrammar)

    def test0(self):
        data = '121 141 141 141'
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)
        ptree = list(ptree)

class TestOps1(TestOps0):
    class ExprGrammar(Grammar):
        r_num = Rule(One, Times(Except(One)), One)
        r_sof = Rule(Sof)
        r_eof = Rule(Eof)

        root = [r_num, r_sof, r_eof]

    def test0(self):
        data = '122221 14441 121 12241'
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)
        ptree = list(ptree)

class TestOps2(TestOps0):
    class ExprGrammar(Grammar):
        r_num = Rule(Four, Times(Only(Five, Two)), Four)
        r_sof = Rule(Sof)
        r_eof = Rule(Eof)

        root = [r_num, r_sof, r_eof]

    def test0(self):
        data = '122221 14441 121 12241 455554'

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

        with self.assertRaises(EaccError):
            ptree = list(ptree)

    def test1(self):
        data = '455554 45555555554 455554'

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

    def test2(self):
        data = '42222524 42222224 4555552554'

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

    def test3(self):
        data = '422322524 42222224 4555552554'

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

        with self.assertRaises(EaccError):
            ptree = list(ptree)

class TestOps3(TestOps0):
    class ExprGrammar(Grammar):
        r_num = Rule(Two, DotTok(), Two)
        r_sof = Rule(Sof)
        r_eof = Rule(Eof)

        root = [r_num, r_sof, r_eof]


    def test0(self):
        data = '122221 14441 121 12241 422224'

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

        with self.assertRaises(EaccError):
            ptree = list(ptree)

class TestOps4(TestOps0):
    class ExprGrammar(Grammar):
        r_num0 = Rule(One, Two, Three, Four)
        r_num1 = Rule(One, Two, Three)

        r_num2 = Rule(One, Two)
        r_sof = Rule(Sof)
        r_eof = Rule(Eof)

        root = [r_num0, r_num1, r_num2, r_sof, r_eof]

    def test0(self):
        data = '12 1234 12 1234 123'

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

        ptree = list(ptree)

    def test1(self):
        data = '123 1234 12 1234 1 '

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

        with self.assertRaises(EaccError):
            ptree = list(ptree)

    def test2(self):
        data = '1234 12'

        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)

        ptree = list(ptree)

class TestOps5(TestOps0):
    class ExprGrammar(Grammar):
        r_num0 = Rule(Four, Times(Only(Five, Two)), Four)
        r_num1 = Rule(Four, Times(Only(Five, Two)), One)

        r_sof = Rule(Sof)
        r_eof = Rule(Eof)

        root = [r_num0, r_num1, r_sof, r_eof]

    def test0(self):
        data = '4222224 45555554 42222221'
        tokens = self.lexer.feed(data)
        ptree  = self.eacc.build(tokens)
        ptree = list(ptree)


if __name__ == '__main__':
    unittest.main()
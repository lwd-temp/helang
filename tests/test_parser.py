import unittest

from helang.parser import Parser
from helang.lexer import Lexer
from helang.u8 import U8
from helang.he_ast import Test5GAST
from helang.speed_tester import MUSICS


class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('1! 5! 哥们在这给你测试!')

    def setUp(self) -> None:
        self.def_code = """
            u8 list1 = 1 | 2 | 3;
            u8 list2 = [3];
        """

        self.u8_set_code = """
            u8 a = 1 | 2 | 3;
            a[1 | 3] = 12;
        """

        # You need to provide variable a.
        self.u8_get_code = """
            u8 b = a[1 | 3];
        """

        # You need to provide variable a.
        self.print_code = """
            print a[1 | 2];
        """

        self.test_5g_code = """
            test5g;
        """

    def test_parse_def(self):
        lexer = Lexer(self.def_code)
        env = dict()
        Parser(lexer.lex()).parse().evaluate(env)
        self.assertEqual(env['list1'].value, [1, 2, 3])
        self.assertEqual(env['list2'].value, [0, 0, 0])

    def test_parse_u8_set(self):
        env = dict()
        Parser(Lexer(self.u8_set_code).lex()).parse().evaluate(env)
        self.assertEqual(env['a'].value, [12, 2, 12])

    def test_parse_u8_get(self):
        env = {'a': U8([2, 3, 4])}
        Parser(Lexer(self.u8_get_code).lex()).parse().evaluate(env)
        self.assertEqual(env['b'].value, [2, 4])

    def test_parse_print(self):
        env = {'a': U8([2, 3, 4])}
        printed_content = Parser(Lexer(self.print_code).lex()).parse().evaluate(env)
        self.assertEqual(printed_content.value, [2, 3])

    def test_parse_test_5g(self):
        # Hack the testing musics to reduce time.
        MUSICS.clear()
        MUSICS.append('TEST')
        result = Parser(Lexer(self.test_5g_code).lex()).parse().evaluate(dict())
        self.assertEqual(result.value, Test5GAST.SPECIAL_VALUE)

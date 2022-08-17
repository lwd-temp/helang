from helang.lexer import Lexer
from helang.tokens import Token, TokenKind


code = """
u8 a = 1 | // Comment inline.
2
// Comment for single line.
"""


def test_lexer():
    lexer = Lexer(code)
    tokens = lexer.lex()
    expected = [
        Token('u8', TokenKind.U8),
        Token('a', TokenKind.IDENT),
        Token('=', TokenKind.ASSIGN),
        Token('1', TokenKind.NUMBER),
        Token('|', TokenKind.OR),
        Token('2', TokenKind.NUMBER)
    ]

    assert tokens == expected

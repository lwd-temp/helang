from .tokens import Token, TokenKind
from .exceptions import BadStatementException
from .he_ast import AST, VoidAST, ListAST, VarDefAST, VarAssignAST, VarExprAST,\
    PrintAST, SprintAST, VarIncrementAST, U8SetAST, U8GetAST, Test5GAST,\
    EmptyU8InitAST, OrU8InitAST, CyberspacesAST
from typing import List, Optional, Callable, Tuple


class Parser:
    def __init__(self, tokens: List[Token]):
        self._tokens = tokens
        self._pos = 0

    def _expect(self, expected_kind: TokenKind, validator: Optional[Callable[[Token], bool]] = None):
        if self._pos >= len(self._tokens):
            raise BadStatementException('no more tokens')

        token = self._tokens[self._pos]

        if token.kind != expected_kind:
            raise BadStatementException(f'expected {expected_kind} at pos {self._pos}, got {token.kind}')

        if validator is not None and not validator(token):
            raise BadStatementException(f'failed to pass custom validator at offset {self._pos}')

        self._pos += 1
        return token

    def parse(self) -> AST:
        """
        root
          : print
          | sprint
          | u8_set
          | var_def
          | var_declare
          | var_assign
          | var_increment
          | expr
          | test_5g
          | semicolon
          | cyberspaces
          ;
        :return: parsed abstract syntax tree.
        """
        root_parsers = [
            self._root_parse_print,
            self._root_parse_sprint,
            self._root_parse_u8_set,
            self._root_parse_var_def,
            self._root_parse_var_declare,
            self._root_parse_var_assign,
            self._root_parse_var_increment,
            self._root_parse_expr,
            self._root_parse_test_5g,
            self._root_parse_semicolon,
            self._root_parse_cyberspaces,
        ]
        asts = []
        while self._pos < len(self._tokens):
            for parser in root_parsers:
                saved_pos = self._pos
                try:
                    asts.append(parser())
                    break
                except BadStatementException:
                    self._pos = saved_pos
            else:
                raise BadStatementException(f'failed to parse tokens started from {self._pos}, '
                                            f'which is {self._tokens[self._pos]}')
        # Return the AST itself if there is only one.
        return ListAST(asts) if len(asts) != 1 else asts[0]

    def _root_parse_cyberspaces(self) -> CyberspacesAST:
        """
        cyberspaces: CYBERSPACES SEMICOLON;
        :return: AST to check if you are in the Cyber Spaces.
        """
        self._expect(TokenKind.CYBERSPACES)
        self._expect(TokenKind.SEMICOLON)
        return CyberspacesAST()

    def _root_parse_semicolon(self) -> VoidAST:
        """
        semicolon: SEMICOLON;
        :return: void AST for sure.
        """
        self._expect(TokenKind.SEMICOLON)
        return VoidAST()

    def _root_parse_var_def(self) -> VarDefAST:
        """
        var_def: U8 IDENT ASSIGN expr SEMICOLON;
        :return: variable definition AST.
        """
        self._expect(TokenKind.U8)
        var_ident = self._expect(TokenKind.IDENT)
        self._expect(TokenKind.ASSIGN)
        val = self._root_parse_expr()
        self._expect(TokenKind.SEMICOLON)
        return VarDefAST(var_ident.content, val)

    def _root_parse_var_declare(self) -> VarDefAST:
        """
        var_declare: U8 IDENT SEMICOLON;
        :return: variable declaration AST, though it reuses VarDefAST.
        """
        self._expect(TokenKind.U8)
        var_ident = self._expect(TokenKind.IDENT)
        self._expect(TokenKind.SEMICOLON)
        return VarDefAST(var_ident.content, VoidAST())

    def _root_parse_var_assign(self) -> VarAssignAST:
        """
        var_assign: IDENT ASSIGN expr SEMICOLON;
        :return: variable assignment AST.
        """
        ident = self._expect(TokenKind.IDENT)
        self._expect(TokenKind.ASSIGN)
        expr = self._root_parse_expr()
        self._expect(TokenKind.SEMICOLON)
        return VarAssignAST(ident.content, expr)

    def _root_parse_print(self) -> PrintAST:
        """
        print: PRINT expr SEMICOLON;
        :return: AST for printing.
        """
        self._expect(TokenKind.PRINT)
        expr = self._root_parse_expr()
        self._expect(TokenKind.SEMICOLON)
        return PrintAST(expr)

    def _root_parse_sprint(self) -> SprintAST:
        """
        sprint: SPRINT expr SEMICOLON;
        :return: AST for printing strings.
        """
        self._expect(TokenKind.SPRINT)
        expr = self._root_parse_expr()
        self._expect(TokenKind.SEMICOLON)
        return SprintAST(expr)

    def _root_parse_var_increment(self) -> VarIncrementAST:
        """
        var_increment: IDENT INCREMENT SEMICOLON;
        :return: variable increment AST.
        """
        ident = self._expect(TokenKind.IDENT)
        self._expect(TokenKind.INCREMENT)
        self._expect(TokenKind.SEMICOLON)
        return VarIncrementAST(ident.content)

    def _root_parse_test_5g(self) -> Test5GAST:
        """
        test_5g: TEST_5G SEMICOLON;
        :return: AST for testing 5G.
        """
        self._expect(TokenKind.TEST_5G)
        self._expect(TokenKind.SEMICOLON)
        return Test5GAST()

    def _root_parse_u8_set(self) -> U8SetAST:
        """
        u8_set: expr LS expr RS ASSIGN expr SEMICOLON;
        :return: AST for setting u8.
        """
        list_expr, subscript_expr = self._parse_u8_common_parts()
        self._expect(TokenKind.ASSIGN)
        value_expr = self._root_parse_expr()
        self._expect(TokenKind.SEMICOLON)
        return U8SetAST(list_expr, subscript_expr, value_expr)

    def _root_parse_expr(self, skip_u8=False) -> AST:
        """
        expr
          : empty_u8_expr
          | or_u8_expr
          | var_expr
          | u8_get_expr
          ;
        :param skip_u8: whether it should skip u8.
        :return: AST for current expression.
        """
        expr_parsers = [self._parse_empty_u8_expr, self._parse_or_u8_expr, self._parse_u8_get_expr, self._parse_var_expr]
        for parser in expr_parsers:
            if skip_u8 and parser == self._parse_u8_get_expr:
                continue
            saved_pos = self._pos
            try:
                return parser()
            except BadStatementException:
                self._pos = saved_pos
        raise BadStatementException('cannot parse expressions')

    def _parse_empty_u8_expr(self) -> EmptyU8InitAST:
        """
        empty_u8_expr: LS NUMBER RS;
        :return: empty initializer for u8.
        """
        self._expect(TokenKind.LS)
        length = self._expect(TokenKind.NUMBER)
        self._expect(TokenKind.RS)
        return EmptyU8InitAST(int(length.content))

    def _parse_or_u8_expr(self) -> OrU8InitAST:
        """
        or_u8_expr
            : NUMBER
            | NUMBER OR or_u8_expr
            ;
        :return: or initializer for u8.
        """
        first = self._expect(TokenKind.NUMBER)

        try:
            self._expect(TokenKind.OR)
        except BadStatementException:
            return OrU8InitAST(int(first.content))

        return OrU8InitAST(int(first.content), self._parse_or_u8_expr())

    def _parse_var_expr(self) -> VarExprAST:
        """
        var_expr: IDENT;
        :return: variable expression.
        """
        ident = self._expect(TokenKind.IDENT)
        return VarExprAST(ident.content)

    def _parse_u8_get_expr(self) -> U8GetAST:
        """
        u8_get_expr: expr LS expr RS
        :return: AST for getting u8.
        """
        list_expr, subscript_expr = self._parse_u8_common_parts()
        return U8GetAST(list_expr, subscript_expr)

    def _parse_u8_common_parts(self) -> Tuple[AST, AST]:
        list_expr = self._root_parse_expr(skip_u8=True)
        self._expect(TokenKind.LS)
        subscript_expr = self._root_parse_expr()
        self._expect(TokenKind.RS)
        return list_expr, subscript_expr

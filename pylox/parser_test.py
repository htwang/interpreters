import unittest
from parser import Parser

from expr import BinaryExpr, GroupExpr, LiteralExpr, UnaryExpr
from lox_token import Token
from scanner import Scanner
from token_type import TokenType


class ParserTest(unittest.TestCase):
    def test_parse_literal_expr(self) -> None:
        expectation = [
            ("1", LiteralExpr(value=1)),
            ('"a"', LiteralExpr(value="a")),
            ("true", LiteralExpr(value=True)),
            ("false", LiteralExpr(value=False)),
            ("nil", LiteralExpr(value=None)),
        ]
        self._test_expected(expectation)

    def test_parse_unary_expr(self) -> None:
        expectation = [
            (
                "-1",
                UnaryExpr(
                    op=Token(ttype=TokenType.MINUS, lexeme="-"),
                    right=LiteralExpr(value=1),
                ),
            ),
            (
                '!"a"',
                UnaryExpr(
                    op=Token(ttype=TokenType.BANG, lexeme="!"),
                    right=LiteralExpr(value="a"),
                ),
            ),
            # test associativity
            (
                "!-1",
                UnaryExpr(
                    op=Token(ttype=TokenType.BANG, lexeme="!"),
                    right=UnaryExpr(
                        op=Token(ttype=TokenType.MINUS, lexeme="-"),
                        right=LiteralExpr(value=1),
                    ),
                ),
            ),
        ]
        self._test_expected(expectation)

    def test_parse_factor_expr(self) -> None:
        expectation = [
            (
                "1*2",
                BinaryExpr(
                    left=LiteralExpr(value=1),
                    op=Token(ttype=TokenType.STAR, lexeme="*"),
                    right=LiteralExpr(value=2),
                ),
            ),
            # test associativity
            (
                "1*2/3",
                BinaryExpr(
                    left=BinaryExpr(
                        left=LiteralExpr(value=1),
                        op=Token(ttype=TokenType.STAR, lexeme="*"),
                        right=LiteralExpr(value=2),
                    ),
                    op=Token(ttype=TokenType.SLASH, lexeme="/"),
                    right=LiteralExpr(value=3),
                ),
            ),
        ]
        self._test_expected(expectation)

    def test_parse_term_expr(self) -> None:
        expectation = [
            (
                "1+2",
                BinaryExpr(
                    left=LiteralExpr(value=1),
                    op=Token(ttype=TokenType.PLUS, lexeme="+"),
                    right=LiteralExpr(value=2),
                ),
            ),
            # test associativity
            (
                "1+2-3",
                BinaryExpr(
                    left=BinaryExpr(
                        left=LiteralExpr(value=1),
                        op=Token(ttype=TokenType.PLUS, lexeme="+"),
                        right=LiteralExpr(value=2),
                    ),
                    op=Token(ttype=TokenType.MINUS, lexeme="-"),
                    right=LiteralExpr(value=3),
                ),
            ),
        ]
        self._test_expected(expectation)

    def test_equility_expr(self) -> None:
        ops = [
            Token(ttype=TokenType.LESS, lexeme="<"),
            Token(ttype=TokenType.LESS_EQUAL, lexeme="<="),
            Token(ttype=TokenType.GREATER, lexeme=">"),
            Token(ttype=TokenType.GREATER_EQUAL, lexeme=">="),
        ]

        expectation = [
            (
                f"1{op.lexeme}2",
                BinaryExpr(
                    left=LiteralExpr(value=1), op=op, right=LiteralExpr(value=2)
                ),
            )
            for op in ops
        ]

        # test associativity
        expectation.append(
            (
                "1<2<=3",
                BinaryExpr(
                    left=BinaryExpr(
                        left=LiteralExpr(value=1),
                        op=Token(ttype=TokenType.LESS, lexeme="<"),
                        right=LiteralExpr(value=2),
                    ),
                    op=Token(ttype=TokenType.LESS_EQUAL, lexeme="<="),
                    right=LiteralExpr(value=3),
                ),
            ),
        )
        self._test_expected(expectation)

    def test_equality_expr(self) -> None:
        ops = [
            Token(ttype=TokenType.BANG_EQUAL, lexeme="!="),
            Token(ttype=TokenType.EQUAL_EQUAL, lexeme="=="),
        ]

        expectation = [
            (
                f"1{op.lexeme}2",
                BinaryExpr(
                    left=LiteralExpr(value=1), op=op, right=LiteralExpr(value=2)
                ),
            )
            for op in ops
        ]
        # test associativity
        expectation.append(
            (
                "1!=2==3",
                BinaryExpr(
                    left=BinaryExpr(
                        left=LiteralExpr(value=1),
                        op=Token(ttype=TokenType.BANG_EQUAL, lexeme="!="),
                        right=LiteralExpr(value=2),
                    ),
                    op=Token(ttype=TokenType.EQUAL_EQUAL, lexeme="=="),
                    right=LiteralExpr(value=3),
                ),
            ),
        )

        self._test_expected(expectation)

    def test_group_expr(self) -> None:
        expectation = [
            ("(1)", GroupExpr(expr=LiteralExpr(value=1))),
        ]
        self._test_expected(expectation)

    def test_expr_precedence(self) -> None:
        expectation = [
            (
                "2==1<1+2*-3",
                BinaryExpr(
                    left=LiteralExpr(value=2),
                    op=Token(ttype=TokenType.EQUAL_EQUAL, lexeme="=="),
                    right=BinaryExpr(
                        left=LiteralExpr(value=1),
                        op=Token(ttype=TokenType.LESS, lexeme="<"),
                        right=BinaryExpr(
                            left=LiteralExpr(value=1),
                            op=Token(ttype=TokenType.PLUS, lexeme="+"),
                            right=BinaryExpr(
                                left=LiteralExpr(value=2),
                                op=Token(ttype=TokenType.STAR, lexeme="*"),
                                right=UnaryExpr(
                                    op=Token(ttype=TokenType.MINUS, lexeme="-"),
                                    right=LiteralExpr(value=3),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        ]
        self._test_expected(expectation)

    def test_group_override_precedence(self) -> None:
        expectation = [
            (
                "(1+2)*3",
                BinaryExpr(
                    left=GroupExpr(
                        expr=BinaryExpr(
                            left=LiteralExpr(value=1),
                            op=Token(ttype=TokenType.PLUS, lexeme="+"),
                            right=LiteralExpr(value=2),
                        )
                    ),
                    op=Token(ttype=TokenType.STAR, lexeme="*"),
                    right=LiteralExpr(value=3),
                ),
            )
        ]
        self._test_expected(expectation)

    def _test_expected(self, expectation) -> None:
        for text, expected in expectation:
            with self.subTest(msg=f"test parsing {text}"):
                expr = Parser(Scanner(text).scan_tokens())._expression()
                self.assertEqual(expr, expected)

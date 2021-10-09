import unittest
from parser import Parser

from expr import LiteralExpr, UnaryExpr
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

    def _test_expected(self, expectation) -> None:
        for text, expected in expectation:
            with self.subTest(msg=f"test parsing {text}"):
                expr = Parser(Scanner(text).scan_tokens()).parse()
                self.assertEqual(expr, expected)

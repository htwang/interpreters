import unittest

from expr import BinaryExpr, GroupExpr, LiteralExpr, UnaryExpr
from lox_token import Token
from pretty_printer import pprint_expr
from token_type import TokenType


class ExprText(unittest.TestCase):
    def test_expr(self) -> None:
        expr = BinaryExpr(
            left=UnaryExpr(
                Token(ttype=TokenType.MINUS, lexeme="-"), LiteralExpr(value=123)
            ),
            op=Token(ttype=TokenType.STAR, lexeme="*"),
            right=GroupExpr(expr=LiteralExpr(value=45.67)),
        )

        self.assertEqual(pprint_expr(expr), "(* (- 123) (group 45.67))")

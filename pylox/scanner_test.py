import unittest

from lox_token import Token
from scanner import Scanner
from token_type import TokenType


class ScannerTest(unittest.TestCase):
    def test_single_char_token(self) -> None:
        scanner = Scanner("(){},-+;*")
        tokens = scanner.scan_tokens()
        self.assertListEqual(
            tokens,
            [
                Token(ttype=TokenType.LEFT_PAREN, lexeme="("),
                Token(ttype=TokenType.RIGHT_PAREN, lexeme=")"),
                Token(ttype=TokenType.LEFT_BRACE, lexeme="{"),
                Token(ttype=TokenType.RIGHT_BRACE, lexeme="}"),
                Token(ttype=TokenType.COMMA, lexeme=","),
                Token(ttype=TokenType.MINUS, lexeme="-"),
                Token(ttype=TokenType.PLUS, lexeme="+"),
                Token(ttype=TokenType.SEMICOLON, lexeme=";"),
                Token(ttype=TokenType.STAR, lexeme="*"),
                Token(ttype=TokenType.EOF, lexeme=""),
            ],
        )

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
                Token(ttype=TokenType.LEFT_PAREN, lexeme="(", literal=None, line=0),
                Token(ttype=TokenType.RIGHT_PAREN, lexeme=")", literal=None, line=0),
                Token(ttype=TokenType.LEFT_BRACE, lexeme="{", literal=None, line=0),
                Token(ttype=TokenType.RIGHT_BRACE, lexeme="}", literal=None, line=0),
                Token(ttype=TokenType.COMMA, lexeme=",", literal=None, line=0),
                Token(ttype=TokenType.MINUS, lexeme="-", literal=None, line=0),
                Token(ttype=TokenType.PLUS, lexeme="+", literal=None, line=0),
                Token(ttype=TokenType.SEMICOLON, lexeme=";", literal=None, line=0),
                Token(ttype=TokenType.STAR, lexeme="*", literal=None, line=0),
                Token(ttype=TokenType.EOF, lexeme="", literal=None, line=0),
            ],
        )

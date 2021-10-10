from typing import Any, List, Optional

from error import error
from lox_token import Token
from token_type import TokenType


class Scanner:

    KEY_WORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "fun": TokenType.FUN,
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source_code: str) -> None:
        self._source_code = source_code
        self._start = 0
        """ start of an lexeme """
        self._current = 0
        """ the current char under the cursor """
        self._line = 1
        """ the current line number of the source code """
        self._tokens: List[Token] = []

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            # we are at the beginning of the next lexeme
            self._start = self._current
            self._scan()

        self._add_eof_token()
        return self._tokens

    def _scan(self) -> None:
        c = self._advance()
        if c == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == ".":
            self._add_token(TokenType.DOT)
        elif c == "-":
            self._add_token(TokenType.MINUS)
        elif c == "+":
            self._add_token(TokenType.PLUS)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)
        elif c == "*":
            self._add_token(TokenType.STAR)
        elif c == "!":
            self._add_token(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            )
        elif c == "=":
            self._add_token(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            )
        elif c == ">":
            self._add_token(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            )
        elif c == "<":
            self._add_token(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            )
        elif c == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c == '"':
            self._string()
        elif c.isdigit():
            self._number()
        elif self._isalpha_or_underscore(c):
            self._identifier()
        elif c == "\n":
            self._line += 1
        elif c in [" ", "\r", "\t"]:
            return
        else:
            error(self._line, f"Unexpected charactor {c}.")

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source_code)

    def _advance(self) -> str:
        c = self._source_code[self._current]
        self._current += 1
        return c

    def _peek(self) -> Optional[str]:
        if self._is_at_end():
            return None
        return self._source_code[self._current]

    def _peek_next(self) -> Optional[str]:
        if self._current + 1 >= len(self._source_code):
            return None
        return self._source_code[self._current + 1]

    def _match(self, expected: str) -> bool:
        c = self._peek()
        if c is None or c != expected:
            return False
        self._advance()
        return True

    @staticmethod
    def _isalpha_or_underscore(c: str) -> bool:
        return c == "_" or c.isalpha()

    @staticmethod
    def _isalnum_or_underscore(c: str) -> bool:
        return c == "_" or c.isalnum()

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            c = self._advance()
            if c == "\n":
                self._line += 1

        if self._is_at_end():
            error(self._line, "Untermindated string.")

        # consume closing "
        self._advance()

        # strip off the quotes
        literal = self._source_code[self._start + 1 : self._current - 1]
        self._add_token_with_literal(TokenType.STRING, literal)

    def _number(self) -> None:
        c = self._peek()
        while c is not None and c.isdigit():
            self._advance()
            c = self._peek()

        c = self._peek()
        cx = self._peek_next()

        if c == "." and cx is not None and cx.isdigit():
            # consume the dot
            self._advance()

            c = self._peek()
            while c is not None and c.isdigit():
                self._advance()
                c = self._peek()

        literal = float(self._source_code[self._start : self._current])
        self._add_token_with_literal(TokenType.NUMBER, literal)

    def _identifier(self) -> None:
        c = self._peek()
        while c is not None and self._isalnum_or_underscore(c):
            self._advance()
            c = self._peek()

        lexeme = self._source_code[self._start : self._current]
        token_type = self.KEY_WORDS.get(lexeme) or TokenType.IDENTIFIER
        self._add_token(token_type)

    def _add_token(self, ttype: TokenType) -> None:
        self._add_token_with_literal(ttype, None)

    def _add_token_with_literal(self, ttype: TokenType, literal: Any) -> None:
        lexeme = self._source_code[self._start : self._current]
        self._tokens.append(
            Token(ttype=ttype, lexeme=lexeme, literal=literal, line=self._line)
        )

    def _add_eof_token(self) -> None:
        self._tokens.append(
            Token(ttype=TokenType.EOF, lexeme="", literal=None, line=self._line)
        )

from lox_token import Token
from token_type import TokenType
from typing import List, Any
from error import error

class Scanner:

    def __init__(self, source_code: str) -> None:
        self._source_code = source_code
        self._start = 0
        """ start of an lexeme """
        self._current = 0
        """ the current char under the cursor """
        self._line = 0
        """ the current line number of the source code """
        self._tokens = []

    def scan_tokens(self) -> List[Token]: 
        while not self._is_at_end():
            # we are at the beginning of the next lexeme
            self._start = self._current
            self._scan()

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
        else:
            error(self._line, f"Unexpected charactor {c}.")

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source_code)

    def _advance(self) -> str:
        c = self._source_code[self._current]
        self._current += 1
        return c

    def _add_token(self, ttype: TokenType) -> None:
        self._add_token_with_literal(ttype, None)

    def _add_token_with_literal(self, ttype: TokenType, literal: Any) -> None:
        lexeme = self._source_code[self._start:self._current]
        self._tokens.append(Token(ttype=ttype, lexeme=lexeme, literal=literal, line=self._line))

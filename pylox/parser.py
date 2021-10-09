from typing import List, Optional

from error import report
from expr import BinaryExpr, Expr, GroupExpr, LiteralExpr, UnaryExpr
from lox_token import Token
from token_type import TokenType


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Optional[Expr]:
        try:
            return self._expression()
        except ParserError:
            return None

    def _expression(self) -> Expr:
        return self._equility()

    def _equility(self) -> Expr:
        expr = self._comparision()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self._previous()
            right = self._comparision()
            expr = BinaryExpr(left=expr, op=op, right=right)

        return expr

    def _comparision(self) -> Expr:
        expr = self._term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            op = self._previous()
            right = self._term()
            expr = BinaryExpr(left=expr, op=op, right=right)

        return expr

    def _term(self) -> Expr:
        expr = self._factor()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous()
            right = self._factor()
            expr = BinaryExpr(left=expr, op=op, right=right)
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()

        while self._match(TokenType.STAR, TokenType.SLASH):
            op = self._previous()
            right = self._unary()
            expr = BinaryExpr(left=expr, op=op, right=right)

        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            op = self._previous()
            right = self._unary()
            return UnaryExpr(op=op, right=right)

        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return LiteralExpr(value=False)

        if self._match(TokenType.TRUE):
            return LiteralExpr(value=True)

        if self._match(TokenType.NIL):
            return LiteralExpr(value=None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(value=self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._expect(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupExpr(expr=expr)

        self._error("Expect Expression")

    def _error(self, msg: str) -> None:
        token = self._peek()
        if token.ttype == TokenType.EOF:
            report(token.line, " at end", msg)
        else:
            report(token.line, f" at '{token.lexeme}'", msg)
        raise ParserError()

    def _expect(self, token_type: TokenType, msg: str) -> None:
        if not self._match(token_type):
            self._error(msg)

    def _previous(self) -> Expr:
        return self._tokens[self._current - 1]

    def _advance(self) -> Expr:
        cur = self._tokens[self._current]
        self._current += 1
        return cur

    def _peek(self) -> Expr:
        return self._tokens[self._current]

    def _match(self, *token_types: TokenType) -> bool:
        if self._eof():
            return False

        cur = self._peek()
        for token_type in token_types:
            if cur.ttype == token_type:
                self._advance()
                return True
        return False

    def _eof(self) -> bool:
        return self._peek().ttype == TokenType.EOF
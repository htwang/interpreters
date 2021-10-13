from typing import List

from error import report
from expr import BinaryExpr, Expr, GroupExpr, LiteralExpr, UnaryExpr
from lox_token import Token
from stmt import ExprStmt, PrintStmt, Stmt
from token_type import TokenType


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self._tokens = tokens
        self._current = 0

    def parse(self) -> List[Stmt]:
        try:
            return self._program()
        except ParserError:
            return []

    def _program(self) -> List[Stmt]:
        stmts = []
        while not self._eof():
            stmts.append(self._statement())
        return stmts

    def _statement(self) -> Stmt:
        if self._match(TokenType.PRINT):
            return self._print_stmt()

        return self._expr_stmt()

    def _print_stmt(self) -> Stmt:
        expr = self._expression()
        self._expect(TokenType.SEMICOLON, "Expect ; at the end of print statment")
        return PrintStmt(expr=expr)

    def _expr_stmt(self) -> Stmt:
        expr = self._expression()
        self._expect(TokenType.SEMICOLON, "Expect ; at the end of expression")
        return ExprStmt(expr=expr)

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

        raise self._error("Expect Expression")

    def _error(self, msg: str) -> ParserError:
        token = self._peek()
        if token.ttype == TokenType.EOF:
            report(token.line, " at end", msg)
        else:
            report(token.line, f" at '{token.lexeme}'", msg)
        return ParserError()

    def _expect(self, token_type: TokenType, msg: str) -> None:
        if not self._match(token_type):
            raise self._error(msg)

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _advance(self) -> Token:
        cur = self._tokens[self._current]
        self._current += 1
        return cur

    def _peek(self) -> Token:
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

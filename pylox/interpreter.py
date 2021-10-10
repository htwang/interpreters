from dataclasses import dataclass
from typing import Any

from error import error
from expr import BinaryExpr, Expr, ExprVisitor, GroupExpr, LiteralExpr, UnaryExpr
from lox_token import Token
from token_type import TokenType


@dataclass
class LoxRuntimeError(Exception):
    token: Token
    msg: str


class _Interpreter(ExprVisitor):
    def visit_literal(self, expr: LiteralExpr) -> Any:
        return expr.value

    def visit_group(self, expr: GroupExpr) -> Any:
        return self._evaluate(expr.expr)

    def visit_unary(self, expr: UnaryExpr) -> Any:
        right = self._evaluate(expr.right)

        op_type = expr.op.ttype
        if op_type == TokenType.MINUS:
            self._require_type(expr.op, float)
            return -1 * right
        elif op_type == TokenType.BANG:
            return not self._truthy(right)
        else:
            raise self._runtime_error(expr.op, f"Unsupported op {op_type}")

    def visit_binary(self, expr: BinaryExpr) -> Any:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        op_type = expr.op.ttype
        if op_type == TokenType.STAR:
            self._require_type(expr.op, float, left, right)
            return left * right
        elif op_type == TokenType.SLASH:
            self._require_type(expr.op, float, left, right)
            return left / right
        elif op_type == TokenType.MINUS:
            self._require_type(expr.op, float, left, right)
            return left - right
        elif op_type == TokenType.PLUS:
            if isinstance(left, float):
                self._require_type(expr.op, float, right)
            if isinstance(left, str):
                self._require_type(expr.op, str, right)
            return left + right
        elif op_type == TokenType.GREATER:
            self._require_type(expr.op, float, left, right)
            return left > right
        elif op_type == TokenType.GREATER_EQUAL:
            self._require_type(expr.op, float, left, right)
            return left >= right
        elif op_type == TokenType.LESS:
            self._require_type(expr.op, float, left, right)
            return left < right
        elif op_type == TokenType.LESS_EQUAL:
            self._require_type(expr.op, float, left, right)
            return left <= right
        elif op_type == TokenType.EQUAL_EQUAL:
            return left == right
        elif op_type == TokenType.BANG_EQUAL:
            return left != right
        else:
            raise self._runtime_error(expr.op, f"Unsupported op {op_type}")

    def _evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def _truthy(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return value is not None

    def _require_type(self, token: Token, expected_type: type, *values: Any) -> None:
        for value in values:
            if not isinstance(value, expected_type):
                raise self._runtime_error(
                    token,
                    f"type mismatched for {token.lexeme}, expected type is {expected_type}",
                )

    @staticmethod
    def _runtime_error(token: Token, msg: str) -> LoxRuntimeError:
        return LoxRuntimeError(token=token, msg=msg)


def interpret(expr: Expr) -> Any:
    try:
        return expr.accept(_Interpreter())
    except LoxRuntimeError as e:
        error(e.token.line, e.msg)
        return None

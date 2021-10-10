from typing import Any

from expr import BinaryExpr, Expr, ExprVisitor, GroupExpr, LiteralExpr, UnaryExpr
from token_type import TokenType


class _Interpreter(ExprVisitor):
    def visit_literal(self, expr: LiteralExpr) -> Any:
        return expr.value

    def visit_group(self, expr: GroupExpr) -> Any:
        return self._evaluate(expr.expr)

    def visit_unary(self, expr: UnaryExpr) -> Any:
        right = self._evaluate(expr.right)

        op_type = expr.op.ttype
        if op_type == TokenType.MINUS:
            return -1 * right
        elif op_type == TokenType.BANG:
            return not self._truthy(right)
        else:
            raise RuntimeError(f"Unsupported op {op_type}")

    def visit_binary(self, expr: BinaryExpr) -> Any:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        op_type = expr.op.ttype
        if op_type == TokenType.STAR:
            return left * right
        elif op_type == TokenType.SLASH:
            return left / right
        elif op_type == TokenType.MINUS:
            return left - right
        elif op_type == TokenType.PLUS:
            return left + right
        elif op_type == TokenType.GREATER:
            return left > right
        elif op_type == TokenType.GREATER_EQUAL:
            return left >= right
        elif op_type == TokenType.LESS:
            return left < right
        elif op_type == TokenType.LESS_EQUAL:
            return left <= right
        elif op_type == TokenType.EQUAL_EQUAL:
            return left == right
        elif op_type == TokenType.BANG_EQUAL:
            return left != right
        else:
            raise RuntimeError(f"Unsupported op {op_type}")

    def _evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def _truthy(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return value is not None


def interpret(expr: Expr) -> Any:
    return expr.accept(_Interpreter())

import itertools
from typing import Any, List

from env import Environment
from error import LoxRuntimeError, error
from expr import (
    AssignExpr,
    BinaryExpr,
    Expr,
    ExprVisitor,
    GroupExpr,
    LiteralExpr,
    UnaryExpr,
    VarExpr,
)
from lox_token import Token
from stmt import (
    BlockStmt,
    ConditionalStmt,
    DeclStmt,
    ExprStmt,
    PrintStmt,
    Stmt,
    StmtVisitor,
    WhileStmt,
)
from token_type import TokenType


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self) -> None:
        self._env = Environment()

    def interpret(self, stmts: List[Stmt]) -> None:
        try:
            for stmt in stmts:
                self._execute(stmt)
        except LoxRuntimeError as e:
            error(e.token.line, e.msg)
            return None

    def visit_assign(self, expr: AssignExpr) -> Any:
        value = self._evaluate(expr.expr)
        self._env.assign(expr.token, value)
        return value

    def visit_literal(self, expr: LiteralExpr) -> Any:
        return expr.value

    def visit_group(self, expr: GroupExpr) -> Any:
        return self._evaluate(expr.expr)

    def visit_var(self, expr: VarExpr) -> Any:
        return self._env.get_value(expr.token)

    def visit_unary(self, expr: UnaryExpr) -> Any:
        right = self._evaluate(expr.right)

        op_type = expr.op.ttype
        if op_type == TokenType.MINUS:
            self._require_type(expr.op, float, right)
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

    def visit_print(self, stmt: PrintStmt) -> None:
        value = self._evaluate(stmt.expr)
        print(value)

    def visit_expr(self, stmt: ExprStmt) -> None:
        self._evaluate(stmt.expr)

    def visit_decl(self, stmt: DeclStmt) -> None:
        value = None if stmt.initializer is None else self._evaluate(stmt.initializer)
        self._env.define(stmt.token.lexeme, value)

    def visit_block(self, stmt: BlockStmt) -> None:
        self._execute_block(stmt, Environment(self._env))

    def visit_conditional(self, stmt: ConditionalStmt) -> None:
        if self._evaluate(stmt.cond):
            self._execute(stmt.truthy)
        else:
            if stmt.falsy is not None:
                self._execute(stmt.falsy)

    def visit_while(self, stmt: WhileStmt) -> None:
        while self._evaluate(stmt.cond):
            self._execute(stmt.stmt)

    def _evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def _execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def _execute_block(self, block: BlockStmt, env: Environment) -> None:
        previous_env = self._env
        try:
            self._env = env
            for stmt in block.stmts:
                self._execute(stmt)
        finally:
            self._env = previous_env

    def _truthy(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return value is not None

    def _require_type(
        self, token: Token, expected_type: type, value: Any, *more_values: Any
    ) -> None:
        for v in itertools.chain([value], more_values):
            if not isinstance(v, expected_type):
                raise self._runtime_error(
                    token,
                    f"type mismatched for {token.lexeme}, expected type is {expected_type}",
                )

    @staticmethod
    def _runtime_error(token: Token, msg: str) -> LoxRuntimeError:
        return LoxRuntimeError(token=token, msg=msg)

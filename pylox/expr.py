""" class that models expressions """
import abc
from dataclasses import dataclass

from typeing import Any

from lox_token import Token


class ExprVisitor(abc.ABC):
    @abc.abstractmethod
    def visit_literal(self, expr: "LiteralExpr") -> Any:
        pass

    @abc.abstractmethod
    def visit_unary(self, expr: "UnaryExpr") -> Any:
        pass

    @abc.abstractmethod
    def visit_binary(self, expr: "BinaryExpr") -> Any:
        pass

    @abc.abstractmethod
    def visit_group(self, expr: "GroupExpr") -> Any:
        pass


class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, expr_visitor: ExprVisitor) -> Any:
        pass


@dataclass
class LiteralExpr(Expr):
    value: Any

    def accept(self, expr_visitor: ExprVisitor) -> Any:
        return expr_visitor.visit_literal(self)


@dataclass
class UnaryExpr(Expr):
    op: Token
    right: Expr

    def accept(self, expr_visitor: ExprVisitor) -> Any:
        return expr_visitor.visit_unary(self)


@dataclass
class BinaryExpr(Expr):
    left: Expr
    op: Token
    right: Expr

    def accept(self, expr_visitor: ExprVisitor) -> Any:
        return expr_visitor.visit_binary(self)


@dataclass
class GroupExpr(Expr):
    expr: Expr

    def accept(self, expr_visitor: ExprVisitor) -> Any:
        return expr_visitor.visit_group(self)

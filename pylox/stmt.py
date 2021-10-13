""" class that models statements """
import abc
from dataclasses import dataclass

from expr import Expr


class StmtVisitor(abc.ABC):
    @abc.abstractmethod
    def visit_print(self, stmt: "PrintStmt") -> None:
        pass

    @abc.abstractmethod
    def visit_expr(self, stmt: "ExprStmt") -> None:
        pass


class Stmt(abc.ABC):
    @abc.abstractmethod
    def accept(self, stmt_visitor: StmtVisitor) -> None:
        pass


@dataclass
class PrintStmt(Stmt):
    expr: Expr

    def accept(self, stmt_visitor: StmtVisitor) -> None:
        stmt_visitor.visit_print(self)


@dataclass
class ExprStmt(Stmt):
    expr: Expr

    def accept(self, stmt_visitor: StmtVisitor) -> None:
        stmt_visitor.visit_expr(self)

""" class that models statements """
import abc
from dataclasses import dataclass
from typing import Optional

from expr import Expr
from lox_token import Token


class StmtVisitor(abc.ABC):
    @abc.abstractmethod
    def visit_print(self, stmt: "PrintStmt") -> None:
        pass

    @abc.abstractmethod
    def visit_expr(self, stmt: "ExprStmt") -> None:
        pass

    @abc.abstractmethod
    def visit_decl(self, stmt: "DeclStmt") -> None:
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


@dataclass
class DeclStmt(Stmt):
    token: Token
    initializer: Optional[Expr] = None

    def accept(self, stmt_visitor: StmtVisitor) -> None:
        stmt_visitor.visit_decl(self)

""" class that models statements """
import abc
from dataclasses import dataclass
from typing import List, Optional

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

    @abc.abstractmethod
    def visit_block(self, stmt: "BlockStmt") -> None:
        pass

    @abc.abstractmethod
    def visit_conditional(self, stmt: "ConditionalStmt") -> None:
        pass

    @abc.abstractmethod
    def visit_while(self, stmt: "WhileStmt") -> None:
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


@dataclass
class BlockStmt(Stmt):
    stmts: List[Stmt]

    def accept(self, stmt_visitor: StmtVisitor) -> None:
        stmt_visitor.visit_block(self)


@dataclass
class ConditionalStmt(Stmt):
    cond: Expr
    truthy: Stmt
    falsy: Optional[Stmt] = None

    def accept(self, stmt_visitor: StmtVisitor) -> None:
        stmt_visitor.visit_conditional(self)


@dataclass
class WhileStmt(Stmt):
    cond: Expr
    stmt: Stmt

    def accept(self, stmt_visitor: StmtVisitor) -> None:
        stmt_visitor.visit_while(self)

from expr import BinaryExpr, Expr, ExprVisitor, GroupExpr, LiteralExpr, UnaryExpr


class _PPrinter(ExprVisitor):
    def visit_literal(self, expr: LiteralExpr) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visit_unary(self, expr: UnaryExpr) -> str:
        return self._parenthesize(expr.op.lexeme, expr.right)

    def visit_binary(self, expr: BinaryExpr) -> str:
        return self._parenthesize(expr.op.lexeme, expr.left, expr.right)

    def visit_group(self, expr: GroupExpr) -> str:
        return self._parenthesize("group", expr.expr)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        result = f"({name}"
        for expr in exprs:
            result += f" {expr.accept(self)}"
        result += ")"
        return result


_pprinter = _PPrinter()


def pprint_expr(expr: Expr) -> str:
    return expr.accept(_pprinter)

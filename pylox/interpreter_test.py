import unittest
from parser import Parser
from typing import Any, cast

from expr import Expr
from interpreter import interpret
from scanner import Scanner


class InterpreterTest(unittest.TestCase):
    def test_interpret(self) -> None:
        self.assertEqual(self._evaluate("!true"), False)
        self.assertEqual(self._evaluate("!false"), True)
        self.assertEqual(self._evaluate("-1"), -1.0)
        self.assertEqual(self._evaluate("1<2"), True)
        self.assertEqual(self._evaluate("1<=1"), True)
        self.assertEqual(self._evaluate("1>1"), False)
        self.assertEqual(self._evaluate("1>=1"), True)
        self.assertEqual(self._evaluate("1==1"), True)
        self.assertEqual(self._evaluate("1!=1"), False)
        self.assertEqual(self._evaluate("1+2"), 3.0)
        self.assertEqual(self._evaluate("1-2"), -1.0)
        self.assertEqual(self._evaluate("1*2"), 2.0)
        self.assertEqual(self._evaluate("1/2"), 0.5)
        self.assertEqual(self._evaluate('"a"+"b"'), "ab")
        self.assertEqual(self._evaluate('(1+2)*3'), 9.0)

    def _evaluate(self, source: str) -> Any:
        expr = Parser(Scanner(source).scan_tokens()).parse()
        self.assertIsNotNone(expr)
        return interpret(cast(Expr, expr))

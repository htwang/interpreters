import unittest
from parser import Parser
from typing import Any, cast

from expr import Expr
from interpreter import Interpreter, LoxRuntimeError
from scanner import Scanner


class InterpreterTest(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

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
        self.assertEqual(self._evaluate("(1+2)*3"), 9.0)

    def test_interpret_malformed(self) -> None:
        self.assertIsNone(self._evaluate('1-"a"'))
        self.assertIsNone(self._evaluate('1+"a"'))
        self.assertIsNone(self._evaluate('1/"a"'))
        self.assertIsNone(self._evaluate('1*"a"'))
        self.assertIsNone(self._evaluate('1>"a"'))
        self.assertIsNone(self._evaluate('1>="a"'))
        self.assertIsNone(self._evaluate('1<"a"'))
        self.assertIsNone(self._evaluate('1<="a"'))
        self.assertIsNone(self._evaluate('-"a"'))
        self.assertIsNone(self._evaluate('"a"-1'))
        self.assertIsNone(self._evaluate('"a"+1'))
        self.assertIsNone(self._evaluate('"a"/1'))
        self.assertIsNone(self._evaluate('"a"*1'))
        self.assertIsNone(self._evaluate('"a">1'))
        self.assertIsNone(self._evaluate('"a">=1'))
        self.assertIsNone(self._evaluate('"a"<1'))
        self.assertIsNone(self._evaluate('"a"<=1'))

    def _evaluate(self, source: str) -> Any:
        try:
            expr = Parser(Scanner(source).scan_tokens())._expression()
            self.assertIsNotNone(expr)
            return self.interpreter._evaluate(cast(Expr, expr))
        except LoxRuntimeError:
            return None

from typing import Any, Dict

from error import LoxRuntimeError
from lox_token import Token


class Environment:
    def __init__(self) -> None:
        self._map: Dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        self._map[name] = value

    def assign(self, token: Token, value: Any) -> None:
        name = token.lexeme
        if name not in self._map:
            raise LoxRuntimeError(token=token, msg=f"Undefined variable {token.lexeme}")
        self._map[name] = value

    def get_value(self, token: Token) -> Any:
        name = token.lexeme
        if name in self._map:
            return self._map[name]
        raise LoxRuntimeError(token=token, msg=f"Undefined variable {token.lexeme}")

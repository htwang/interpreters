from typing import Any, Dict, Optional

from error import LoxRuntimeError
from lox_token import Token


class Environment:
    def __init__(self, enclosed: Optional["Environment"] = None) -> None:
        self._map: Dict[str, Any] = {}
        self._enclosed = enclosed

    def define(self, name: str, value: Any) -> None:
        self._map[name] = value

    def assign(self, token: Token, value: Any) -> None:
        name = token.lexeme
        if name in self._map:
            self._map[name] = value
            return

        if self._enclosed is not None:
            self._enclosed.assign(token, value)
        else:
            raise LoxRuntimeError(token=token, msg=f"Undefined variable {token.lexeme}")

    def get_value(self, token: Token) -> Any:
        name = token.lexeme
        if name in self._map:
            return self._map[name]

        if self._enclosed is not None:
            return self._enclosed.get_value(token)
        else:
            raise LoxRuntimeError(token=token, msg=f"Undefined variable {token.lexeme}")

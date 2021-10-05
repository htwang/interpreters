from dataclasses import dataclass
from typing import Any

from token_type import TokenType


@dataclass
class Token:
    ttype: TokenType
    lexeme: str
    literal: Any
    line: int

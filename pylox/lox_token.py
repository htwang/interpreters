from dataclasses import dataclass
from typing import Any, Optional

from token_type import TokenType


@dataclass
class Token:
    ttype: TokenType
    lexeme: str
    literal: Optional[Any] = None
    line: int = 1

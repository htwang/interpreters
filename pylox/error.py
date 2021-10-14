""" utilties for error reporting """
from dataclasses import dataclass

from lox_token import Token


@dataclass
class LoxRuntimeError(Exception):
    token: Token
    msg: str


def report(line: int, where: str, msg: str) -> None:
    print(f"[line {line}] Error{where}: {msg}")


def error(line: int, msg: str) -> None:
    report(line, "", msg)

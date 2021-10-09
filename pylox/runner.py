""" entry point of the python implementation of the lox language """

from parser import Parser

from pretty_printer import pprint_expr
from scanner import Scanner


def _run(source_code: str) -> None:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expr = parser.parse()
    print(pprint_expr(expr))


def run_from_file(file_name: str) -> None:
    with open(file_name) as f:
        _run(f.read())


def run_prompt() -> None:
    """run an interactive prompt"""
    while True:
        try:
            line = input(">> ")
            _run(line)
        except EOFError:
            print("")
            break

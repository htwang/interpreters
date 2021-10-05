""" entry point of the python implementation of the lox language """

from scanner import Scanner


def _run(source_code: str) -> None:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    for t in tokens:
        print(t)


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

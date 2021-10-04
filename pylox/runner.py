""" entry point of the python implementation of the lox language """


def _run(source_code: str) -> None:
    print (source_code)


def run_from_file(file_name: str) -> None:
    with open(file_name) as f:
        _run(f.read())

def run_prompt() -> None:
    """ run an interactive prompt """
    while True:
        try:
            line = input(">> ")
            _run(line)
        except EOFError:
            print("")
            break


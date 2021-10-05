import sys

from runner import run_from_file, run_prompt


def main() -> None:
    argc = len(sys.argv)

    if argc > 2:
        print("Usage: pylox [script]")
        exit(-1)
    elif argc == 2:
        run_from_file(sys.argv[1])
    else:
        run_prompt()


if __name__ == "__main__":
    main()

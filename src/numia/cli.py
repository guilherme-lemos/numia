import argparse

from numia import report


def _init(args: argparse.Namespace) -> None:
    print(args.path)


def _report(args: argparse.Namespace) -> None:
    report.main()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="numia")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a project or ledger")
    init_parser.add_argument("path")
    init_parser.set_defaults(func=_init)

    report_parser = subparsers.add_parser("report", help="Generate a report")
    report_parser.set_defaults(func=_report)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        print("🚀 Numia v26.09.0")
        return

    args.func(args)


if __name__ == "__main__":
    main()

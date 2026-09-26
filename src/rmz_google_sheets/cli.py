"""Command-line interface for Google Sheets."""

import argparse
import json
import math
import sys
from collections.abc import Sequence
from typing import Any

from rmz_google_sheets.client import append_values, build_service, get_values, update_values


def parse_values(raw: str) -> list[list[Any]]:
    try:
        values = json.load(sys.stdin) if raw == "-" else json.loads(raw)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"invalid JSON values: {exc}") from exc

    if (
        not isinstance(values, list)
        or not values
        or any(not isinstance(row, list) or not row for row in values)
    ):
        raise argparse.ArgumentTypeError("values must be a non-empty JSON array of non-empty rows")
    if any(
        not isinstance(cell, (str, int, float, bool))
        or isinstance(cell, float) and not math.isfinite(cell)
        for row in values
        for cell in row
    ):
        raise argparse.ArgumentTypeError("each cell must be a string, number, or boolean")
    return values


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rmz-sheets",
        description="Read and edit Google Sheets ranges.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_parser = subparsers.add_parser("get", help="read values from a range")
    get_parser.add_argument("spreadsheet_id")
    get_parser.add_argument("range")

    for command, help_text in (
        ("update", "replace values in a range"),
        ("append", "append rows to a table"),
    ):
        command_parser = subparsers.add_parser(command, help=help_text)
        command_parser.add_argument("spreadsheet_id")
        command_parser.add_argument("range")
        command_parser.add_argument(
            "--values",
            required=True,
            metavar="JSON",
            help="two-dimensional JSON array of values, or '-' to read JSON from stdin",
        )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command == "get":
        result = get_values(build_service(), args.spreadsheet_id, args.range)
    else:
        try:
            values = parse_values(args.values)
        except argparse.ArgumentTypeError as exc:
            parser.error(str(exc))
        service = build_service()
        operation = update_values if args.command == "update" else append_values
        result = operation(service, args.spreadsheet_id, args.range, values)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

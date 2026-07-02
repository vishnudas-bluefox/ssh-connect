from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from ssh_connect.store import CONFIG_FILE, Connection, add, delete, get, list_names, load_all


def _prompt(text: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{text}{suffix}: ").strip()
    return value or default


def _prompt_required(text: str, default: str = "") -> str:
    while True:
        value = _prompt(text, default)
        if value:
            return value
        print("Required.")


def _prompt_int(text: str, default: int) -> int:
    while True:
        raw = _prompt(text, str(default))
        try:
            return int(raw)
        except ValueError:
            print("Enter a number.")


def cmd_add(args: argparse.Namespace) -> int:
    cli_mode = bool(args.host)

    name = args.name or _prompt_required("Name (short alias, e.g. cp-sandbox)")
    connections = load_all()
    if name in connections and not args.force:
        print(f"'{name}' already exists. Use --force to overwrite.")
        return 1

    host = args.host or _prompt_required("Host (IP or hostname)")
    if args.user is not None:
        user = args.user
    elif cli_mode:
        user = "ubuntu"
    else:
        user = _prompt("User", "ubuntu")

    if args.pem is not None:
        pem_file = args.pem
    elif cli_mode:
        pem_file = ""
    else:
        pem_file = _prompt("PEM file path (leave empty if none)")

    if args.port is not None:
        port = args.port
    elif cli_mode:
        port = 22
    else:
        port = _prompt_int("Port", 22)

    extra = args.extra_args or []

    if pem_file:
        pem_path = Path(pem_file).expanduser().resolve()
        if not pem_path.is_file():
            print(f"PEM file not found: {pem_path}")
            return 1
        pem_file = str(pem_path)

    connection = Connection(
        name=name,
        host=host,
        user=user,
        pem_file=pem_file,
        port=port,
        extra_args=extra or None,
    )
    add(connection)
    print(f"Saved '{name}' -> {connection.user}@{connection.host}")
    print(f"Connect with: ssh-connect {name}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    if not delete(args.name):
        print(f"Connection '{args.name}' not found.")
        return 1
    print(f"Deleted '{args.name}'.")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    connections = load_all()
    if not connections:
        print("No connections saved.")
        print(f"Config: {CONFIG_FILE}")
        print("Add one with: ssh-connect add <name>")
        return 0

    width = max(len(name) for name in connections)
    for name, conn in connections.items():
        pem = conn.pem_file or "-"
        print(f"  {name:<{width}}  {conn.user}@{conn.host}:{conn.port}  {pem}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    conn = get(args.name)
    if not conn:
        print(f"Connection '{args.name}' not found.")
        return 1
    print(f"name:       {conn.name}")
    print(f"host:       {conn.host}")
    print(f"user:       {conn.user}")
    print(f"port:       {conn.port}")
    print(f"pem_file:   {conn.pem_file or '-'}")
    print(f"extra_args: {' '.join(conn.extra_args) if conn.extra_args else '-'}")
    print(f"command:    {' '.join(conn.ssh_command())}")
    return 0


def cmd_connect(args: argparse.Namespace) -> int:
    conn = get(args.name)
    if not conn:
        print(f"Connection '{args.name}' not found.")
        print("Run: ssh-connect list")
        return 1

    pem = conn.resolved_pem()
    if conn.pem_file and (not pem or not pem.is_file()):
        print(f"PEM file not found: {conn.pem_file}")
        return 1

    cmd = conn.ssh_command()
    if args.dry_run:
        print(" ".join(cmd))
        return 0

    os.execvp(cmd[0], cmd)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ssh-connect",
        description="Manage and connect to saved SSH profiles.",
    )
    parser.add_argument("--version", action="version", version="ssh-connect 0.1.1")

    sub = parser.add_subparsers(dest="command")

    add_parser = sub.add_parser("add", help="Create or update a connection")
    add_parser.add_argument("name", nargs="?", help="Short alias name")
    add_parser.add_argument("--host", help="Host IP or hostname")
    add_parser.add_argument("--user", default=None, help="SSH user (default: ubuntu)")
    add_parser.add_argument("--pem", help="Path to PEM/private key file")
    add_parser.add_argument("--port", type=int, default=None, help="SSH port (default: 22)")
    add_parser.add_argument("--extra-args", nargs="*", default=[], help="Extra ssh flags")
    add_parser.add_argument("--force", action="store_true", help="Overwrite existing name")
    add_parser.set_defaults(func=cmd_add)

    rm_parser = sub.add_parser("rm", aliases=["delete", "del"], help="Delete a connection")
    rm_parser.add_argument("name", help="Connection name to delete")
    rm_parser.set_defaults(func=cmd_delete)

    list_parser = sub.add_parser("list", aliases=["ls"], help="List saved connections")
    list_parser.set_defaults(func=cmd_list)

    show_parser = sub.add_parser("show", help="Show connection details")
    show_parser.add_argument("name", help="Connection name")
    show_parser.set_defaults(func=cmd_show)

    connect_parser = sub.add_parser("connect", help="Connect to a saved profile")
    connect_parser.add_argument("name", help="Connection name")
    connect_parser.add_argument("--dry-run", action="store_true", help="Print ssh command only")
    connect_parser.set_defaults(func=cmd_connect)

    return parser


SUBCOMMANDS = {"add", "rm", "delete", "del", "list", "ls", "show", "connect", "-h", "--help", "--version"}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()

    if not argv:
        parser.print_help()
        return 0

    if argv[0] not in SUBCOMMANDS:
        dry_run = "--dry-run" in argv
        name = next(arg for arg in argv if arg != "--dry-run")
        return cmd_connect(argparse.Namespace(name=name, dry_run=dry_run))

    args = parser.parse_args(argv)
    return args.func(args)

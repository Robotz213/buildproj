"""Modulo buildproj - Ferramenta de Build para Projetos C++.

Este módulo processa argumentos de linha de comando para selecionar o sistema
de build (MSVC ou MSYS2), o arquivo fonte C++ e outras opções, e então invoca
a tarefa de build apropriada.
"""

import argparse
import sys

from buildproj import build_task


def _main_entry() -> None:
    parser = argparse.ArgumentParser(
        description="Build Tool with MSVC or MSYS2",
    )
    parser.add_argument(
        "--build-method",
        "-b",
        choices=["msvc", "msys2"],
        help="Build method to use",
        default="msvc",
    )

    parser.add_argument(
        "--cpp-file",
        type=str,
        default="main.cpp",
        help="C++ source file",
    )

    parser.add_argument(
        "--python-executable",
        type=str,
        help="Path to Python executable",
        default=sys.executable,
    )

    parser.add_argument("--module-name", type=str, help="Name of the module")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        return

    args = parser.parse_args(sys.argv[1:])

    build_task(args)


if __name__ == "__main__":
    _main_entry()

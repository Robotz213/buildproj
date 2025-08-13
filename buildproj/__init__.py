"""Modulo buildproj - Ferramenta de Build para Projetos C++.

Este módulo processa argumentos de linha de comando para selecionar o sistema
de build (MSVC ou MSYS2), o arquivo fonte C++ e outras opções, e então invoca
a tarefa de build apropriada.
"""

import argparse
import shutil
import sys
from pathlib import Path

from tqdm import tqdm

from .build_tools import build_msvc, build_msys2

callable_builders = {"msvc": build_msvc, "msys2": build_msys2}


class BuildProjArgumentError(Exception):
    """Representa erro de argumento inválido para o buildproj."""

    def __init__(self, message: str) -> None:
        """Inicializa a exceção BuildProjArgumentError com uma mensagem personalizada.

        Args:
            message (str): Mensagem de erro detalhando o argumento inválido.

        """
        super().__init__(f"Erro de argumento: {message}")


def build_task(args: argparse.Namespace) -> None:
    """Executa a tarefa de build do projeto conforme os argumentos fornecidos.

    Args:
        args (argparse.Namespace): Namespace contendo os argumentos de linha
            de comando para configuração do build.

    Raises:
        BuildProjArgumentError: Caso nenhum sistema de
            build seja especificado (--msvc ou --msys2).

    """
    if Path("build").exists():
        shutil.rmtree("build")

    if not Path("CMakeLists.txt").exists():
        build_makelist(
            module_name=args.module_name,
            python_executable=args.python_executable,
            cpp_filename=args.cpp_file,
        )

    if args.build_method not in callable_builders:
        raise BuildProjArgumentError(message="Escolha --msvc ou --msys2")

    callable_builders[args.build_method](args.module_name)


def build_makelist(
    module_name: str,
    python_executable: str | None = None,
    cpp_filename: str | None = None,
) -> None:
    """Gera o arquivo CMakeLists.txt para um projeto pybind11 com parâmetros custom.

    Args:
        module_name (str): Nome do módulo pybind11 a ser criado.
        python_executable (str | None): Caminho absoluto para o executável do Python.
        cpp_filename (str | None): Nome do arquivo fonte C++ principal.

    Raises:
        OSError: Caso ocorra erro ao escrever o arquivo CMakeLists.txt.

    """
    py_path = python_executable or str(Path(sys.executable).resolve().as_posix())
    # Modelo do conteúdo do CMakeLists.txt
    cmake_content = f"""cmake_minimum_required(VERSION 3.15)
project({module_name} LANGUAGES CXX)

# Define padrão de compilação
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Faz o pybind11 usar o FindPython moderno
set(PYBIND11_FINDPYTHON ON)

# Define explicitamente o Python (substitua pelo caminho que quer usar por padrão)
set(Python3_EXECUTABLE "{py_path}" CACHE FILEPATH "Path to Python executable")

# Acha Python e pybind11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Cria o módulo
pybind11_add_module({module_name} {cpp_filename})
"""
    try:
        # Escreve o conteúdo no arquivo CMakeLists.txt
        with Path("CMakeLists.txt").open("w", encoding="utf-8") as f:
            f.write(cmake_content)
    except OSError as e:
        # Exibe mensagem de erro caso não seja possível escrever o arquivo
        tqdm.write(f"Erro ao criar CMakeLists.txt: {e}")
        raise

# README

## Introdução

O projeto **buildproj** é uma ferramenta de automação de build para projetos C++,
permitindo a escolha entre os sistemas MSVC e MSYS2. Seu objetivo é facilitar a
compilação de módulos C++ (especialmente com pybind11) de forma simples e
automatizada, integrando-se ao ambiente Python.

## Funcionalidades

- Geração automática do arquivo `CMakeLists.txt` para projetos pybind11.
- Suporte a múltiplos sistemas de build: MSVC e MSYS2.
- Seleção do arquivo fonte C++ e do executável Python via linha de comando.
- Interface de linha de comando amigável.

## Como Usar

Execute o comando abaixo para iniciar o processo de build:

```sh
python -m buildproj --build-method msvc --cpp-file main.cpp --module-name meu_modulo
```

## Requisitos

- Python 3.13 ou superior
- Dependências do sistema para MSVC ou MSYS2, conforme o método de build escolhido
- CMake 3.15 ou superior

## Licença

Este projeto está licenciado sob a [GNU General Public License v3.0](./LICENSE). Sinta-se à vontade para usar, modificar e distribuir este software.

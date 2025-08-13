/**
 * Execute o processo de build do projeto utilizando o MSVC.
 *
 * Args:
 * target (const std::string &): Nome do target a ser compilado.
 *
 * Returns:
 * void: Não retorna valor.
 *
 * Raises:
 * std::runtime_error: Caso ocorra erro durante o processo de build.
 */
#include <pybind11/pybind11.h>
#include <cstdlib>   // Para std::system
#include <iostream>  // Para std::cerr
#include <stdexcept> // Para std::runtime_error
#include <string>    // Para std::string
namespace py = pybind11;

/**
 * Execute o build do projeto com target customizado via MSVC.
 *
 * Args:
 * target (const std::string &): Nome do target a ser compilado.
 *
 * Returns:
 * void: Não retorna valor.
 *
 * Raises:
 * std::runtime_error: Caso ocorra erro durante o processo de build.
 */
void build_msvc(const std::string &target)
{
    // Comando para gerar os arquivos de build com CMake e MSVC
    const char *cmake_cmd =
        "cmake -G \"Visual Studio 17 2022\" -A x64 -S . -B build "
        "-DPYBIND11_FINDPYTHON=ON "
        "-DCMAKE_CXX_STANDARD=17";

    // Executa o comando de configuração do CMake
    int ret = std::system(cmake_cmd);
    if (ret != 0)
    {
        // Exibe mensagem de erro e lança exceção
        std::cerr << "Erro ao executar o comando CMake (configuração)." << std::endl;
        throw std::runtime_error("Falha na configuração do CMake.");
    }

    // Monta o comando para compilar o target especificado
    std::string build_cmd =
        "cmake --build build --config Release --target " + target;

    // Executa o comando de build
    ret = std::system(build_cmd.c_str());
    if (ret != 0)
    {
        // Exibe mensagem de erro e lança exceção
        std::cerr << "Erro ao compilar o projeto." << std::endl;
        throw std::runtime_error("Falha na compilação do projeto.");
    }
}

void build_msys2(const std::string &target)
{
    // Comando para gerar os arquivos de build com CMake e Ninja
    const char *cmake_cmd =
        "cmake -G Ninja -S . -B build "
        "-DPYBIND11_FINDPYTHON=ON "
        "-DCMAKE_CXX_STANDARD=17";

    // Executa o comando de configuração do CMake
    int ret = std::system(cmake_cmd);
    if (ret != 0)
    {
        // Exibe mensagem de erro e lança exceção
        std::cerr << "Erro ao executar o comando CMake (configuração)." << std::endl;
        throw std::runtime_error("Falha na configuração do CMake.");
    }

    // Monta o comando para compilar o target especificado
    std::string build_cmd =
        "cmake --build build --config Release --target " + target;

    // Executa o comando de build
    ret = std::system(build_cmd.c_str());
    if (ret != 0)
    {
        // Exibe mensagem de erro e lança exceção
        std::cerr << "Erro ao compilar o projeto." << std::endl;
        throw std::runtime_error("Falha na compilação do projeto.");
    }
}

PYBIND11_MODULE(build_tools, handle)
{
    // Define a documentação do módulo Python
    handle.doc() = "BuildTool para PyBind11 usando MSVC/MSYS";
    handle.def("build_msvc", &build_msvc, "Função de build de projeto PyBind11 com MSVC");
    handle.def("build_msys2", &build_msys2, "Função de build de projeto PyBind11 com MSYS2");
}

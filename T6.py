import subprocess
from lexer import Lexer, TokenTipo
from generator import Generator
from parser import Parser
import sys

def main():
    print("PTypescript -> Python Compiler")

    if len(sys.argv) != 2:
        sys.exit("Erro: Compilador precisa de um arquivo source como argumento.")
    
    source_file = sys.argv[1]

    with open(source_file, 'r') as inputFile:
        source = inputFile.read()

    # Inicializa o lexer, o generator e o parser
    lexer = Lexer(source)
    generator = Generator("out.py")  # Altere para gerar um arquivo Python
    parser = Parser(lexer, generator)

    # Parser é inicializado.
    parser.programa() 
    
    # Escreve a saída para o arquivo.
    generator.writeFile() 
    print("Compilacao Finalizada.")

if __name__ == "__main__":
    main()

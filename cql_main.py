import sys
from lexer import lexer
from parser import parse_sql
from semantic import execute_command
from database import database

def run_cql_file(filename):
    try:
        with open(filename, 'r') as file:
            line_number = 0  # Contador de linhas para imprimir no erro
            if not filename.endswith(".cql"):
                print(f"Erro: O ficheiro {filename} tem de ter a extensão .cql")
                sys.exit(1)
                
            for line in file:
                line_number += 1
                line = line.strip()  # Remove espaços extras ao redor da linha

                # Ignorar linhas vazias ou comentários de linha única
                if not line or line.startswith("#"):
                    continue

                try:
                    parsed = parse_sql(line)
                    execute_command(parsed)
                except Exception as e:
                    print(f"[ERRO] Linha {line_number}: '{line}'")
                    print(f"       {str(e)}")
    
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{filename}' não encontrado")

    except Exception as e:
        print(f"[ERRO] Falha ao processar o arquivo '{filename}': {str(e)}")

def run_interactive():
    # Função para rodar interativamente
    print("Escreva as expressões ou 'exit' para sair.")
    while True:
        try:
            expr = input(">> ").strip()

            if expr.lower() == 'sair':  # Permite sair do modo interativo
                break
                
            parsed = parse_sql(expr)
            result = execute_command(parsed)

            if result is None:
                print("<< Comando executado com sucesso!")
            else:
                print(f"<< {result}")

        except Exception as e:
            print(f"[ERRO] {e}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_cql_file(sys.argv[1])
    else:
        run_interactive()

import sys
from lexer import lexer
from parser import parse_sql
from semantic import execute_command
from database import database

def run_cql_file(filename):
    try:
        with open(filename, 'r') as file:
            # print(f"\nExecutando arquivo: {filename}")
            line_number = 0  # Contador de linhas para imprimir no erro

            for line in file:
                line_number += 1
                line = line.strip()  # Remove espaços extras ao redor da linha

                #! Aqui esta a verificacao dos comentarios na linha unica
                # Ignorar linhas vazias ou comentários de linha única
                if not line: #or line.startswith('--'):
                    continue

                try:
                    # Tenta parsear e executar o comando da linha
                    parsed = parse_sql(line)
                    execute_command(parsed)
                except Exception as e:
                    print(f"[ERRO] Linha {line_number}: '{line}'")
                    print(f"       {str(e)}")
    
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{filename}' não encontrado")

    except Exception as e:
        print(f"[ERRO] Falha ao processar o arquivo '{filename}': {str(e)}")
    
    # (Opcional) Imprimir o estado final do banco de dados, caso deseje
    # print("\nEstado final da base de dados:")
    # print(database)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cql_interpreter.py arquivo.fca")
    else:
        run_cql_file(sys.argv[1])

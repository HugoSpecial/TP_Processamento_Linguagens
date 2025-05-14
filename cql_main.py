import sys
from lexer import lexer
from parser import parse_sql
from semantic import execute_command
from database import database
import os

def run_cql_file(filename):
    # Variáveis de controlo
    inside_block = False
    inside_procedure = False
    procedure_content = ""  # Para armazenar o conteúdo da procedure
    captured_content = ""  # Vai armazenar tudo em uma única linha
    
    try:
        with open(filename, 'r') as file:
            line_number = 0
            if not filename.endswith(".cql"):
                print(f"Erro: O ficheiro {filename} tem de ter a extensão .cql")
                sys.exit(1)

            for line in file:
                line_number += 1
                line = line.strip()

                if not line:
                    continue

                try:

                    # Para capturar o conteúdo entre {- e -}
                    if line.startswith("{-"):
                        inside_block = True
                        captured_content = line[2:]

                    elif line.endswith("-}") and inside_block:
                        inside_block = False
                        captured_content += " " + line[:-2]
                        
                        final_content = " ".join(captured_content.split())

                        parsed = parse_sql("{-" + final_content + "-}")
                        result = execute_command(parsed)

                        captured_content = ""

                    elif line.upper().startswith("PROCEDURE"):
                        # Inicia a captura do PROCEDURE
                        if(line.upper().endswith("END")):
                            parsed = parse_sql(line)
                            result = execute_command(parsed)
                        else:
                            inside_procedure = True
                            procedure_content = line

                    elif line.upper().startswith("END") and inside_procedure:
                        inside_procedure = False
                        procedure_content += " " + line.strip()
                        
                        single_line_procedure = " ".join(procedure_content.split())                        

                        parsed = parse_sql(single_line_procedure)
                        result = execute_command(parsed)

                        procedure_content = ""

                    elif inside_procedure:

                        procedure_content += " " + line.strip()

                    elif inside_block:
                        captured_content += " " + line
                    else:
                        parsed = parse_sql(line)
                        result = execute_command(parsed)

                except Exception as e:
                    print(f"[ERRO] Linha {line_number}: '{line}'")
                    print(f"       {str(e)}")

    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{filename}' não encontrado")
    except Exception as e:
        print(f"[ERRO] Falha ao processar o arquivo '{filename}': {str(e)}")

def run_interactive():
    print("Escreva as expressões ou 'sair' para sair.")
    while True:
        try:
            expr = input(">> ").strip()

            if expr.upper().startswith("IMPORT TABLE"):
                # Procura por FROM "<ficheiro>"
                import re
                match = re.search(r'FROM\s+"([^"]+)"', expr, re.IGNORECASE)
                if match:
                    filename = match.group(1)
                    # Se for apenas o nome (sem caminho), prefixa com ./data/
                    if not os.path.isabs(filename) and not os.path.dirname(filename):
                        data_path = os.path.join("data", filename)
                        expr = expr.replace(f'"{filename}"', f'"{data_path}"')

            if expr.lower() == 'sair':
                break
            else:
                parsed = parse_sql(expr)
                result = execute_command(parsed)
                print(f"<< AST: {parsed}")

        except Exception as e:
            print(f"[ERRO] {e}")

def generate_ast(filename):

    # Variáveis de controlo
    inside_block = False
    inside_procedure = False
    procedure_content = ""  # Para armazenar o conteúdo da procedure
    captured_content = ""  # Vai armazenar tudo em uma única linha

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            try:

                if line.startswith("{-"):
                    inside_block = True
                    captured_content = line[2:]

                elif line.endswith("-}") and inside_block:
                    inside_block = False
                    captured_content += " " + line[:-2]
                    
                    final_content = " ".join(captured_content.split())

                    parsed = parse_sql("{-" + final_content + "-}")
                    print(f"<< AST: {parsed}")

                    captured_content = ""

                elif line.upper().startswith("PROCEDURE"):
                    # Inicia a captura do PROCEDURE
                    if(line.upper().endswith("END")):
                        parsed = parse_sql(line, ast=True)
                        print(f"<< AST: {parsed}")
                    else:
                        inside_procedure = True
                        procedure_content = line

                elif line.upper().startswith("END") and inside_procedure:
                    inside_procedure = False
                    procedure_content += " " + line.strip()
                    
                    single_line_procedure = " ".join(procedure_content.split())                        

                    parsed = parse_sql(single_line_procedure)
                    print(f"<< AST: {parsed}")

                    procedure_content = ""

                elif inside_procedure:

                    procedure_content += " " + line.strip()

                elif inside_block:
                    captured_content += " " + line
                else:
                    parsed = parse_sql(line)
                    print(f"<< AST: {parsed}")

            except Exception as e:
                print(f"Erro ao processar linha: {line}")
                print(f"Detalhes: {e}")    

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_cql_file(sys.argv[1])
    elif len(sys.argv) > 2 and sys.argv[2].upper() == "AST":
        generate_ast(sys.argv[1])
    else:
        run_interactive()

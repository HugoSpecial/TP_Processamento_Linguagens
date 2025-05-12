import sys
from lexer import lexer
from parser import parse_sql
from semantic import execute_command
from database import database

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
                    # if line.upper().startswith("AST:"):
                    #     expr = line[4:].strip()
                    #     parsed = parse_sql(expr, ast=True)
                    #     print(f"<< AST: {parsed}")
                    
                    # Para capturar o conteúdo entre {- e -}
                    if line.startswith("{-"):
                        inside_block = True
                        captured_content = line[2:]  # Remove "{-" do início

                    elif line.endswith("-}") and inside_block:
                        inside_block = False
                        captured_content += " " + line[:-2]  # Remove "-}" do final
                        
                        final_content = " ".join(captured_content.split())
                        parsed = parse_sql("{-" + final_content + "-}")
                        result = execute_command(parsed)
                        captured_content = ""  # Reseta para o próximo bloco

                    elif line.upper().startswith("PROCEDURE"):
                        # Inicia a captura do PROCEDURE
                        if(line.upper().endswith("END")):
                            parsed = parse_sql(line)
                            result = execute_command(parsed)
                        else:
                            inside_procedure = True
                            procedure_content = line

                    elif line.upper().startswith("END") and inside_procedure:
                        # Finaliza o PROCEDURE
                        inside_procedure = False
                        # Adiciona a linha final (END PROCEDURE) e remove quebras de linha
                        procedure_content += " " + line.strip()
                        
                        # Remove espaços extras e quebras de linha
                        single_line_procedure = " ".join(procedure_content.split())                        

                        parsed = parse_sql(single_line_procedure)
                        result = execute_command(parsed)

                        # Limpa o conteúdo da procedure para o próximo
                        procedure_content = ""

                    elif inside_procedure:
                        # Durante a captura do PROCEDURE, adiciona o conteúdo à linha atual
                        procedure_content += " " + line.strip()

                    elif inside_block:
                        captured_content += " " + line  # Adiciona como continuação de outros blocos
                    # Fim do bloco
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

            if expr.lower() == 'sair':
                break
            else:
                parsed = parse_sql(expr)
                parsed2 = parse_sql(expr, ast=True)
                result = execute_command(parsed)
                print(f"<< AST: {parsed2}")

        except Exception as e:
            print(f"[ERRO] {e}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_cql_file(sys.argv[1])
    else:
        run_interactive()

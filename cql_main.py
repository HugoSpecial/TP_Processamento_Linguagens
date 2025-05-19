import sys
import os
from lexer import lexer
from parser import parser, parse_sql
from semantic import interpret
from database import database
from pprint import PrettyPrinter
import re

pp = PrettyPrinter(sort_dicts=False)

def preprocess_import_command(expr):
    if not expr.upper().startswith("IMPORT TABLE"):
        return expr
        
    match = re.search(r'FROM\s+("[^"]+"|\S+)', expr, re.IGNORECASE)
    if not match:
        return expr
        
    filename = match.group(1).strip('"')
    
    if not os.path.exists(filename):
        data_path = os.path.join("data", filename)
        if os.path.exists(data_path):
            expr = expr.replace(match.group(1), f'"{data_path}"')
        else:
            print(f"[AVISO] Ficheiro '{filename}' não encontrado na pasta atual nem em 'data/'")
    
    return expr

def read_file(filename):
    with open(filename, "r", encoding='utf-8') as file:
        return file.read()

def run_interactive_mode():
    print("Modo interativo. Use 'SAIR' para sair.")
    while True:
        try:
            line = input(">> ").strip()
            if not line:
                continue
            if line.upper() == "SAIR":
                break
                
            line = preprocess_import_command(line)
            
            # Mostra AST e executa
            parsed = parse_sql(line)
            print("Arvore de Sintaxe Abstrata:")
            pp.pprint(parsed)
            
            result = interpret(line)
            if result:
                if isinstance(result, list):
                    for res in result:
                        print(f"<< {res}")
                else:
                    print(f"<< {result}")
        except KeyboardInterrupt:
            print("\nUse 'sair' para sair.")
            continue
        except Exception as e:
            print(f"[ERRO] {str(e)}", file=sys.stderr)


def run_file_mode(filename, show_ast=True, execute_commands=True):
    if not os.path.exists(filename):
        print(f"Error: O ficheiro {filename} nao existe.", file=sys.stderr)
        sys.exit(1)
    if not filename.endswith(".cql"):
        print(f"Error: O ficheiro {filename} tem de ter extensao .cql", file=sys.stderr)
        sys.exit(1)

    # Le todo o ficheiro de entrada
    content = read_file(filename)

    try:
        parsed = parse_sql(content)
        
        if show_ast:
            base_name = os.path.splitext(os.path.basename(filename))[0]
            print("\nArvore de Sintaxe Abstrata:")
            print("\n")
            pp.pprint(parsed)
            print("\n")
        
        if execute_commands:
            results = interpret(content)
            if results:
                if isinstance(results, list):
                    for i, res in enumerate(results, 1):
                        print("\n")
                        print(res)

    except Exception as e:
        print(e, file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_interactive_mode()
    elif len(sys.argv) == 2:
        run_file_mode(sys.argv[1], show_ast=False, execute_commands=True)
    elif len(sys.argv) == 3 and sys.argv[2].lower() == "ast":
        run_file_mode(sys.argv[1], show_ast=True, execute_commands=False)
    else:
        print("Uso:")
        print("  python cql_main.py                     - Modo interativo")
        print("  python cql_main.py arquivo.cql         - Executa comandos do arquivo")
        print("  python cql_main.py arquivo.cql ast     - Mostra apenas a AST do arquivo")
        sys.exit(1)
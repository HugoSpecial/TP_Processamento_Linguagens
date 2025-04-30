import sys
from lexer import SQLLexer
from parser import SQLParser
from semantic import execute_command
from database import database

def run_cql_file(filename):
    try:
        with open(filename, 'r') as file:
            # Read entire content at once
            content = file.read()
            
            lexer = SQLLexer()
            lexer.build()
            lexer.input(content)
            
            # For debugging, print all tokens
            # print("=== TOKENS ===")
            # while True:
            #     tok = lexer.token()
            #     if not tok:
            #         break
            #     print(tok)
            
            # Reset lexer for parsing
            lexer.input(content)
            parser = SQLParser()
            parser.build()
            
            try:
                parsed = parser.parse(content)
                if parsed:
                    execute_command(parsed)
            except Exception as e:
                print(f"[ERRO] {str(e)}")

    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{filename}' não encontrado")
    except Exception as e:
        print(f"[ERRO] Falha ao processar o arquivo '{filename}': {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cql_interpreter.py arquivo.cql")
    else:
        run_cql_file(sys.argv[1])

import sys
from lexer import lexer
from parser import parse_sql
from semantic import execute_command
from database import database

def run_cql_file(filename):
    try:
        with open(filename, 'r') as file:
            print(f"\nExecutando arquivo: {filename}")
            for line in file:
                line = line.strip()
                if not line or line.startswith('--'):
                    continue
                
                try:
                    parsed = parse_sql(line)
                    execute_command(parsed)
                except Exception as e:
                    print(f"[ERRO] Linha: '{line}'")
                    print(f"       {str(e)}")
    
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{filename}' não encontrado")
    
   # print("\nEstado final da base de dados:")
   # print(database)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cql_interpreter.py arquivo.cql")
    else:
        run_cql_file(sys.argv[1])
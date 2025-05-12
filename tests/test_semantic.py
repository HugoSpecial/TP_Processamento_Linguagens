import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from semantic import execute_command
import parser as parser_module

parser = parser_module.build_parser()

examples = [
    'IMPORT TABLE estacoes FROM "data/estacoes.csv";',
    'IMPORT TABLE observacoes FROM "data/observacoes.csv";',
    "SELECT * FROM estacoes;",
    "SELECT Id,Local FROM estacoes;",
]

for example in examples:
    print("\nInput:", example)
    parsed = parser.parse(example)
    execute_command(parsed)
    print("\n")
#! VER ISTO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from semantic import interpret

examples = [
    'IMPORT TABLE estacoes FROM "data/estacoes.csv";',
    'IMPORT TABLE observacoes FROM "data/observacoes.csv";',
    "SELECT * FROM estacoes;",
    "SELECT Id,Local FROM estacoes limit 2;",
]

for example in examples:
    print("\nInput:", example)
    result = interpret(example)
    print("Result:", result)
    print("\n")
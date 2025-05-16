import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import parser

parser.build_parser()

examples = [
    'IMPORT TABLE estacoes FROM "estacoes.csv";',
    "SELECT DataHoraObservacao,Id FROM observacoes;",
    "SELECT * FROM observacoes WHERE Temperatura > 22 LIMIT 1;",
    "CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22;",
]

for example in examples:
    print("\nInput:", example)
    result = parser.parse_sql(example)
    print("AST:", result)
    print("\n")

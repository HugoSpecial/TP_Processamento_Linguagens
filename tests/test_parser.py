import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import parser

# Constrói o parser (se quiser que AST esteja ativo por padrão, usa ast=True)
parser.build_parser()

examples = [
    'IMPORT TABLE estacoes FROM "estacoes.csv";',
    "SELECT DataHoraObservacao,Id FROM observacoes;",
    "SELECT * FROM observacoes WHERE Temperatura > 22 LIMIT 1;",
    "CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22;",
]

for example in examples:
    print("\nInput:", example)
    result = parser.parse_sql(example, ast=True)
    print("AST:", result)
    print("\n")

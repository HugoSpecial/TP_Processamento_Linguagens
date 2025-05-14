import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lexer as lex_grammar

lexer = lex_grammar.build()

exemplos = [
    "SELECT * FROM clientes;",
    "import table clientes from 'clientes.csv';",
    "EXPORT TABLE clientes AS 'clientes_export.csv';",
    "SELECT * FROM observacoes WHERE IntensidadeVentoKM > 3 LIMIT 2;"
    '-- SELECT * FROM estacoes;'
    '{- SELECT id FROM estacoes; '
    'WHERE IntensidadeVentoKM > 3 LIMIT 2;-}'
]

for frase in exemplos:
    print(f"\nInput: {frase}")
    lexer.input(frase)
    for token in lexer:
        print(token)
from ply import lex

# Adicionando os tokens necessários
tokens = (
    'IMPORT',
    'CREATE',
    'EXPORT',
    'DISCARD',
    'RENAME',
    'PRINT',
    'AS',
    'TABLE',
    'FROM',
    'SELECT',
    'IDENTIFIER',
    'STRING',
    'SEMICOLON',
    'STAR',
    'COMMA',
    'EQUAL',
    'NOTEQUAL',
    'LESS',
    'GREATER',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'LIMIT',
    'WHERE',
    'AND',
    'NUMBER',
    'JOIN',
    'USING',
    'LPAREN',
    'RPAREN',
    "PROCEDURE",
    "DO",
    "END",
    "CALL",
)

# Definindo palavras reservadas
reserved = {
    'IMPORT': 'IMPORT',
    'CREATE':'CREATE',
    'EXPORT': 'EXPORT',
    'TABLE': 'TABLE',
    'FROM': 'FROM',
    'SELECT': 'SELECT',
    'AS': 'AS',
    'DISCARD': 'DISCARD',
    'RENAME': 'RENAME',
    'PRINT': 'PRINT',
    'LIMIT': 'LIMIT',
    'WHERE': 'WHERE',
    'AND': 'AND',
    'JOIN': 'JOIN',
    'USING': 'USING',
    "PROCEDURE": "PROCEDURE",
    "DO": "DO",
    "END": "END",
    "CALL": "CALL",
}

# Expressões regulares simples
t_SEMICOLON = r';'
t_COMMA = r',' 
t_STAR = r'\*'
t_EQUAL = r'='
t_NOTEQUAL = r'<>'
t_LESS = r'<'
t_GREATER = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

t_NUMBER = r'\d+(\.\d+)?'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_comment(t):
    r'\-\-.*'
    pass

def t_MULTI_COMMENT(t):
    r'\{-[\s\S]*?-\}'  # Captura o conteúdo entre {--} e --}
    pass  # Ignora o conteúdo do comentário

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def build():
    lexer = lex.lex()
    return lexer

# Construir o lexer
lexer = lex.lex()
from ply import lex

# Adicionando os tokens necessários
tokens = (
    'IMPORT',
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
    'WHERE',  # Novo token WHERE
    'AND',  # Novo token AND
    'NUMBER'  # Novo token NUMBER
)

# Definindo palavras reservadas
reserved = {
    'IMPORT': 'IMPORT',
    'EXPORT': 'EXPORT',
    'TABLE': 'TABLE',
    'FROM': 'FROM',
    'SELECT': 'SELECT',
    'AS': 'AS',
    'DISCARD': 'DISCARD',
    'RENAME': 'RENAME',
    'PRINT': 'PRINT',
    'LIMIT': 'LIMIT',
}

# Definindo expressões regulares para tokens
t_SEMICOLON = r';'
t_COMMA = r',' 
t_STAR = r'\*'
t_EQUAL = r'='
t_NOTEQUAL = r'<>'  # Not equal to
t_LESS = r'<'
t_GREATER = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_ignore = ' \t'  # Ignora espaços e tabulações
t_WHERE = r'WHERE'
t_AND = r'AND'
t_NUMBER = r'\d+'

# Regras para tokens específicos
def t_SELECT(t):
    r'SELECT'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

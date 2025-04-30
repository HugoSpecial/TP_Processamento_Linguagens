from ply import lex

tokens = (
    'IMPORT', 'CREATE', 'EXPORT', 'DISCARD', 'RENAME', 'PRINT',
    'AS', 'TABLE', 'FROM', 'SELECT', 'IDENTIFIER', 'STRING',
    'SEMICOLON', 'STAR', 'COMMA', 'EQUAL', 'NOTEQUAL',
    'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL',
    'LIMIT', 'WHERE', 'AND', 'NUMBER',
)

reserved = {
    'IMPORT': 'IMPORT',
    'CREATE': 'CREATE',
    'EXPORT': 'EXPORT',
    'DISCARD': 'DISCARD',
    'RENAME': 'RENAME',
    'PRINT': 'PRINT',
    'AS': 'AS',
    'TABLE': 'TABLE',
    'FROM': 'FROM',
    'SELECT': 'SELECT',
    'LIMIT': 'LIMIT',
    'WHERE': 'WHERE',
    'AND': 'AND'
}

t_ignore = ' \t'

def t_COMMENT(t):
    r'--[^\n]*'
    pass  # Completely ignore comments

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Simple tokens
t_SEMICOLON = r';'
t_COMMA = r',' 
t_STAR = r'\*'
t_EQUAL = r'='
t_NOTEQUAL = r'<>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_LESS = r'<'
t_GREATER = r'>'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
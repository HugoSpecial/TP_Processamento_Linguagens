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
    # "SINGLE_COMMENT",
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
    'AND': 'AND'
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
t_ignore = ' \t'

t_NUMBER = r'\d+(\.\d+)?'

# Regra para SELECT (e outras palavras reservadas)
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

def t_comment(t):
    r'\-\-.*'
    pass

# def t_MULTI_COMMENT(t):
#     r'\{-[\s\S]*?-\}'
#     pass


# # Início de comentário de bloco
# def t_COMMENT_BLOCK_START(t):
#     r'\{\-'
#     t.lexer.begin('comment')  # Muda para o estado de comentário

# # Estado 'comment'
# def t_comment_COMMENT_BLOCK_END(t):
#     r'\-\}'
#     t.lexer.begin('INITIAL')  # Volta para o estado normal

# def t_comment_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)

# def t_comment_anything(t):
#     r'.|\n'
#     pass  # Ignora qualquer coisa dentro do comentário

# def t_comment_error(t):
#     t.lexer.skip(1)

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()
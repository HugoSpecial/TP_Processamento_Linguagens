from ply import lex

class SQLLexer:
    # Lista de tokens
    tokens = (
        'IMPORT', 'CREATE', 'EXPORT', 'DISCARD', 'RENAME', 'PRINT', 'AS',
        'TABLE', 'FROM', 'SELECT', 'IDENTIFIER', 'STRING', 'SEMICOLON',
        'STAR', 'COMMA', 'EQUAL', 'NOTEQUAL', 'LESS', 'GREATER',
        'LESS_EQUAL', 'GREATER_EQUAL', 'LIMIT', 'WHERE', 'AND', 'NUMBER',
    )

    # Palavras reservadas
    reserved = {
        'IMPORT': 'IMPORT',
        'CREATE': 'CREATE',
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

    # Tokens simples (literals com nomes)
    t_SEMICOLON = r';'
    t_COMMA = r',' 
    t_STAR = r'\*'
    t_EQUAL = r'='
    t_NOTEQUAL = r'<>' 
    t_LESS = r'<'
    t_GREATER = r'>' 
    t_LESS_EQUAL = r'<='
    t_GREATER_EQUAL = r'>='
    t_NUMBER = r'\d+(\.\d+)?'

    states = (
        ('commentblock', 'exclusive'),
    )

    # Initial state rules
    t_ignore = ' \t'  # Ignore spaces and tabs, but not newlines
    t_commentblock_ignore = ' \t'  # Ignore spaces and tabs in comments too

    # Enter comment block state
    def t_COMMENT_BLOCK_START(self, t):
        r'\{--'
        t.lexer.begin('commentblock')  # Enter comment state
        t.lexer.comment_start = t.lexer.lineno  # Track starting line

    # Comment block rules
    def t_commentblock_COMMENT_BLOCK_END(self, t):
        r'--\}'
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')  # Return to initial state
        return None  # Discard token

    def t_commentblock_CONTENT(self, t):
        r'(.|\n)+?(?=--\}|$)'
        t.lexer.lineno += t.value.count('\n')
        return None  # Discard content

    # Error handling in comment state
    def t_commentblock_error(self, t):
        print(f"Illegal character in comment: '{t.value[0]}'")
        t.lexer.skip(1)

    # Line comments (unchanged)
    @staticmethod
    def t_COMMENT_LINE(t):
        r'--[^\n]*'
        pass

    # --- Other rules AFTER comments ---
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value.upper(), 'IDENTIFIER')
        return t

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.value = t.value[1:-1]  # Remove as aspas
        return t

    def t_error(self, t):
        # Skip only if it's a newline (common in many languages)
        if t.value[0] == '\n':
            t.lexer.lineno += 1
            t.lexer.skip(1)
        else:
            print(f"Caracter ilegal '{t.value[0]}' na linha {t.lineno}")
            t.lexer.skip(1)

    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()
from ply import yacc
from lexer import tokens, lexer
from database import database

def p_command(p):
    '''
    command : sql_command SEMICOLON
            | empty
    '''
    if len(p) == 3:  # sql_command SEMICOLON
        p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None  # Explicitly return None for empty productions

# IMPORT
def p_sql_command_import(p):
    '''
    sql_command : IMPORT TABLE IDENTIFIER FROM STRING
    '''
    p[0] = ('IMPORT', p[3], p[5])

# EXPORT
def p_sql_command_export(p):
    '''
    sql_command : EXPORT TABLE IDENTIFIER AS STRING
    '''
    p[0] = ('EXPORT', p[3], p[5])

# DISCARD
def p_sql_command_discard(p):
    '''
    sql_command : DISCARD TABLE IDENTIFIER
    '''
    p[0] = ('DISCARD', p[3])

# RENAME
def p_sql_command_rename(p):
    '''
    sql_command : RENAME TABLE IDENTIFIER IDENTIFIER
    '''
    p[0] = ('RENAME', p[3], p[4])

# PRINT
def p_sql_command_print(p):
    '''
    sql_command : PRINT TABLE IDENTIFIER
    '''
    p[0] = ('PRINT', p[3])

# SELECT commands
def p_sql_command_select(p):
    '''
    sql_command : SELECT star_columns FROM IDENTIFIER
                | SELECT column_list FROM IDENTIFIER
                | SELECT star_columns FROM IDENTIFIER WHERE condition_list
                | SELECT column_list FROM IDENTIFIER WHERE condition_list
                | SELECT star_columns FROM IDENTIFIER LIMIT NUMBER
                | SELECT column_list FROM IDENTIFIER LIMIT NUMBER
                | SELECT star_columns FROM IDENTIFIER WHERE condition_list LIMIT NUMBER
                | SELECT column_list FROM IDENTIFIER WHERE condition_list LIMIT NUMBER
    '''
    if len(p) == 5:  # Basic SELECT without WHERE/LIMIT
        if isinstance(p[2], list):
            p[0] = ('SELECT_COLUMNS', p[4], p[2])
        else:
            p[0] = ('SELECT_ALL', p[4])
    elif len(p) == 7:  # SELECT with WHERE or LIMIT
        if p[5] == 'WHERE':
            if isinstance(p[2], list):
                p[0] = ('SELECT_COLUMNS_WHERE', p[4], p[2], p[6])
            else:
                p[0] = ('SELECT_ALL_WHERE', p[4], p[6])
        else:  # LIMIT
            if isinstance(p[2], list):
                p[0] = ('SELECT_COLUMNS_LIMIT', p[4], p[2], p[6])
            else:
                p[0] = ('SELECT_ALL_LIMIT', p[4], p[6])
    else:  # SELECT with WHERE and LIMIT (len == 9)
        if isinstance(p[2], list):
            p[0] = ('SELECT_COLUMNS_WHERE_LIMIT', p[4], p[2], p[6], p[8])
        else:
            p[0] = ('SELECT_ALL_WHERE_LIMIT', p[4], p[6], p[8])

# CREATE TABLE AS SELECT
def p_sql_command_create(p):
    '''
    sql_command : CREATE TABLE IDENTIFIER SELECT star_columns FROM IDENTIFIER
                | CREATE TABLE IDENTIFIER SELECT column_list FROM IDENTIFIER
                | CREATE TABLE IDENTIFIER SELECT star_columns FROM IDENTIFIER WHERE condition_list
                | CREATE TABLE IDENTIFIER SELECT column_list FROM IDENTIFIER WHERE condition_list
    '''
    if len(p) == 8:  # Without WHERE
        if isinstance(p[5], list):
            p[0] = ('CREATE_TABLE', p[3], p[7], p[5], None)
        else:
            p[0] = ('CREATE_TABLE', p[3], p[7], '*', None)
    else:  # With WHERE (len == 10)
        if isinstance(p[5], list):
            p[0] = ('CREATE_TABLE', p[3], p[7], p[5], p[9])
        else:
            p[0] = ('CREATE_TABLE', p[3], p[7], '*', p[9])

# Column definitions
def p_star_columns(p):
    '''
    star_columns : STAR
    '''
    p[0] = '*'

def p_column_list(p):
    '''
    column_list : IDENTIFIER
               | column_list COMMA IDENTIFIER
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Condition handling
def p_condition_list(p):
    '''
    condition_list : condition
                  | condition_list AND condition
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_condition(p):
    '''
    condition : IDENTIFIER comparison_operator value
    '''
    p[0] = (p[1], p[2], p[3])

def p_comparison_operator(p):
    '''
    comparison_operator : EQUAL
                        | NOTEQUAL
                        | LESS
                        | GREATER
                        | LESS_EQUAL
                        | GREATER_EQUAL
    '''
    p[0] = p[1]

def p_value(p):
    '''
    value : STRING
          | NUMBER
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe na entrada: '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: fim inesperado do arquivo")

# Build the parser
parser = yacc.yacc()

def parse_sql(sql):
    try:
        return parser.parse(sql, lexer=lexer)
    except Exception as e:
        print(f"Erro durante o parsing: {str(e)}")
        return None
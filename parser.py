# === parser.py ===
from ply import yacc
from lexer import tokens, lexer
from database import database

# AST flag
GENERATE_AST = False

# === Comandos ===
def p_import_command(p):
    """ command : IMPORT TABLE IDENTIFIER FROM STRING SEMICOLON"""
    if GENERATE_AST:
        p[0] = {'op': 'IMPORT', 'args': [p[3], p[5]]}
    else:
        p[0] = ('IMPORT', p[3], p[5])

def p_export_command(p):
    """ command : EXPORT TABLE IDENTIFIER AS STRING SEMICOLON"""
    if GENERATE_AST:
        p[0] = {'op': 'EXPORT', 'args': [p[3], p[5]]}
    else:
        p[0] = ('EXPORT', p[3], p[5])

def p_discard_command(p):
    """ command : DISCARD TABLE IDENTIFIER SEMICOLON"""
    if GENERATE_AST:
        p[0] = {'op': 'DISCARD', 'args': [p[3]]}
    else:
        p[0] = ('DISCARD', p[3])

def p_rename_command(p):
    """ command : RENAME TABLE IDENTIFIER IDENTIFIER SEMICOLON"""
    if GENERATE_AST:
        p[0] = {'op': 'RENAME', 'args': [p[3], p[4]]}
    else:
        p[0] = ('RENAME', p[3], p[4])

def p_print_command(p):
    """ command : PRINT TABLE IDENTIFIER SEMICOLON"""
    if GENERATE_AST:
        p[0] = {'op': 'PRINT', 'args': [p[3]]}
    else:
        p[0] = ('PRINT', p[3])

def p_select_command(p):
    """
    command : SELECT star_columns FROM IDENTIFIER WHERE condition_list SEMICOLON
            | SELECT column_list FROM IDENTIFIER WHERE condition_list SEMICOLON
            | SELECT star_columns FROM IDENTIFIER SEMICOLON
            | SELECT column_list FROM IDENTIFIER SEMICOLON
    """
    if GENERATE_AST:
        if len(p) == 8:
            columns = p[2] if isinstance(p[2], list) else '*'
            p[0] = {'op': 'SELECT', 'args': [columns, p[4], p[6]]}
        else:
            columns = p[2] if isinstance(p[2], list) else '*'
            p[0] = {'op': 'SELECT', 'args': [columns, p[4]]}
    else:
        if len(p) == 8:
            if isinstance(p[2], list):
                p[0] = ('SELECT_COLUMNS_WHERE', p[4], p[2], p[6])
            else:
                p[0] = ('SELECT_ALL_WHERE', p[4], p[6])
        else:
            if isinstance(p[2], list):
                p[0] = ('SELECT_COLUMNS', p[4], p[2])
            else:
                p[0] = ('SELECT_ALL', p[4])

def p_select_command_limit(p):
    """
    command : SELECT star_columns FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON
            | SELECT column_list FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON
    """
    if GENERATE_AST:
        columns = p[2] if isinstance(p[2], list) else '*'
        p[0] = {'op': 'SELECT', 'args': [columns, p[4], p[6], p[8]]}
    else:
        if isinstance(p[2], list):
            p[0] = ('SELECT_COLUMNS_WHERE_LIMIT', p[4], p[2], p[6], p[8])
        else:
            p[0] = ('SELECT_ALL_WHERE_LIMIT', p[4], p[6], p[8])

def p_select_simple_limit(p):
    """
    command : SELECT star_columns FROM IDENTIFIER LIMIT NUMBER SEMICOLON
            | SELECT column_list FROM IDENTIFIER LIMIT NUMBER SEMICOLON
    """
    if GENERATE_AST:
        columns = p[2] if isinstance(p[2], list) else '*'
        p[0] = {'op': 'SELECT', 'args': [columns, p[4], p[6]]}
    else:
        if isinstance(p[2], list):
            p[0] = ('SELECT_COLUMNS_LIMIT', p[4], p[2], p[6])
        else:
            p[0] = ('SELECT_ALL_LIMIT', p[4], p[6])

def p_create_table_command(p):
    """
    command : CREATE TABLE IDENTIFIER SELECT star_columns FROM IDENTIFIER WHERE condition_list SEMICOLON
            | CREATE TABLE IDENTIFIER SELECT column_list FROM IDENTIFIER WHERE condition_list SEMICOLON
    """
    columns = p[5] if isinstance(p[5], list) else '*'
    if GENERATE_AST:
        p[0] = {
            'op': 'CREATE_TABLE',
            'args': [p[3], {'op': 'SELECT', 'args': [columns, p[7], p[9]]}]
        }
    else:
        p[0] = ('CREATE_TABLE', p[3], p[7], columns, p[9])

def p_create_table_join_using(p):
    """ command : CREATE TABLE IDENTIFIER FROM IDENTIFIER JOIN IDENTIFIER USING LPAREN IDENTIFIER RPAREN SEMICOLON"""
    if GENERATE_AST:
        p[0] = {
            'op': 'CREATE_TABLE_JOIN',
            'args': [p[3], p[5], p[7], p[10]]
        }
    else:
        p[0] = ('CREATE_TABLE_JOIN', p[3], p[5], p[7], p[10])

def p_procedure_command(p):
    """command : PROCEDURE IDENTIFIER DO procedure_body END"""
    if GENERATE_AST:
        p[0] = {'op': 'DEFINE_PROCEDURE', 'args': [p[2], p[4]]}
    else:
        p[0] = ("DEFINE_PROCEDURE", p[2], p[4])

def p_call_command(p):
    """ command : CALL IDENTIFIER SEMICOLON"""
    if GENERATE_AST:
        p[0] = {'op': 'CALL_PROCEDURE', 'args': [p[2]]}
    else:
        p[0] = ("CALL_PROCEDURE", p[2])

# === Auxiliares ===
def p_star_columns(p):
    """ star_columns : STAR"""
    p[0] = '*'

def p_column_list(p):
    """
    column_list : IDENTIFIER
                | column_list COMMA IDENTIFIER
    """
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_condition_list(p):
    """
    condition_list : condition
                   | condition_list AND condition
    """
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_condition(p):
    """ condition : IDENTIFIER comparison_operator value"""
    p[0] = (p[1], p[2], p[3])

def p_comparison_operator(p):
    """
    comparison_operator : EQUAL
                        | NOTEQUAL
                        | LESS
                        | GREATER
                        | LESS_EQUAL
                        | GREATER_EQUAL
    """
    p[0] = p[1]

def p_procedure_body(p):
    """
    procedure_body : command
                   | procedure_body command
    """
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_value(p):
    """
    value : STRING
          | NUMBER
    """
    p[0] = p[1]

def p_empty_command(p):
    """ command : empty"""
    p[0] = None

def p_empty(p):
    """ empty :"""
    pass

def p_error(p):
    print(f"Erro de sintaxe na entrada: {p}")

def build_parser():
    yacc.yacc(method='LALR', write_tables=False)
    return yacc

parser = yacc.yacc()

def parse_sql(sql, ast=False):
    global GENERATE_AST
    GENERATE_AST = ast
    return parser.parse(sql)


from ply import yacc
from lexer import tokens, lexer
from database import database

def p_program(p):
    """program : command
              | program command"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_command(p):
    """command : table_command
              | query_command
              | create_command
              | procedure_command
              | call_command
              | SEMICOLON"""  # Comando vazio
    p[0] = p[1] if len(p) > 1 else None

def p_table_command(p):
    """table_command : import_command
                    | export_command
                    | discard_command
                    | rename_command
                    | print_command"""
    p[0] = p[1]

def p_import_command(p):
    """import_command : IMPORT TABLE IDENTIFIER FROM STRING SEMICOLON"""
    p[0] = ('IMPORT', p[3], p[5])

def p_export_command(p):
    """export_command : EXPORT TABLE IDENTIFIER AS STRING SEMICOLON"""
    p[0] = ('EXPORT', p[3], p[5])

def p_discard_command(p):
    """discard_command : DISCARD TABLE IDENTIFIER SEMICOLON"""
    p[0] = ('DISCARD', p[3])

def p_rename_command(p):
    """rename_command : RENAME TABLE IDENTIFIER IDENTIFIER SEMICOLON"""
    p[0] = ('RENAME', p[3], p[4])

def p_print_command(p):
    """print_command : PRINT TABLE IDENTIFIER SEMICOLON"""
    p[0] = ('PRINT', p[3])

def p_query_command(p):
    """query_command : select_command
                    | select_where_command
                    | select_limit_command
                    | select_where_limit_command"""
    p[0] = p[1]

def p_select_command(p):
    """select_command : SELECT columns FROM IDENTIFIER SEMICOLON"""
    p[0] = ('SELECT', p[2], p[4])

def p_select_where_command(p):
    """select_where_command : SELECT columns FROM IDENTIFIER WHERE condition_list SEMICOLON"""
    p[0] = ('SELECT', p[2], p[4], p[6])  # Alterado para 'SELECT' em vez de 'SELECT_WHERE'


def p_select_simple_limit(p):
    """
    select_limit_command : SELECT columns FROM IDENTIFIER LIMIT NUMBER SEMICOLON
    """
    p[0] = ('SELECT', p[2], p[4], None, p[6])

def p_select_where_limit_command(p):
    """select_where_limit_command : SELECT columns FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON"""
    p[0] = ('SELECT_WHERE_LIMIT', p[2], p[4], p[6], p[8])

def p_create_command(p):
    """create_command : create_table_select_command
                     | create_table_join_command"""
    p[0] = p[1]

def p_create_table_select_command(p):
    """create_table_select_command : CREATE TABLE IDENTIFIER SELECT columns FROM IDENTIFIER where_clause SEMICOLON"""
    columns = p[5] if isinstance(p[5], list) else '*'
    p[0] = ('CREATE_TABLE_SELECT', p[3], p[7], columns, p[8] if len(p) > 9 else None)

def p_create_table_join_command(p):
    """create_table_join_command : CREATE TABLE IDENTIFIER FROM IDENTIFIER JOIN IDENTIFIER USING LPAREN IDENTIFIER RPAREN SEMICOLON"""
    p[0] = ('CREATE_TABLE_JOIN', p[3], p[5], p[7], p[10])

def p_procedure_command(p):
    """procedure_command : PROCEDURE IDENTIFIER DO procedure_body END"""
    p[0] = ("PROCEDURE", p[2], p[4])

def p_procedure_body(p):
    """procedure_body : command
                     | procedure_body command"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_call_command(p):
    """call_command : CALL IDENTIFIER SEMICOLON"""
    p[0] = ("CALL", p[2])

def p_columns(p):
    """columns : STAR
              | column_list"""
    p[0] = '*' if p[1] == '*' else p[1]

def p_column_list(p):
    """column_list : IDENTIFIER
                  | column_list COMMA IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_condition_list(p):
    """condition_list : condition
                     | condition_list AND condition"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_condition(p):
    """condition : IDENTIFIER comparison_operator value"""
    p[0] = (p[1], p[2], p[3])

def p_comparison_operator(p):
    """comparison_operator : EQUAL
                          | NOTEQUAL
                          | LESS
                          | GREATER
                          | LESS_EQUAL
                          | GREATER_EQUAL"""
    p[0] = p[1]

def p_value(p):
    """value : STRING
            | NUMBER"""
    p[0] = p[1]

def p_where_clause(p):
    """where_clause : WHERE condition_list
                   | empty"""
    p[0] = p[2] if len(p) == 3 else None

def p_empty(p):
    """empty :"""
    pass

def p_error(p):
    print(f"Erro de sintaxe na entrada: {p}")

def build_parser():
    parser = yacc.yacc()
    return parser

parser = build_parser()

def parse_sql(sql):
    return parser.parse(sql)
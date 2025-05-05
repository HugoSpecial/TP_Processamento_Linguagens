from ply import yacc
from lexer import tokens, lexer
from database import database

# IMPORT
def p_import_command(p):
    '''
    command : IMPORT TABLE IDENTIFIER FROM STRING SEMICOLON
    '''
    p[0] = ('IMPORT', p[3], p[5])

# EXPORT
def p_export_command(p):
    '''
    command : EXPORT TABLE IDENTIFIER AS STRING SEMICOLON
    '''
    p[0] = ('EXPORT', p[3], p[5])

# DISCARD
def p_discard_command(p):
    '''
    command : DISCARD TABLE IDENTIFIER SEMICOLON
    '''
    p[0] = ('DISCARD', p[3])

# RENAME
def p_rename_command(p):
    '''
    command : RENAME TABLE IDENTIFIER IDENTIFIER SEMICOLON
    '''
    p[0] = ('RENAME', p[3], p[4])

# PRINT
def p_print_command(p):
    '''
    command : PRINT TABLE IDENTIFIER SEMICOLON
    '''
    p[0] = ('PRINT', p[3])

# SELECT
def p_select_command(p):
    '''
    command : SELECT star_columns FROM IDENTIFIER WHERE condition_list SEMICOLON
            | SELECT column_list FROM IDENTIFIER WHERE condition_list SEMICOLON
            | SELECT star_columns FROM IDENTIFIER SEMICOLON
            | SELECT column_list FROM IDENTIFIER SEMICOLON
    '''
    if len(p) == 8:  # SELECT ... WHERE ...
        if isinstance(p[2], list):  # column list
            table_name = p[4]
            columns = p[2]
            conditions = p[6]
            p[0] = ('SELECT_COLUMNS_WHERE', table_name, columns, conditions)
        else:  # '*' (star)
            table_name = p[4]
            conditions = p[6]
            p[0] = ('SELECT_ALL_WHERE', table_name, conditions)
    elif len(p) == 6:  # SELECT ... ;
        if isinstance(p[2], list):  # column list
            table_name = p[4]
            columns = p[2]
            p[0] = ('SELECT_COLUMNS', table_name, columns)
        else:  # '*' (star)
            table_name = p[4]
            p[0] = ('SELECT_ALL', table_name)

# LIMIT opcional
def p_select_command_limit(p):
    '''
    command : SELECT star_columns FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON
            | SELECT column_list FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON
    '''
    if isinstance(p[2], list):  # column list
        table_name = p[4]
        columns = p[2]
        conditions = p[6]
        limit = p[8]
        p[0] = ('SELECT_COLUMNS_WHERE_LIMIT', table_name, columns, conditions, limit)
    else:  # '*' (star)
        table_name = p[4]
        conditions = p[6]
        limit = p[8]
        p[0] = ('SELECT_ALL_WHERE_LIMIT', table_name, conditions, limit)

def p_create_table_command(p):
    '''
    command : CREATE TABLE IDENTIFIER SELECT star_columns FROM IDENTIFIER WHERE condition_list SEMICOLON
            | CREATE TABLE IDENTIFIER SELECT column_list FROM IDENTIFIER WHERE condition_list SEMICOLON
    '''
    if isinstance(p[5], list):  # SELECT column_list
        table_name = p[3]         # nome da nova tabela
        columns = p[5]            # lista de colunas
        source_table = p[7]       # tabela de origem
        conditions = p[9]         # condições WHERE
        p[0] = ('CREATE_TABLE', table_name, source_table, columns, conditions)
    else:  # SELECT star_columns
        table_name = p[3]         # nome da nova tabela
        source_table = p[7]       # tabela de origem
        conditions = p[9]         # condições WHERE
        p[0] = ('CREATE_TABLE', table_name, source_table, '*', conditions)


# Colunas: '*' ou lista
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

# Condições
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

def p_empty_command(p):
    'command : empty'
    p[0] = None

def p_empty(p):
    'empty :'
    pass

# Erro
def p_error(p):
    print(f"Erro de sintaxe na entrada: {p}")

# Criação do parser
parser = yacc.yacc()

# Função de parse
def parse_sql(sql):
    return parser.parse(sql)
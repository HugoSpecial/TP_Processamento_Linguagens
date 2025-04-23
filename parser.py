from ply import yacc
from lexer import tokens, lexer
from database import database

# Gramática para o import
def p_import_command(p):
    '''
    command : IMPORT TABLE IDENTIFIER FROM STRING SEMICOLON
    '''
    p[0] = ('IMPORT', p[3], p[5])

def p_export_command(p):
    '''
    command : EXPORT TABLE IDENTIFIER AS STRING SEMICOLON
    '''
    p[0] = ('EXPORT', p[3], p[5])

def p_discard_command(p):
    '''
    command : DISCARD TABLE IDENTIFIER SEMICOLON
    '''
    p[0] = ('DISCARD', p[3])

def p_rename_command(p):
    '''
    command : RENAME TABLE IDENTIFIER IDENTIFIER SEMICOLON
    '''
    p[0] = ('RENAME', p[3], p[4])

def p_print_command(p):
    '''
    command : PRINT TABLE IDENTIFIER SEMICOLON
    '''
    p[0] = ('PRINT', p[3])

# Gramática para SELECT
def p_select_command(p):
    '''
    command : SELECT star_columns FROM IDENTIFIER WHERE condition_list SEMICOLON
            | SELECT column_list FROM IDENTIFIER WHERE condition_list SEMICOLON
            | SELECT star_columns FROM IDENTIFIER SEMICOLON
            | SELECT column_list FROM IDENTIFIER SEMICOLON
    '''
    if len(p) == 8:  # Inclui SELECT ... WHERE ... ;
        if isinstance(p[2], list):  # É uma lista de colunas
            table_name = p[4]
            columns = p[2]
            conditions = p[6]
            p[0] = ('SELECT_COLUMNS_WHERE', table_name, columns, conditions)
        else:  # Deve ser '*'
            table_name = p[4]
            conditions = p[6]
            p[0] = ('SELECT_ALL_WHERE', table_name, conditions)
    elif len(p) == 6:  # SELECT ... ;
        if isinstance(p[2], list):
            table_name = p[4]
            columns = p[2]
            p[0] = ('SELECT_COLUMNS', table_name, columns)
        else:
            table_name = p[4]
            p[0] = ('SELECT_ALL', table_name)

# Gramática para a lista de condições
def p_condition_list(p):
    '''
    condition_list : condition
                  | condition_list AND condition
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Gramática para as condições (comparação de coluna com valor)
def p_condition(p):
    '''
    condition : IDENTIFIER comparison_operator value
    '''
    p[0] = (p[1], p[2], p[3])

# Gramática para os operadores de comparação
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

# Gramática para a cláusula WHERE e AND
def p_where_clause(p):
    '''
    condition_list : WHERE condition
                  | WHERE condition_list AND condition
    '''
    if len(p) == 3:  # WHERE condition
        p[0] = [p[2]]
    else:  # WHERE condition_list AND condition
        p[0] = p[2] + [p[4]]

# Gramática para o valor (STRING ou NUMBER)
def p_value(p):
    '''
    value : STRING
          | NUMBER
    '''
    p[0] = p[1]

# Gramática para a cláusula LIMIT
def p_limit(p):
    '''
    command : SELECT star_columns FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON
            | SELECT column_list FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON
    '''
    if p[3] == '*':  # SELECT * FROM <tabela> WHERE <condições> LIMIT <n>
        table_name = p[4]
        conditions = p[6]
        limit = p[8]
        p[0] = ('SELECT_ALL_WHERE_LIMIT', table_name, conditions, limit)
    else:  # SELECT <colunas> FROM <tabela> WHERE <condições> LIMIT <n>
        table_name = p[4]
        columns = p[2]
        conditions = p[6]
        limit = p[8]
        p[0] = ('SELECT_COLUMNS_WHERE_LIMIT', table_name, columns, conditions, limit)

# Gramática para colunas com o uso de *
def p_star_columns(p):
    '''
    star_columns : STAR
    '''
    p[0] = '*'  # Usando o token STAR para representar o * (seleção de todas as colunas)

# Gramática para a lista de colunas
def p_column_list(p):
    '''
    column_list : IDENTIFIER
                | column_list COMMA IDENTIFIER
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Função de erro
def p_error(p):
    print(f"Erro de sintaxe na entrada: {p}")

# Criando o parser
parser = yacc.yacc()

# Função para parsear o SQL
def parse_sql(sql):
    return parser.parse(sql)

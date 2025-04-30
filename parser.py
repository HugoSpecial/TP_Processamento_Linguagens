from ply import yacc
from lexer import SQLLexer  # Seu lexer já existente

class SQLParser:
    def __init__(self):
        self.lexer = None
        self.yacc = None
        self.tokens = None

    def build(self, **kwargs):
        self.lexer = SQLLexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, sql):
        self.lexer.input(sql)
        return self.yacc.parse(lexer=self.lexer.lexer)

    # IMPORT
    def p_import_command(self, p):
        ''' command : IMPORT TABLE IDENTIFIER FROM STRING SEMICOLON '''
        p[0] = ('IMPORT', p[3], p[5])

    # EXPORT
    def p_export_command(self, p):
        ''' command : EXPORT TABLE IDENTIFIER AS STRING SEMICOLON '''
        p[0] = ('EXPORT', p[3], p[5])

    # DISCARD
    def p_discard_command(self, p):
        ''' command : DISCARD TABLE IDENTIFIER SEMICOLON '''
        p[0] = ('DISCARD', p[3])

    # RENAME
    def p_rename_command(self, p):
        ''' command : RENAME TABLE IDENTIFIER IDENTIFIER SEMICOLON '''
        p[0] = ('RENAME', p[3], p[4])

    # PRINT
    def p_print_command(self, p):
        ''' command : PRINT TABLE IDENTIFIER SEMICOLON '''
        p[0] = ('PRINT', p[3])

    # SELECT
    def p_select_command(self, p):
        ''' command : SELECT star_columns FROM IDENTIFIER WHERE condition_list SEMICOLON
                    | SELECT column_list FROM IDENTIFIER WHERE condition_list SEMICOLON
                    | SELECT star_columns FROM IDENTIFIER SEMICOLON
                    | SELECT column_list FROM IDENTIFIER SEMICOLON '''
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

    # SELECT com LIMIT
    def p_select_command_limit(self, p):
        ''' command : SELECT star_columns FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON
                    | SELECT column_list FROM IDENTIFIER WHERE condition_list LIMIT NUMBER SEMICOLON '''
        if isinstance(p[2], list):
            p[0] = ('SELECT_COLUMNS_WHERE_LIMIT', p[4], p[2], p[6], p[8])
        else:
            p[0] = ('SELECT_ALL_WHERE_LIMIT', p[4], p[6], p[8])

    # CREATE TABLE AS SELECT ...
    def p_create_table_command(self, p):
        ''' command : CREATE TABLE IDENTIFIER SELECT star_columns FROM IDENTIFIER WHERE condition_list SEMICOLON
                    | CREATE TABLE IDENTIFIER SELECT column_list FROM IDENTIFIER WHERE condition_list SEMICOLON '''
        if isinstance(p[5], list):
            p[0] = ('CREATE_TABLE', p[3], p[7], p[5], p[9])
        else:
            p[0] = ('CREATE_TABLE', p[3], p[7], '*', p[9])

    # Colunas
    def p_star_columns(self, p):
        ''' star_columns : STAR '''
        p[0] = '*'

    def p_column_list(self, p):
        ''' column_list : IDENTIFIER
                        | column_list COMMA IDENTIFIER '''
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

    # Condições
    def p_condition_list(self, p):
        ''' condition_list : condition
                           | condition_list AND condition '''
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

    def p_condition(self, p):
        ''' condition : IDENTIFIER comparison_operator value '''
        p[0] = (p[1], p[2], p[3])

    def p_comparison_operator(self, p):
        ''' comparison_operator : EQUAL
                                | NOTEQUAL
                                | LESS
                                | GREATER
                                | LESS_EQUAL
                                | GREATER_EQUAL '''
        p[0] = p[1]

    def p_value(self, p):
        ''' value : STRING
                  | NUMBER '''
        p[0] = p[1]

    # Erro
    def p_error(self, p):
        if p:
            print(f"Erro de sintaxe na entrada: {p}")
        # else:
        #     print("Erro de sintaxe: fim inesperado do arquivo")

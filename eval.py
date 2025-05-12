class SQLEval:
    # Tabela de símbolos para armazenar tabelas e variáveis
    symbols = {
        'tables': {},       # Armazena estruturas de tabelas
        'variables': {}     # Armazena variáveis temporárias
    }

    # Operadores adaptados para operações SQL
    operators = {
        # Operadores básicos
        "=": lambda args: args[0] == args[1],
        "<>": lambda args: args[0] != args[1],
        "<": lambda args: args[0] < args[1],
        ">": lambda args: args[0] > args[1],
        "<=": lambda args: args[0] <= args[1],
        ">=": lambda args: args[0] >= args[1],
        
        # Operações SQL
        "SELECT": lambda args: SQLExpEval._select(args),
        "CREATE": lambda args: SQLExpEval._create_table(args),
        "IMPORT": lambda args: SQLExpEval._import_data(args),
        "EXPORT": lambda args: SQLExpEval._export_data(args),
        "PRINT": lambda args: print(args[0]),
        "JOIN": lambda args: SQLExpEval._join_tables(args),
        "WHERE": lambda args: SQLExpEval._filter(args),
        "AS": lambda args: SQLExpEval._alias(args),
        "RENAME": lambda args: SQLExpEval._rename(args),
        "DISCARD": lambda args: SQLExpEval._discard(args),
    }

    @staticmethod
    def _create_table(args):
        """CREATE TABLE nome (col1, col2, ...)"""
        table_name = args[0]
        columns = args[1]
        SQLExpEval.symbols['tables'][table_name] = {
            'columns': columns,
            'data': []
        }
        return f"Table {table_name} created with columns {columns}"

    @staticmethod
    def _select(args):
        """SELECT * FROM tabela"""
        table_name = args[1]  # args[0] seria a lista de colunas ou *
        if table_name not in SQLExpEval.symbols['tables']:
            raise Exception(f"Table {table_name} not found")
        
        # Implementação simplificada - na prática seria mais complexa
        return SQLExpEval.symbols['tables'][table_name]['data']

    @staticmethod
    def _import_data(args):
        """IMPORT 'arquivo' AS tabela"""
        filename = args[0]
        table_name = args[1]
        
        # Simulação - na prática você leria o arquivo
        imported_data = [
            ["data1_row1", "data1_row2"],
            ["data2_row1", "data2_row2"]
        ]
        
        SQLExpEval.symbols['tables'][table_name] = {
            'columns': ["col1", "col2"],
            'data': imported_data
        }
        return f"Data imported from {filename} as table {table_name}"

    @staticmethod
    def _filter(args):
        """WHERE condição"""
        # args[0] seria a condição a ser avaliada
        # Implementação simplificada
        return f"Filter applied: {args[0]}"

    @staticmethod
    def evaluate(ast):
        if isinstance(ast, (int, float, str)):  # constantes
            return ast
        if isinstance(ast, dict):  # operação
            return SQLExpEval._eval_operator(ast)
        if isinstance(ast, list):  # lista de argumentos
            return [SQLExpEval.evaluate(a) for a in ast]
        raise Exception(f"Unknown AST type: {type(ast)}")
    
    @staticmethod
    def _eval_operator(ast):
        if 'op' in ast:
            op = ast["op"]
            args = [SQLExpEval.evaluate(a) for a in ast['args']]
            
            if op in SQLExpEval.operators:
                return SQLExpEval.operators[op](args)
            raise Exception(f"Unknown operator {op}")
        
        if 'var' in ast:  # referência a variável/tabela
            var_name = ast["var"]
            if var_name in SQLExpEval.symbols['tables']:
                return SQLExpEval.symbols['tables'][var_name]
            if var_name in SQLExpEval.symbols['variables']:
                return SQLExpEval.symbols['variables'][var_name]
            raise Exception(f"Variable/Table '{var_name}' not found")
        
        raise Exception("Malformed AST")
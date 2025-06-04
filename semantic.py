import csv
import os
from database import database
from parser import parse_sql

procedures = {}

def evaluate_condition(row, headers, condition):
    column, operator, value = condition
    if column not in headers:
        return False
    
    col_index = headers.index(column)
    cell_value = row[col_index]
    
    try:
        if operator == '=': return str(cell_value) == str(value)
        if operator == '<>': return str(cell_value) != str(value)
        if operator == '<': return float(cell_value) < float(value)
        if operator == '>': return float(cell_value) > float(value)
        if operator == '<=': return float(cell_value) <= float(value)
        if operator == '>=': return float(cell_value) >= float(value)
    except ValueError:
        return False
    
    return False

def process_import(table_name, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            data = [row for row in csv_reader if row and not row[0].startswith('#')]
            
            if not headers:
                raise ValueError("Arquivo sem cabeçalhos")
            
            database.add_table(table_name, headers, data)
            return True
    except Exception as e:
        raise Exception(f"Erro ao importar: {str(e)}")

def process_export(table_name, file_path):
    table = database.get_table(table_name)
    if not table:
        raise Exception(f"Tabela '{table_name}' não encontrada")

    headers = table.get('variaveis', [])
    data = table.get('dados', [])
    
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        return True
    except Exception as e:
        raise Exception(f"Erro ao exportar: {str(e)}")

def execute_import(command):
    _, table_name, file_path = command
    try:
        if process_import(table_name, file_path):
            return f"Tabela '{table_name}' importada com sucesso!"
    except Exception as e:
        return f"[ERRO] {str(e)}"

def execute_export(command):
    _, table_name, file_path = command
    try:
        if process_export(table_name, file_path):
            return f"Tabela '{table_name}' exportada com sucesso!"
    except Exception as e:
        return f"[ERRO] {str(e)}"

def execute_discard(command):
    _, table_name = command
    if database.discard_table(table_name):
        return f"Tabela '{table_name}' descartada com sucesso"
    return f"[ERRO] Tabela '{table_name}' não encontrada"

def execute_rename(command):
    _, old_name, new_name = command
    if database.rename_table(old_name, new_name):
        return f"Tabela renomeada de '{old_name}' para '{new_name}'"
    else:
        return f"[ERRO] Falha ao renomear tabelaaaaaaaaaaaaa"
    return 

def execute_print(command):
    _, table_name = command
    table = database.get_table(table_name)
    if not table:
        return f"[ERRO] Tabela '{table_name}' não encontrada"
    
    output = []
    headers = table['variaveis']
    output.append(" | ".join(headers))
    output.append("-" * len(" | ".join(headers)))
    
    for row in table['dados']:
        output.append(" | ".join(str(x) for x in row))
    
    return "\n".join(output)

def execute_select(command):
    """Executa comandos SELECT com todas as variações"""
    if not command or len(command) < 3:
        return "[ERRO] Comando SELECT inválido: estrutura incorreta"

    cmd_type = command[0]
    
    columns = table_name = conditions = limit = None
    
    if cmd_type == "SELECT":
        if len(command) == 3:  # SELECT columns FROM table
            columns, table_name = command[1], command[2]
        elif len(command) == 4:  # Com WHERE ou LIMIT
            if isinstance(command[3], list):  # Tem WHERE
                columns, table_name, conditions = command[1], command[2], command[3]
            else:  # Tem LIMIT
                columns, table_name, limit = command[1], command[2], command[3]
        elif len(command) == 5:  # Com WHERE e LIMIT
            columns, table_name, conditions, limit = command[1], command[2], command[3], command[4]

    table = database.get_table(table_name)
    if not table:
        return f"[ERRO] Tabela '{table_name}' não encontrada"
    
    headers = table['variaveis']
    data = table['dados']
    
    if columns == '*':
        col_indices = list(range(len(headers)))
        selected_headers = headers
    else:
        try:
            col_indices = [headers.index(col) for col in columns]
            selected_headers = columns
        except ValueError as e:
            return f"[ERRO] Coluna não encontrada: {str(e)}"
    
    if conditions:
        filtered_data = []
        for row in data:
            if all(evaluate_condition(row, headers, cond) for cond in conditions):
                filtered_data.append(row)
    else:
        filtered_data = data
    
    if limit:
        try:
            limit = int(limit)
            filtered_data = filtered_data[:limit]
        except ValueError:
            return f"[ERRO] Valor de LIMIT inválido: {limit}"

    output = []
    output.append(" | ".join(selected_headers))
    output.append("-" * len(" | ".join(selected_headers)))
    
    for row in filtered_data:
        output.append(" | ".join(str(row[i]) for i in col_indices))
    
    return "\n".join(output)

def create_table_select(new_table, source_table, columns, conditions):
    source = database.get_table(source_table)
    if not source:
        return f"[ERRO] Tabela de origem '{source_table}' não encontrada"
    
    headers = source['variaveis']
    data = source['dados']
    
    if columns == '*':
        col_indices = list(range(len(headers)))
        new_headers = headers
    else:
        try:
            col_indices = [headers.index(col) for col in columns]
            new_headers = columns
        except ValueError as e:
            return f"[ERRO] Coluna não encontrada: {str(e)}"
    
    if conditions:
        new_data = []
        for row in data:
            if all(evaluate_condition(row, headers, cond) for cond in conditions):
                new_data.append([row[i] for i in col_indices])
    else:
        new_data = [[row[i] for i in col_indices] for row in data]
    
    database.add_table(new_table, new_headers, new_data)
    return f"Tabela '{new_table}' criada com {len(new_data)} linhas (SELECT de '{source_table}')"

def create_table_join(new_table, table1, table2, join_column):
    """Cria tabela a partir de JOIN"""
    t1 = database.get_table(table1)
    t2 = database.get_table(table2)
    if not t1 or not t2:
        return f"[ERRO] {'Tabela 1' if not t1 else 'Tabela 2'} não encontrada"
    
    if join_column not in t1['variaveis'] or join_column not in t2['variaveis']:
        return f"[ERRO] Coluna de junção '{join_column}' não encontrada em ambas as tabelas"
    
    t1_key_idx = t1['variaveis'].index(join_column)
    t2_key_idx = t2['variaveis'].index(join_column)
    
    new_headers = t1['variaveis'] + [h for h in t2['variaveis'] if h != join_column]
    
    new_data = []
    for row1 in t1['dados']:
        for row2 in t2['dados']:
            if str(row1[t1_key_idx]) == str(row2[t2_key_idx]):
                new_row = row1 + [row2[i] for i in range(len(row2)) if i != t2_key_idx]
                new_data.append(new_row)
    
    database.add_table(new_table, new_headers, new_data)
    return f"Tabela '{new_table}' criada com {len(new_data)} linhas (JOIN de '{table1}' e '{table2}' em '{join_column}')"

def execute_procedure(command):
    if command[0] == "PROCEDURE":
        _, name, body = command
        procedures[name] = body
        return f"Procedimento '{name}' definido com {len(body)} comandos"
    
    elif command[0] == "CALL":
        _, name = command
        if name not in procedures:
            return f"[ERRO] Procedimento '{name}' não definido"
        
        results = []
        for cmd in procedures[name]:
            result = execute_command(cmd)
            if result:
                results.append(result)
        
        return "\n".join(results) if results else None
    
    return f"[ERRO] Comando de procedimento inválido: {command}"

def execute_command(command):
    if not command:
        return None
    
    cmd_type = command[0]
    
    if cmd_type == "IMPORT":
        return execute_import(command)
    elif cmd_type == "EXPORT":
        return execute_export(command)
    elif cmd_type == "DISCARD":
        return execute_discard(command)
    elif cmd_type == "RENAME":
        return execute_rename(command)
    elif cmd_type == "PRINT":
        return execute_print(command)
    elif cmd_type.startswith("SELECT"):
        return execute_select(command)
    elif cmd_type == "CREATE_TABLE_SELECT":
        if len(command) == 5:
            return create_table_select(command[1], command[2], command[3], command[4])
        else:
            return "[ERRO] Comando CREATE_TABLE_SELECT inválido: estrutura incorreta"
    
    elif cmd_type == "CREATE_TABLE_JOIN" or cmd_type == "CREATE_TABLE_JOIN":
        # Formato: ('CREATE_TABLE_JOIN', new_table, table1, table2, join_column)
        if len(command) == 5:
            return create_table_join(command[1], command[2], command[3], command[4])
        else:
            return "[ERRO] Comando CREATE_TABLE_JOIN inválido: estrutura incorreta"
    
    elif cmd_type in ("PROCEDURE", "CALL"):
        return execute_procedure(command)
    
    return f"[ERRO] Comando não reconhecido: {cmd_type}"

def interpret(code):
    """Função principal de interpretação"""
    parsed = parse_sql(code)
    if not parsed:
        return None

    results = []
    for command in parsed:
        result = execute_command(command)
        if result:
            results.append(result)
    return results if results else None
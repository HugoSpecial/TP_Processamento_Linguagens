import csv
from database import database

# Função para processar a importação
def process_import(table_name, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            data = list(csv_reader)

            if not headers:
                raise ValueError("Arquivo sem cabeçalhos")
            if data and any(len(headers) != len(row) for row in data):
                raise ValueError("Número de colunas inconsistente")

            database.add_table(table_name, headers, data)
            return True

    except FileNotFoundError:
        raise Exception(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        raise Exception(f"Erro semântico: {str(e)}")

# Função para processar a exportação
def process_export(table_name, file_path):
    table = database.get_table(table_name)
    if not table:
        raise Exception(f"Tabela '{table_name}' não encontrada")

    headers = table.get('variaveis') or table.get('headers')
    data = table.get('dados') or table.get('data')

    if headers is None or data is None:
        raise Exception("Estrutura da tabela inválida")

    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
            print(f"Tabela '{table_name}' exportada com sucesso para '{file_path}'")
    except Exception as e:
        raise Exception(f"Erro ao exportar tabela: {str(e)}")

def evaluate_condition(row, headers, condition):
    column_name, operator, value = condition
    if column_name not in headers:
        return False
    col_index = headers.index(column_name)
    column_value = row[col_index]

    if operator == '=':
        return column_value == value
    elif operator == '<>':
        return column_value != value
    elif operator == '<':
        return column_value < value
    elif operator == '>':
        return column_value > value
    elif operator == '<=':
        return column_value <= value
    elif operator == '>=':
        return column_value >= value
    return False

# Função para executar os comandos
def execute_command(parsed):
    if parsed is None:
    # Linha vazia ou comentário ignorado
        return

    if not parsed or len(parsed) < 1:
        print("[ERRO] Comando inválido.")
        return

    cmd_type = parsed[0]

    if cmd_type == 'IMPORT' and len(parsed) >= 3:
        _, table_name, file_path = parsed
        if process_import(table_name, file_path):
            print(f"Tabela '{table_name}' importada com sucesso!")

    elif cmd_type == 'SELECT_ALL' and len(parsed) >= 2:
        table_name = parsed[1]
        table = database.get_table(table_name)
        if table is None:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")
        elif 'dados' not in table:
            print(f"[ERRO] Estrutura da tabela '{table_name}' inválida.")
        elif not table['dados']:
            print(f"A tabela '{table_name}' está vazia.")
        else:
            print(f"Selecionando todos os dados da tabela '{table_name}':")
            for row in table['dados']:
                print(row)

    elif cmd_type == 'SELECT_COLUMNS' and len(parsed) >= 3:
        table_name, columns = parsed[1], parsed[2]
        table = database.get_table(table_name)
        if table:
            print(f"Selecionando colunas '{', '.join(columns)}' da tabela '{table_name}':")
            col_indexes = [table['variaveis'].index(col) for col in columns]
            for row in table['dados']:
                print([row[i] for i in col_indexes])

    elif cmd_type == 'EXPORT' and len(parsed) >= 3:
        _, table_name, file_path = parsed
        process_export(table_name, file_path)

    elif cmd_type == 'DISCARD' and len(parsed) >= 2:
        table_name = parsed[1]
        table = database.get_table(table_name)
        if table:
            table['dados'] = []
            print(f"Dados da tabela '{table_name}' excluídos com sucesso.")
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")

    elif cmd_type == 'RENAME' and len(parsed) >= 3:
        old_name, new_name = parsed[1], parsed[2]
        table = database.get_table(old_name)
        if table:
            database.rename_table(old_name, new_name)
            print(f"Tabela '{old_name}' renomeada para '{new_name}'.")
        else:
            print(f"[ERRO] Tabela '{old_name}' não encontrada.")

    elif cmd_type == 'PRINT' and len(parsed) >= 2:
        table_name = parsed[1]
        table = database.get_table(table_name)
        if table:
            print(f"Imprimindo os dados da tabela '{table_name}':")
            for row in table['dados']:
                print(row)
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")

    elif cmd_type == 'SELECT_ALL_WHERE' and len(parsed) >= 3:
        table_name, conditions = parsed[1], parsed[2]
        table = database.get_table(table_name)
        if table:
            headers = table['variaveis']
            print(f"Selecionando todos os dados da tabela '{table_name}' com condições:")
            for row in table['dados']:
                if all(evaluate_condition(row, headers, cond) for cond in conditions):
                    print(row)
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")

    elif cmd_type == 'SELECT_COLUMNS_WHERE' and len(parsed) >= 4:
        table_name, columns, conditions = parsed[1], parsed[2], parsed[3]
        table = database.get_table(table_name)
        if table:
            headers = table['variaveis']
            print(f"Selecionando colunas '{', '.join(columns)}' da tabela '{table_name}' com condições:")
            col_indexes = [headers.index(col) for col in columns]
            for row in table['dados']:
                if all(evaluate_condition(row, headers, cond) for cond in conditions):
                    print([row[i] for i in col_indexes])
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")

    elif cmd_type == 'SELECT_ALL_WHERE_LIMIT' and len(parsed) >= 4:
        table_name, conditions, limit = parsed[1], parsed[2], parsed[3]
        table = database.get_table(table_name)
        if table:
            headers = table['variaveis']
            print(f"Selecionando dados da tabela '{table_name}' com condições e limite {limit}:")
            count = 0
            for row in table['dados']:
                if all(evaluate_condition(row, headers, cond) for cond in conditions):
                    print(row)
                    count += 1
                if count == limit:
                    break
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")

    elif cmd_type == 'SELECT_COLUMNS_WHERE_LIMIT' and len(parsed) >= 5:
        table_name, columns, conditions, limit = parsed[1], parsed[2], parsed[3], parsed[4]
        table = database.get_table(table_name)
        if table:
            headers = table['variaveis']
            print(f"Selecionando colunas '{', '.join(columns)}' da tabela '{table_name}' com condições e limite {limit}:")
            col_indexes = [headers.index(col) for col in columns]
            count = 0
            for row in table['dados']:
                if all(evaluate_condition(row, headers, cond) for cond in conditions):
                    print([row[i] for i in col_indexes])
                    count += 1
                if count == limit:
                    break
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")
    
    elif cmd_type == 'CREATE_TABLE':
        new_table_name, source_table, columns, conditions = parsed[1], parsed[2], parsed[3], parsed[4]
        table = database.get_table(source_table)
        if not table:
            print(f"[ERRO] Tabela de origem '{source_table}' não encontrada.")
            return

        headers = table['variaveis']
        data = table['dados']

        # Seleciona as colunas
        if columns == '*':
            selected_headers = headers
            selected_indexes = list(range(len(headers)))
        else:
            try:
                selected_headers = columns
                selected_indexes = [headers.index(col) for col in columns]
            except ValueError as e:
                print(f"[ERRO] Coluna não encontrada: {e}")
                return

        # Filtra os dados com base nas condições
        new_data = []
        for row in data:
            if all(evaluate_condition(row, headers, cond) for cond in conditions):
                new_data.append([row[i] for i in selected_indexes])

        # Cria nova tabela no banco
        database.add_table(new_table_name, selected_headers, new_data)
        print(f"Tabela '{new_table_name}' criada com sucesso com {len(new_data)} linha(s).")

    elif cmd_type == 'SELECT_ALL_LIMIT' and len(parsed) >= 3:
        table_name, limit = parsed[1], parsed[2]
        table = database.get_table(table_name)
        if table:
            print(f"Selecionando os primeiros {limit} dados da tabela '{table_name}':")
            for row in table['dados'][:limit]:
                print(row)
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")

    elif cmd_type == 'SELECT_COLUMNS_LIMIT' and len(parsed) >= 4:
        table_name, columns, limit = parsed[1], parsed[2], parsed[3]
        table = database.get_table(table_name)
        if table:
            headers = table['variaveis']
            print(f"Selecionando colunas '{', '.join(columns)}' da tabela '{table_name}' com limite {limit}:")
            col_indexes = [headers.index(col) for col in columns]
            for row in table['dados'][:limit]:
                print([row[i] for i in col_indexes])
        else:
            print(f"[ERRO] Tabela '{table_name}' não encontrada.")

    elif cmd_type == 'CREATE_TABLE_JOIN':
        new_table = parsed[1]
        table1 = parsed[2]
        table2 = parsed[3]
        join_key = parsed[4]

        # Obter as tabelas do banco de dados
        t1 = database.get_table(table1)
        t2 = database.get_table(table2)

        if not t1:
            print(f"[ERRO] Tabela '{table1}' não encontrada.")
            return
        if not t2:
            print(f"[ERRO] Tabela '{table2}' não encontrada.")
            return

        # Verificar se a join_key existe em ambas as tabelas
        if join_key not in t1['variaveis'] or join_key not in t2['variaveis']:
            print(f"[ERRO] Chave de junção '{join_key}' não encontrada em uma ou ambas as tabelas.")
            return

        # Índices da join_key em ambas as tabelas
        t1_key_index = t1['variaveis'].index(join_key)
        t2_key_index = t2['variaveis'].index(join_key)

        # Criar cabeçalhos para a nova tabela
        new_headers = t1['variaveis'] + [col for col in t2['variaveis'] if col != join_key]

        # Criar os dados da nova tabela com base na junção
        new_data = []
        for row1 in t1['dados']:
            for row2 in t2['dados']:
                if row1[t1_key_index] == row2[t2_key_index]:
                    new_row = row1 + [row2[i] for i in range(len(row2)) if i != t2_key_index]
                    new_data.append(new_row)

        # Adicionar a nova tabela ao banco de dados
        database.add_table(new_table, new_headers, new_data)
        print(f"Tabela '{new_table}' criada com sucesso com {len(new_data)} linha(s).")

        

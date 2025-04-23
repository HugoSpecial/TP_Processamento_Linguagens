class Database:
    def __init__(self):
        self.tables = {}
    
    def add_table(self, name, headers, data):
        self.tables[name] = {
            'variaveis': headers,
            'dados': data
        }
    
    def get_table(self, name):
        return self.tables.get(name)

    def rename_table(self, old_name, new_name):
        # Verifica se a tabela existe
        if old_name in self.tables:
            # Renomeia a tabela
            self.tables[new_name] = self.tables.pop(old_name)
            print(f"Tabela '{old_name}' renomeada para '{new_name}'.")
        else:
            raise Exception(f"Tabela '{old_name}' não encontrada.")
    
    def __str__(self):
        return str(self.tables)

database = Database()
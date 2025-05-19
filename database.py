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
        if old_name in self.tables:
            self.tables[new_name] = self.tables.pop(old_name)
            return True
        else:
            raise Exception(f"Tabela '{old_name}' não encontrada.")

    def discard_table(self, name):
        if name in self.tables:
            del self.tables[name]
            print(f"Tabela '{name}' removida com sucesso.")
            return True
        else:
            print(f"Tabela '{name}' não encontrada para remoção.")
            return False

    def __str__(self):
        return str(self.tables)

# Exemplo de uso:
database = Database()

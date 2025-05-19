[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/uCocwY5e)
Processamento de Linguagens (ESI) - laboral
-----

## trabalho prático 

### grupo  09   

  | Número | Nome             |
  |--------|------------------|
  | 27963  | Hugo Especial    |
  | 27966  | Paulo Gonçalves  |
  | 27969  | Marco Cardoso    |

### estrutura do projeto

  [/doc](./doc)   documentação de apoio do projeto desenvolvido / relatório do trabalho prático
  
  [/data](./data) ficheiros de dados a serem usados no programa (.csv) 

  [/input](./input) exemplos de código na linguagem CQL - Comma Query Language  (.cql)

  [/tests](./tests) execução de testes aos analisadores

### dependências de módulos externos 

## PLY
  ```bash
  pip install ply
  ```

### exemplos de utilização 

#### ficheiro de entrada

```bash
python main.py ./input/ficheiro.cql 
```

#### mostragem de Árvore de Sintaxe Abstrata

  ```bash
  python cql_main.py ficheiro.cql ast
  ```

#### de forma interativa (um comando de cada vez)

```bash
python main.py 
>> IMPORT TABLE obs FROM "observacoes.csv" ;
>> SELECT * FROM obs;
['E1', '2.5', '23.2', '133.2', 'NE', '0.7', '58.0', '2025-04-10T19:00']
['E2', '15.1', '12.5', '679.6', 'E', '0.0', '4.2', '2025-04-10T19:00']
['E3', '4.0', '16.4', '0.0', 'NE', '0.0', '1.1', '2025-04-10T19:00']
['E4', '3.6', '16.8', '1.6', 'SW', '0.0', '1.0', '2025-04-10T19:00']
```

## Funcionalidades Principais

  ### Comandos de Tabela

  - `IMPORT TABLE [nome] FROM "[arquivo.csv]";`  
    Importa dados de um arquivo CSV

  - `EXPORT TABLE [nome] AS "[arquivo.csv]";`  
    Exporta tabela para CSV

  - `PRINT TABLE [nome];`  
    Exibe o conteúdo de uma tabela

  - `DISCARD TABLE [nome];`  
    Remove todos os dados de uma tabela

  - `RENAME TABLE [nome antigo] [nome novo];`  
    Renomeia uma tabela

  ### Comandos de Consulta

  - `SELECT * FROM [tabela];`  
    Seleciona todos os dados

  - `SELECT [col1, col2] FROM [tabela];`  
    Seleciona colunas específicas

  - `SELECT ... WHERE [condição];`  
    Filtra resultados

  - `SELECT ... LIMIT [n];`  
    Limita número de resultados

  ### Criação de Tabelas

  - `CREATE TABLE [nome] SELECT ...;`  
    Cria tabela a partir de consulta

  - `CREATE TABLE [nome] FROM [tabela1] JOIN [tabela2] USING [coluna];`  
    Cria tabela via JOIN

  ### Procedures

  - `PROCEDURE [nome] [comandos]; END PROCEDURE;`  
    Define procedimento armazenado

  - `CALL [nome];`  
    Executa procedimento
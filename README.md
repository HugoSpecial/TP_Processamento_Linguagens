  # Trabalho Prático - Processamento de Linguagens

  ## Grupo Nº 09

  | Número | Nome             |
  |--------|------------------|
  | 27963  | Hugo Especial    |
  | 27966  | Paulo Gonçalves  |
  | 27969  | Marco Cardoso    |

  ## Descrição

  Este projeto implementa um interpretador para uma linguagem de consulta personalizada (CQL) que permite:

  - Importar/exportar dados de tabelas em formato CSV  
  - Executar operações básicas de base de dados  
  - Definir e executar procedimentos armazenados  
  - Analisar a estrutura sintática dos comandos  

  ---

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


  ## Instalação

  Clone o repositório:

  ```bash
  git clone https://github.com/HugoSpecial/TP_Processamento_Linguagens.git
  ```

  Instale as dependências:

  ```bash
  pip install ply
  ```

  ---

  ## Uso

  ### Modo de Execução

  ```bash
  python cql_main.py ficheiro.cql
  ```

  ### Modo de Execução com mostragem de Árvore de Sintaxe Abstrata

  ```bash
  python cql_main.py ficheiro.cql ast
  ```

  ### Modo Interativo

  ```bash
  python cql_main.py
  >> import table obs from "data/observacoes.csv";
  Tabela 'obs' importada com sucesso!
  << AST: {'op': 'IMPORT', 'args': ['obs', 'data/observacoes.csv']}
  ```

  ---

  ## Exemplos

  ### Exemplo 1: Importação e Consulta

  ```sql
  IMPORT TABLE clientes FROM "dados/clientes.csv";
  SELECT nome, email FROM clientes WHERE idade > 18 LIMIT 10;
  EXPORT TABLE resultados AS "consulta_clientes.csv";
  ```

  ### Exemplo 2: Procedure

  ```sql
  PROCEDURE importar_dados
    IMPORT TABLE vendas FROM "dados/vendas.csv";
    IMPORT TABLE produtos FROM "dados/produtos.csv";
    CREATE TABLE vendas_completas FROM vendas JOIN produtos USING produto_id;
  END PROCEDURE;

  CALL importar_dados;
  ```

  ## Licença

  Este projeto é apenas para fins educativos.

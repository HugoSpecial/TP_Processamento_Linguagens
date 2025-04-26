-- Nota: Modifiquei o ficheiro do observacoes.csv para ter o numero de resultados condizente com o numero de colunas



import table estacoes from "estacoes.csv";
import table observacoes from "observacoes.csv";
SELECT * FROM observacoes WHERE Temperatura <> 12.5;

-- COMANDOS QUE FUNCIONAM
-- print table estacoes;
-- RENAME TABLE estacoes est;
-- discard table estacoes;
-- export table estacoes as "est.csv";

-- SELECT * FROM observacoes WHERE Temperatura > 22;
-- SELECT * FROM observacoes WHERE Temperatura < 20 AND Temperatura > 10;
-- SELECT * FROM observacoes WHERE Temperatura = 12.5;
-- SELECT * FROM observacoes WHERE Temperatura <> 12.5;
-- select * from est;
-- select Coordenadas from estacoes;
-- select Id from estacoes;
-- select Local from estacoes;
-- select Id, Local from estacoes;


-- COMANDOS QUE NAO FUNCIONAM
-- SELECT * FROM observacoes WHERE IntensidadeVentoKM > 3 LIMIT 2; -- neste caso o uso do LIMIT
-- SELECT Temperatura FROM observacoes WHERE Temperatura > 22; -- Penso que o sor nao pede isto

-- O QUE FALTA
-- Alinea C e D
-- Meter o limit a dar
import table observacoes from "data/observacoes.csv";
import table estacoes from "data/estacoes.csv";

create table ola SELECT Temperatura FROM observacoes WHERE Temperatura >= 22;

print table ola;
export table ola as "ola.txt";
-- print table observacoes;
-- select * from estacoes limit 2;
-- select Id from observacoes limit 3;
{- CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id); print table completo; -}

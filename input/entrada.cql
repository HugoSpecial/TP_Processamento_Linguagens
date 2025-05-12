import table observacoes from "data/observacoes.csv";
import table estacoes from "data/estacoes.csv";

PROCEDURE atualizar_observacoes DO
CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22;
CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id);
END

CALL atualizar_observacoes;

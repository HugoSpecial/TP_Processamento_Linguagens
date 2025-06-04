import table observacoes from "data/observacoes.csv";
import table estacoes from "data/estacoes.csv";

select * from observacoes where Temperatura < 20;

PROCEDURE atualizar_observacoes DO
CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22;
print table mais_quentes;
CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id);
print table completo;
END

CALL atualizar_observacoes;

select * from completo where Local = "Terras de Bouro/Barral (CIM)";

Export table completo as "completo.csv";

;;;

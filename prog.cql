import table observacoes from "observacoes.csv";
create table obs SELECT Temperatura FROM observacoes WHERE Temperatura < 22;
select * from obs where Temperatura = 12.5;
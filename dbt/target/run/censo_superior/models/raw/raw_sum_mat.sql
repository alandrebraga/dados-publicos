

  create or replace view `educacao-superior-415319`.`raw_dados_publicos`.`raw_sum_mat`
  OPTIONS()
  as select
    sum(qt_mat) as total_matriculados,
    sum(qt_ing) as total_ingressantes
from `educacao-superior-415319.raw_dados_publicos.cursos_2022`;


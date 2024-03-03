SELECT
    nu_ano_censo,
    no_cine_rotulo,
    co_cine_rotulo,
    {{ modalidade_ensino('tp_modalidade_ensino') }} as modalidade_ensino,
    sum(qt_mat) as qt_mat
FROM `educacao-superior-415319.raw_dados_publicos.cursos_2022`
GROUP BY nu_ano_censo, no_cine_rotulo, co_cine_rotulo, tp_modalidade_ensino

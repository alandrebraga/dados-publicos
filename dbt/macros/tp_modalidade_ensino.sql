{% macro modalidade_ensino(tp_modalidade_ensino) %}
    CASE
        WHEN {{ tp_modalidade_ensino }} = 1 THEN 'Presencial'
        WHEN {{ tp_modalidade_ensino }} = 2 THEN 'EAD'
        ELSE 'Não identificado'
    END
{% endmacro %}